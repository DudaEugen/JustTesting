from django.http import Http404


def user_permissions_decorator(foo):
    def check_permissions(request, **kwargs):
        # simple implementation
        if request.user.is_authenticated and request.user.is_superuser:
            return foo(request, **kwargs)
        else:
            raise Http404("У Вас немає прав доступу до цієї сторінки")
    return check_permissions
