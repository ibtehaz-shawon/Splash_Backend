import json

from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import loader

# http://stackoverflow.com/questions/30292540/posting-data-from-a-form-into-the-database-using-django
# https://tutorial.djangogirls.org/en/django_forms/
from unsplash.register_phone_form import RegisterForm


def register_phone(request):
    template = loader.get_template('unsplash/register.html')
    template_file = "unsplash/register.html"

    if request.method == 'GET':
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, template_file, context)

    elif request.method == 'POST':
        device_id = request.POST.get('device_id')
        device_height = request.POST.get('device_height')
        device_width = request.POST.get('device_width')

        print request.body
        print device_height
        print device_width

        response_data = {}
        error_message = {}

        if form.is_valid():
            register = form.save()
            print register.unique_id

            success_message = {
                'unique_id': str(register.unique_id),
                'message': 'successfully registered',
            }
            form = RegisterForm()
            context = {
                'form': form
            }

            # Add JSON response here
            response_data['success'] = success_message
            print response_data
            return HttpResponse(json.dumps(response_data), content_type='application/json')
            # open the following only if needed to view another view.
            # return render(request, template_file, context)
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

            response_data['error'] = error_message
            return HttpResponse(json.dump(response_data), content_type='application/json')