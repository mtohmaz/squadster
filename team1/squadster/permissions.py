from rest_framework import permissions

# http://www.django-rest-framework.org/api-guide/permissions/#custom-permissions
class IsHost(permissions.BasePermission):
    message = 'Must be the host to perform this action.'
    
    """
    def has_permission(self, request, view):
        pass
    """
    
    def has_object_permission(self, request, view, obj):
        user_id = request.user.id
        host_id = obj.host_id
        if user_id == host_id:
            return True
        else:
            return False
