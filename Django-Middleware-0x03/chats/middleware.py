from datetime import datetime, time, timedelta
from django.http import HttpResponseForbidden

# 1. Logging User Requests
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        with open("request_logs.txt", "a") as file:
            file.write(log_entry)

        return self.get_response(request)


# 2. Restrict Chat Access by Time
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/chat/"):
            now = datetime.now().time()
            start = time(18, 0)  # 6 PM
            end = time(21, 0)    # 9 PM

            if now < start or now > end:  # Deny access **outside 6–9 PM**
                return HttpResponseForbidden(
                    "<h3>Access to chat is restricted at this time.</h3>"
                )

        return self.get_response(request)


# 3. Detect and Block Offensive Language (Rate Limiting)
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}  # {ip: [timestamps]}

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/chat/"):
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            if ',' in ip:
                ip = ip.split(',')[0]

            now = datetime.now()
            if ip not in self.message_log:
                self.message_log[ip] = []

            # Keep only messages in the last 1 minute
            one_minute_ago = now - timedelta(minutes=1)
            self.message_log[ip] = [t for t in self.message_log[ip] if t > one_minute_ago]

            if len(self.message_log[ip]) >= 5:
                return HttpResponseForbidden(
                    "<h3>Message limit reached. Try again in a minute.</h3>"
                )

            self.message_log[ip].append(now)

        return self.get_response(request)


# 4. Enforce Chat User Role Permissions
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/chat/admin/"):
            user = request.user
            if not user.is_authenticated or getattr(user, "role", None) not in ["admin", "moderator"]:
                return HttpResponseForbidden(
                    "<h3>You do not have permission to access this page.</h3>"
                )
        return self.get_response(request)
