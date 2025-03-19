from flask import Flask, request
from usageflow.core import UsageFlowClient
import time
from typing import Dict, Any, Optional

class UsageFlowMiddleware:
    def __init__(self, app: Flask, api_key: str):
        self.app = app
        self.client = UsageFlowClient(api_key)
        self._init_middleware()

    def _init_middleware(self):
        """Initialize the middleware by registering before/after request handlers"""
        self.app.before_request(self._before_request)
        self.app.after_request(self._after_request)

    def _before_request(self):
        """Handle request before it reaches the view"""
        request.usageflow_start_time = time.time()
        
        # Prepare request metadata
        metadata = {
            "method": request.method,
            "url": request.path,
            "rawUrl": request.url,
            "clientIP": request.remote_addr,
            "userAgent": request.headers.get("user-agent"),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "headers": {k: ("****" if "key" in k.lower() else v) for k, v in request.headers.items()},
            "queryParams": dict(request.args),
            "body": request.get_json(silent=True),
            "userId": self._extract_user_id(),
        }

        # Store metadata for later use
        request.usageflow_metadata = metadata

        # Get ledger ID and allocate request
        ledger_id = self._guess_ledger_id()
        success, result = self.client.allocate_request(ledger_id, metadata)
        
        if not success:
            error_message = result.get('message', 'Request fulfillment failed')
            status_code = result.get('status_code', 500)
            
            if status_code == 429:
                return {"error": "Rate limit exceeded"}, 429
            elif status_code == 403:
                return {"error": "Access forbidden"}, 403
            elif status_code == 401:
                return {"error": "Unauthorized access"}, 401
            else:
                return {"error": error_message}, status_code

        # Store event ID and ledger ID for later use
        request.usageflow_event_id = result.get('eventId') if result else None
        request.usageflow_ledger_id = ledger_id

    def _after_request(self, response):
        """Handle request after it has been processed by the view"""
        if hasattr(request, "usageflow_event_id") and request.usageflow_event_id:
            metadata = request.usageflow_metadata
            metadata.update({
                "responseStatusCode": response.status_code,
                "responseHeaders": dict(response.headers),
                "duration": int((time.time() - request.usageflow_start_time) * 1000),
            })
            
            self.client.fulfill_request(
                request.usageflow_ledger_id,
                request.usageflow_event_id,
                metadata
            )

        return response

    def _extract_user_id(self) -> str:
        """Extract user ID from JWT or headers"""
        token = self.client.extract_bearer_token(request.headers.get("Authorization"))
        if token:
            claims = self.client.decode_jwt_unverified(token)
            return claims.get("sub", "anonymous") if claims else "anonymous"
        return request.headers.get("X-User-ID", "anonymous")

    def _guess_ledger_id(self) -> str:
        """Determine the ledger ID from the request"""
        method = request.method
        url = request.path

        # Check config for identity field configuration
        config = self.client.get_config()
        if config:
            field_name = config.get("identityFieldName")
            location = config.get("identityFieldLocation")

            if field_name and location:
                match location:
                    case "path_params":
                        # Get path parameters from the request
                        if field_name in request.view_args or {}:
                            return method + " " + url + " " + self.client.transform_to_ledger_id(request.view_args[field_name])

                    case "query_params":
                        # Check query parameters
                        if field_name in request.args:
                            return method + " " + url + " " + self.client.transform_to_ledger_id(request.args[field_name])

                    case "body":
                        # Check request body
                        try:
                            body_data = request.get_json(silent=True) or {}
                            if field_name in body_data:
                                return method + " " + url + " " + self.client.transform_to_ledger_id(body_data[field_name])
                        except Exception:
                            pass

                    case "bearer_token":
                        # Extract from bearer token
                        auth_header = request.headers.get("Authorization")
                        if auth_header:
                            token = self.client.extract_bearer_token(auth_header)
                            if token:
                                claims = self.client.decode_jwt_unverified(token)
                                if claims and field_name in claims:
                                    return method + " " + url + " " + self.client.transform_to_ledger_id(claims[field_name])

        # Fallback to legacy logic if no config match or value not found
        # Check Authorization header for Bearer token
        auth_header = request.headers.get("Authorization")
        if auth_header:
            token = self.client.extract_bearer_token(auth_header)
            if token:
                claims = self.client.decode_jwt_unverified(token)
                if claims and "sub" in claims:
                    return method + " " + url + " " + self.client.transform_to_ledger_id(claims["sub"])

        # Check URL path for accountId
        path_segments = request.path.strip("/").split("/")
        for i, segment in enumerate(path_segments):
            if segment == "accounts" and i + 1 < len(path_segments):
                return method + " " + url + " " + self.client.transform_to_ledger_id(path_segments[i + 1])

        # Check URL query parameters
        for key in ["userId", "accountId"]:
            if key in request.args:
                return method + " " + url + " " + self.client.transform_to_ledger_id(request.args[key])

        # Check JSON body
        try:
            body_data = request.get_json(silent=True) or {}
            for key in ["userId", "accountId"]:
                if key in body_data:
                    return method + " " + url + " " + self.client.transform_to_ledger_id(body_data[key])
        except Exception:
            pass

        # Fallback to default ledgerId
        return f"{method} {url}"

__version__ = "0.1.0"
__all__ = ["UsageFlowMiddleware"] 