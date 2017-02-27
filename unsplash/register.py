from django.forms import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

# http://stackoverflow.com/questions/30292540/posting-data-from-a-form-into-the-database-using-django
def register_phone(request):
    template = loader.get_template('unsplash/register.html')
    template_file = "unsplash/register.html"

    if request.method == 'GET':
        context_instance = RequestContext(request)
        context = {}
        print "GET Req"
        return render(request, template_file, context)

    elif request.method == 'POST':
        device_id = request.POST.get('device_id')
        device_height = request.POST.get('device_height')
        device_width = request.POST.get('device_width')

        print device_id
        print device_height
        print device_width

        response_data = {}
        success_message = []
        error_message = []

        if len(device_id) > 0 & len(device_height) > 0 & len(device_width) > 0:
            # success
            success = "Successful"
            success_message.append(success)
        else:
            if len(device_id) == 0:
                error_message.append("Device ID required")
                print error_message
            if len(device_height) == 0:
                error_message.append("Device Width required")
                print error_message
            if len(device_width) == 0:
                error_message.append("Device Height required")
                print error_message

        if len(error_message) > 0:
            # error stayed
            response_data['error'] = error_message
        else:
            response_data['success'] = success_message

        print response_data
        return render(request, template_file, response_data)
