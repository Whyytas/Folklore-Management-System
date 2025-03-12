import traceback
import json
from django.http import JsonResponse


class CatchAllExceptionsMiddleware:
    """Middleware to catch all unhandled exceptions and return a JSON error response."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            error_trace = traceback.format_exc()
            print(error_trace)  # This will log to Azure logs

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Handle AJAX requests
                return JsonResponse({
                    "status": "error",
                    "message": str(e),
                    "trace": error_trace.split("\n")
                }, status=500)

            # For non-AJAX requests, return HTML error message
            return JsonResponse({
                "error": "A server error occurred. Please check the console logs for details.",
                "details": str(e)
            }, status=500)

        return response
