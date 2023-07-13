from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

def sample_data(request):
    person= {'firstname': 'Priska', 'lastname': 'Kashyap'}
    item_list = {"Chocolate": 4, "Pen": 10, "Pencil": 3}
    order_number= "000132342"
    context= {
        'person': person,
        'item_list': item_list,
        'order_number': order_number,
        }
    return JsonResponse(context)