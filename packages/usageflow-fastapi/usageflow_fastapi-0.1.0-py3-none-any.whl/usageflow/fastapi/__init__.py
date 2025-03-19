from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from usageflow.core import UsageFlowClient
import time
from typing import Dict, Any, Optional

class UsageFlowMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, api_key: str):
        super().__init__(app)
        self.client = UsageFlowClient(api_key)

    async def dispatch(self, request: Request, call_next):
        """Process request and response"""
        start_time = time.time()

        # Store request body for later use
        request.state.body_data = await self._get_request_body(request)

        # Prepare request metadata
        metadata = {
            "method": request.method,
            "url": str(request.url.path),
            "rawUrl": str(request.url),
            "clientIP": request.client.host if request.client else None,
            "userAgent": request.headers.get("user-agent"),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "headers": {k: ("****" if "key" in k.lower() else v) for k, v in request.headers.items()},
            "queryParams": dict(request.query_params),
            "pathParams": dict(request.path_params),
            "body": request.state.body_data,
            "userId": self._extract_user_id(request),
        }

        # Store metadata for later use
        request.state.metadata = metadata

        # Get ledger ID
        ledger_id = self._guess_ledger_id(request)
        
        # Allocate request
        success, result = self.client.allocate_request(ledger_id, metadata)
        
        if not success:
            error_message = result.get('message', 'Request fulfillment failed')
            status_code = result.get('status_code', 500)
            
            if status_code == 429:
                return Response(content={"error": "Rate limit exceeded"}, status_code=429)
            elif status_code == 403:
                return Response(content={"error": "Access forbidden"}, status_code=403)
            elif status_code == 401:
                return Response(content={"error": "Unauthorized access"}, status_code=401)
            else:
                return Response(content={"error": error_message}, status_code=status_code)

        # Store event ID
        request.state.event_id = result.get('eventId') if result else None

        # Process the request
        response = await call_next(request)

        # Log response if we have an event ID
        if hasattr(request.state, "event_id") and request.state.event_id:
            metadata = request.state.metadata
            metadata.update({
                "responseStatusCode": response.status_code,
                "responseHeaders": dict(response.headers),
                "duration": int((time.time() - start_time) * 1000),
            })
            
            self.client.fulfill_request(ledger_id, request.state.event_id, metadata)

        return response

    async def _get_request_body(self, request: Request) -> Optional[Dict[str, Any]]:
        """Extract and return request body, safely handling different content types"""
        try:
            content_type = request.headers.get("content-type", "")
            if "application/json" in content_type:
                return await request.json()
            elif "application/x-www-form-urlencoded" in content_type:
                form = await request.form()
                return dict(form)
            elif "multipart/form-data" in content_type:
                form = await request.form()
                return dict(form)
            else:
                body = await request.body()
                return body.decode("utf-8")
        except Exception:
            return None

    def _extract_user_id(self, request: Request) -> str:
        """Extract user ID from JWT or headers"""
        token = self.client.extract_bearer_token(request.headers.get("Authorization"))
        if token:
            claims = self.client.decode_jwt_unverified(token)
            return claims.get("sub", "anonymous") if claims else "anonymous"
        return request.headers.get("X-User-ID", "anonymous")

    def _guess_ledger_id(self, request: Request) -> str:
        """Determine the ledger ID from the request"""
        method = request.method
        url = request.url.path

        # Check config for identity field configuration
        config = self.client.get_config()
        if config:
            field_name = config.get("identityFieldName")
            location = config.get("identityFieldLocation")

            if field_name and location:
                match location:
                    case "path_params":
                        # Get path parameters from the request
                        path_params = request.path_params
                        if field_name in path_params:
                            return method + " " + url + " " + self.client.transform_to_ledger_id(path_params[field_name])

                    case "query_params":
                        # Check query parameters
                        query_params = dict(request.query_params)
                        if field_name in query_params:
                            return method + " " + url + " " + self.client.transform_to_ledger_id(query_params[field_name])

                    case "body":
                        # Check request body
                        try:
                            if hasattr(request.state, "body_data"):
                                body_data = request.state.body_data
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
        path_segments = request.url.path.strip("/").split("/")
        for i, segment in enumerate(path_segments):
            if segment == "accounts" and i + 1 < len(path_segments):
                return method + " " + url + " " + self.client.transform_to_ledger_id(path_segments[i + 1])

        # Check URL query parameters
        query_params = dict(request.query_params)
        for key in ["userId", "accountId"]:
            if key in query_params:
                return method + " " + url + " " + self.client.transform_to_ledger_id(query_params[key])

        # Check JSON body
        try:
            if hasattr(request.state, "body_data"):
                body_data = request.state.body_data
                for key in ["userId", "accountId"]:
                    if key in body_data:
                        return method + " " + url + " " + self.client.transform_to_ledger_id(body_data[key])
        except Exception:
            pass

        # Fallback to default ledgerId
        return f"{method} {url}"

__version__ = "0.1.0"
__all__ = ["UsageFlowMiddleware"] 