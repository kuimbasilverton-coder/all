from datetime import timedelta
from django.utils import timezone
from django.db import OperationalError, ProgrammingError

class TrackVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            from elearning.models import Visit
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            user = request.user if request.user.is_authenticated else None

            recent_visit = Visit.objects.filter(
                user=user,
                session_key=session_key,
                visit_time__gte=timezone.now() - timedelta(hours=1)
            ).exists()

            if not recent_visit:
                Visit.objects.create(user=user, session_key=session_key)
        except Exception:
            pass  # Never let tracking break the site

        response = self.get_response(request)
        return response
