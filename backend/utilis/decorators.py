from functools import wraps
from django.http import JsonResponse

def require_owner(model_class, pk_field='pk'):
    """Decorator to check if the user is the owner of an object."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            obj_id = kwargs.get(pk_field)
            obj = model_class.objects.filter(pk=obj_id).first()
            if not obj:
                return JsonResponse({'error': 'Not found'}, status=404)
            if hasattr(obj, 'created_by') and obj.created_by != request.user:
                return JsonResponse({'error': 'Permission denied'}, status=403)
            return view_func(request, obj, *args, **kwargs)
        return wrapper
    return decorator
