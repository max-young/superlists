#  from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from lists.forms import ItemForm
from lists.models import Item, List


@csrf_exempt
def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


@csrf_exempt
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            item = Item.objects.create(text=request.POST['text'], list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})


@csrf_exempt
def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        item = Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})


@csrf_exempt
def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['text'], list=list_)
    return redirect(list_)
