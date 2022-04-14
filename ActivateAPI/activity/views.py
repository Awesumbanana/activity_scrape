from django.shortcuts import render
from django.http import JsonResponse
from activity.serializers import ActivityDetailsSerializer
from activity.crawler import Crawler


def index(request):
    return render(request, 'form.html')

def get_experience_details(query):
    c = Crawler()
    experience_details = c.get_experience_data(query)
    return experience_details

def query_experience(request):
    if request.method == 'POST':
        query = request.POST.get('textfield', None)
        details = get_experience_details(query)
        details_serializer = ActivityDetailsSerializer(details)
        print(details_serializer.data)
        return JsonResponse(details_serializer.data)
    else:
        return render(request, 'form.html')
