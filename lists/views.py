#  from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from lists.models import Item


@csrf_exempt
def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text', '')
        Item.objects.create(text=new_item_text)
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html')


@csrf_exempt
def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
