from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

from core.utils import is_in_share_tree









class InstancePreloaderAndPermissionChecker:
    """
    Decorator base class, which can replace id with model instance and throw 403 in defined cases.
    """

    default_set_key = ''
    default_get_key = ''

    #Set *model_class* in inheritors to some model class.
    model_class = None

    def __init__(self, set_key=None, get_key=None):
        """
        Decorator can transform django view attributes.
        """
        self.set_key = set_key or self.default_set_key
        self.get_key = get_key or self.default_get_key

    def has_permission(self, user, instance):
        """
        Override this method to determine if the *user* can represent wrapped action on the *instance*.
        """
        raise NotImplementedError()

    def __call__(self, view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            instance_id = kwargs.get(self.get_key)
            instance = get_object_or_404(self.model_class.objects, id=instance_id)
            if not self.has_permission(request.user, instance):
                return HttpResponseForbidden()
            kwargs[self.set_key] = instance
            del kwargs[self.get_key]
            return view_func(request, *args, **kwargs)
        return wrapper


class OwnerOnly(InstancePreloaderAndPermissionChecker):
    """
    Decorator base class, which can throw 403 if *request.user* is not in the owner tree.
    """
    def get_instance_owner(self, instance):
        """
        returns: *core.ShareTree* field of the instance, *instance.owner* by default.
        """
        return instance.owner

    def has_permission(self, user, instance):
        return is_in_share_tree(user, self.get_instance_owner(instance))