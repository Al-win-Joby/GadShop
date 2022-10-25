from unicodedata import category


from .models import Category

def menulinks(request):
    if request.user is not None:
        links=Category.objects.all()
        return dict(links=links)
    else:
        return None 