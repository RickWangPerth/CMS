from functools import wraps
from django.http import JsonResponse

def cognito_auth_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.cognito_user:
            return JsonResponse({
                'error': 'Authentication required'
            }, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper 