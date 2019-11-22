from django.conf import settings as sett


def settings(request):
    return {"settings": sett}
