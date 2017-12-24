import time

from django.utils.deprecation import MiddlewareMixin


class StatsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """Store the start time when the request comes in."""
        request.start_time = time.time()

    def process_response(self, request, response):
        """Calculate and output the page generation duration."""
        # Get the start time from the request and calculate how long
        # the response took.
        duration = time.time() - request.start_time

        # Add the header.
        response["X-Page-Generation-Duration-ms"] = int(duration * 1000)
        return response
