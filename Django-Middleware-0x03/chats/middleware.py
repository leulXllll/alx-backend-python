from django.http import HttpResponseForbidden
from datetime import datetime, time
from django.http import HttpResponseForbidden
from datetime import datetime, timedelta
from collections import defaultdict
import logging
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
import logging
from datetime import datetime
from django.http import HttpRequest

# Set up logging configuration
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class RequestLoggingMiddleware:
    """Middleware to log all incoming requests"""
    
    def __init__(self, get_response):
        """Initialize the middleware"""
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        """Process each request and log details"""
        # Get user information
        user = getattr(request, 'user', None)
        username = user.username if user and user.is_authenticated else 'Anonymous'
        
        # Log request details
        log_message = (
            f"User: {username} - "
            f"Method: {request.method} - "
            f"Path: {request.path} - "
            f"IP: {self.get_client_ip(request)}"
        )
        logger.info(log_message)
        
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Extract client IP from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


logger = logging.getLogger(__name__)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = defaultdict(list)
        self.limit = 5  # 5 messages
        self.time_window = 60  # 60 seconds (1 minute)

    def __call__(self, request):
        # Only process POST requests to message endpoints
        if request.method == 'POST' and ('/messages/' in request.path or '/chats/' in request.path):
            ip_address = self.get_client_ip(request)
            now = datetime.now()
            
            # Remove old timestamps
            self.message_counts[ip_address] = [
                ts for ts in self.message_counts[ip_address]
                if now - ts < timedelta(seconds=self.time_window)
            ]
            
            # Check if limit exceeded
            if len(self.message_counts[ip_address]) >= self.limit:
                logger.warning(f"Rate limit exceeded for IP: {ip_address}")
                return HttpResponseForbidden(
                    "Too many messages sent. Please wait 1 minute before sending more.",
                    status=429
                )
            
            # Record new message
            self.message_counts[ip_address].append(now)
        
        return self.get_response(request)

    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define allowed hours (9AM to 6PM)
        self.allowed_start = time(9, 0)  # 9:00 AM
        self.allowed_end = time(18, 0)   # 6:00 PM

    def __call__(self, request):
        current_time = datetime.now().time()
        
        # Check if request path starts with /chats/ (or your chat endpoints)
        if request.path.startswith('/chats/') or request.path.startswith('/api/chats/'):
            if not (self.allowed_start <= current_time <= self.allowed_end):
                return HttpResponseForbidden(
                    "Chat access is only available between 9AM and 6PM"
                )
        
        return self.get_response(request)
    
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_paths = [
            '/api/admin/',
            '/api/moderator/',
            '/api/delete/'
        ]
        self.allowed_roles = ['admin', 'moderator']

    def __call__(self, request):
        # Check if request path requires special permissions
        if any(path in request.path for path in self.protected_paths):
            user = request.user
            
            # Check if user is authenticated and has required role
            if not (user.is_authenticated and hasattr(user, 'profile') and 
                   user.profile.role in self.allowed_roles):
                return HttpResponseForbidden(
                    "You don't have permission to access this resource",
                    status=403
                )
        
        return self.get_response(request)
    
    