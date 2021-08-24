import os


def base_template(request):
    return {
        "navbar_brand": os.getenv("NAVBAR_BRAND"),
        "can_view_results": request.user.is_authenticated and \
                            request.user.has_perm("Testing.view_testingsession"),
    }
