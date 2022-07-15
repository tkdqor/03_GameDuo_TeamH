from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Assignee : 민지

    관리자와 해당 obj와 동일한 유저만 접근이 가능합니다.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return True
            elif request.user == obj.user:
                return True
            else:
                return False
        else:
            False
