from django.http import HttpResponseForbidden
from functools import wraps

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if getattr(request.user, f'is_{role}', False):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have permission to view this page.")
        return _wrapped_view
    return decorator
