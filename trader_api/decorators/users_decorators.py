# users/decorators.py
from functools import wraps
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

def user_type_required(required_type):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.type == required_type:
                return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({'detail': 'Permission denied'}, status=403)
        return _wrapped_view
    return decorator

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and group_name in request.user.groups.values_list('name', flat=True):
                return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({'detail': 'Permission denied'}, status=403)
        return _wrapped_view
    return decorator
