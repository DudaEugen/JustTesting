import os


def base_template(request):
    return {
        "navbar_brand": os.getenv("NAVBAR_BRAND"),
    }
