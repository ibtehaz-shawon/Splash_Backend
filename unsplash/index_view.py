import datetime
import django
from django.conf.global_settings import TIME_ZONE, DEBUG, LANGUAGE_CODE
from django.http import HttpResponse
from django.template import loader
from unsplash.models import Photo


def original_index(request):
    template = loader.get_template('unsplash/index.html')
    if request.method == 'GET':
        latest_photos = Photo.objects.order_by('-created_at')
        total_photos = len(latest_photos)
        ten_photos = Photo.objects.order_by('-created_at')[:10]

        context = {
            'message': 'Hello World',
            'total_photos': total_photos,
            'photos': ten_photos,
            'django_version': django.get_version(),
            'current_time': datetime.datetime.now().strftime('%H:%M'),
            'system_timezone': TIME_ZONE,
            'debug_status': DEBUG,
            'system_language': LANGUAGE_CODE
        }

        print "Total Photos: " + str(len(latest_photos))
        return HttpResponse(template.render(context, request))

    else:
        context = {
            'message': 'Wrong URI Request'
        }
        return HttpResponse(template.render(context, request))


