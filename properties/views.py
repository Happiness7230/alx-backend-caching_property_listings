from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_propertie, get_redis_cache_metrics

# Cache for 15 minutes (60 seconds * 15)
@cache_page(60 * 15)
def property_list(request):
    properties = Property.objects.all().values()
    return JsonResponse({
        "data": properties
    })

def property_list(request):
    properties = get_all_properties()
    data = [{'id': p.id, 'title': p.title, 'price': p.price} for p in properties]
    return JsonResponse({'data': data})

def redis_metrics(request):
    metrics = get_redis_cache_metrics()
    return JsonResponse(metrics)
