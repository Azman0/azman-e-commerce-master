from .models import Categories


def categories(request):
    categories = Categories.objects.all().exclude(status='hidden')

    return { "categories":categories }
