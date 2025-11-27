# middleware.py
from datetime import datetime, time, timedelta
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        with open("request_logs.txt", "a") as file:
            file.write(log_entry)

        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()

        # Restrict between 6PM and 9PM (18:00–21:00)
        start = time(18, 0)  # 6 PM
        end = time(21, 0)    # 9 PM

        if start <= now <= end:
            return HttpResponseForbidden("<h3>Access to chat is restricted at this time.</h3>")

        return self.get_response(request)
    
from django.http import HttpResponseForbidden

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}  # {ip: [timestamps]}

    def __call__(self, request):
        if request.method == "POST":  # Count only chat message posts
            ip = request.META.get('REMOTE_ADDR')
            now = datetime.now()

            # Create entry if IP not in log
            if ip not in self.message_log:
                self.message_log[ip] = []

            # Filter out timestamps older than 1 minute
            one_minute_ago = now - timedelta(minutes=1)
            self.message_log[ip] = [
                t for t in self.message_log[ip] if t > one_minute_ago
            ]

            # Enforce limit → 5 messages/minute
            if len(self.message_log[ip]) >= 5:
                return HttpResponseForbidden(
                    "<h3>Message limit reached. Try again in a minute.</h3>"
                )

            # Record new message timestamp
            self.message_log[ip].append(now)

        return self.get_response(request)
    
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/chat/admin/"):
            user = request.user
            if not user.is_authenticated or getattr(user, "role", None) not in ["admin", "moderator"]:
                return HttpResponseForbidden("You do not have permission to access this page.")
        return self.get_response(request)