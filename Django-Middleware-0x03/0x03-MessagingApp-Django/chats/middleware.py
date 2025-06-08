from datetime import datetime
import logging
from django.http import HttpRequest

# Configure logging to write to a file
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Get the authenticated user or 'Anonymous'
        user = getattr(request, 'user', None)
        username = user.username if user and user.is_authenticated else 'Anonymous'
        
        # Log the request details
        log_message = f"{datetime.now()} - User: {username} - Path: {request.path}"
        logger.info(log_message)
        
        response = self.get_response(request)
        return response