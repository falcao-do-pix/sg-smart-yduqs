from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages

def student_required(function=None, login_url='login_aluno'):
    """
    Decorator para views que verifica se o utilizador está logado E se não é
    um staff/admin. Se for um admin, ele é redirecionado.
    """
    def check_user(user):
        # A verificação passa se o utilizador estiver autenticado E não for staff/superuser.
        return user.is_authenticated and not (user.is_staff or user.is_superuser)

    actual_decorator = user_passes_test(
        check_user,
        login_url=login_url,
        redirect_field_name=None
    )

    if function:
        return actual_decorator(function)
    return actual_decorator

def admin_logout_required(view_func):
    """
    Decorator que verifica se um utilizador staff/admin está logado.
    Se estiver, ele é deslogado antes de poder aceder à página (como a de login de aluno).
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            from django.contrib.auth import logout
            logout(request)
            messages.info(request, "Você foi desconectado da sua conta de administrador para poder aceder a esta página.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
