# dashboard/decorators.py (Exemplo)

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def staff_required(function=None, login_url='login_dashboard'):
    """
    Decorator para views que verifica se o utilizador está logado E é um staff.
    """
    def check_user(user):
        # A verificação passa se o utilizador for staff ou superuser.
        return user.is_authenticated and (user.is_staff or user.is_superuser)

    actual_decorator = user_passes_test(
        check_user,
        login_url=login_url,
        redirect_field_name=None
    )

    if function:
        return actual_decorator(function)
    return actual_decorator