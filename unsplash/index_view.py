from django.http import HttpResponse
from django.template import loader
from unsplash.models import Photo


def original_index(request):
    latest_photos = Photo.objects.order_by('-created_at')
    template = loader.get_template('unsplash/index.html')
    context = {
        'message': 'Hello World',
        'photos': latest_photos
    }
    return HttpResponse(template.render(context, request))

