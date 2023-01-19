from django.utils.timezone import now


def year(request):
    return {
        'year': now().year,
    }
