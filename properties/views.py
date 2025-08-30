from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)  
def property_list(request):
    properties = get_all_properties()

    # Serialize property objects
    properties_data = [
        {
            'id': prop.pk,
            'title': prop.title,
            'description': prop.description,
            'price': str(prop.price),
            'location': prop.location,
            'created_at': prop.created_at.isoformat(),
        }
        for prop in properties
    ]

    # If the request is AJAX or wants JSON, return JSON
    if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
        return JsonResponse({'properties': properties_data})

    # Otherwise render HTML template
    return render(request, "properties/property_list.html", {"properties": properties})
