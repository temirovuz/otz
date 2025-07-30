from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAdminUserAndAuthenticated(permissions.BasePermission):
    """
    Faqatgina 'admin' bo‘lgan va avtorizatsiyadan o‘tgan foydalanuvchilarga
    barcha API'larni ishlatishga ruxsat beruvchi permission.
    """

    def has_permission(self, request, view):
        user = request.user

        # Foydalanuvchi avtorizatsiyadan o‘tganmi va adminmi – shuni tekshiradi
        if (
            user
            and user.is_authenticated
            and getattr(user, "user_type", None) == "admin"
        ):
            return True

        # Aks holda ruxsat berilmaydi
        raise PermissionDenied(detail="Sizga ushbu amalni bajarishga ruxsat yo‘q.")

class IsEmployeeUserAndAuthenticated(permissions.BasePermission):
    """
    Faqatgina 'admin' bo‘lgan va avtorizatsiyadan o‘tgan foydalanuvchilarga
    barcha API'larni ishlatishga ruxsat beruvchi permission.
    """

    def has_permission(self, request, view):
        user = request.user

        # Foydalanuvchi avtorizatsiyadan o‘tganmi va adminmi – shuni tekshiradi
        if (
            user
            and user.is_authenticated
            and getattr(user, "user_type", None) in ['admin', 'employee']
        ):
            return True

        # Aks holda ruxsat berilmaydi
        raise PermissionDenied(detail="Sizga ushbu amalni bajarishga ruxsat yo‘q.")