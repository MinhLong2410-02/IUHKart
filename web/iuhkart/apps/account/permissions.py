# permissions.py
from rest_framework import permissions

class IsVendor(permissions.BasePermission):
    """
    Allows access only to vendor users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_vendor

class IsCustomer(permissions.BasePermission):
    """
    Allows access only to customer users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_customer
