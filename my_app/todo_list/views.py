from django.shortcuts import render, redirect
from .models import List
from .forms import ListForm
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
    import json
    import requests
    #managebac API call test
    headers = {
    'auth-token': '62170e73818bebc4e88a7f60e2f86d81a93d064ceec190a5795dc9a79c550841',}
    response = requests.get('https://api.managebac.com/v2/classes', headers=headers)
    mbClasses = json.loads(response.content)

    if request.method == 'POST':
        form = ListForm(request.POST or None)
        if form.is_valid():
            form.save()
            all_items = List.objects.all
            messages.success(request,('Item added to list'))
            return render(request,'home.html',{'all_items' : all_items})

    else:

        all_items = List.objects.all
        return render(request,'home.html',{'all_items' : all_items})

def about(request):
    my_name ="Nick"
    return render(request,'about.html',{'name' : my_name})

def delete(request, list_id):
    item = List.objects.get(pk=list_id)
    item.delete()
    messages.success(request,('Item deleted'))
    return redirect('home')

def cross_off(request, list_id):
    item = List.objects.get(pk=list_id)
    item.completed = True
    item.save()
    return redirect('home')

def uncross(request, list_id):
    item = List.objects.get(pk=list_id)
    item.completed = False
    item.save()
    return redirect('home')

def edit(request,list_id):

    if request.method == 'POST':
        item = List.objects.get(pk=list_id)

        form = ListForm(request.POST or None, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request,('Item edited'))
            return redirect('home')

    else:

        item = List.objects.get(pk=list_id)
        return render(request,'edit.html',{'item' : item})

def search(request):
    
    if request.method == 'POST' and request.POST['item']:
        filterTerm = request.POST['item']
        filteredList = List.objects.filter(item__contains=filterTerm)
        
        messages.success(request,('Tasks containing '+filterTerm))
        return render(request,'home.html',{'all_items' : filteredList})

    else:

        all_items = List.objects.all
        return render(request,'home.html',{'all_items' : all_items})

#sort items alphabetically
def sortAlpha(request):
    
        sorted_items = List.objects.order_by('item')
        return render(request,'home.html',{'all_items' : sorted_items})

#sort items alphabetically
def filterDone(request,state):
    filterSwitch = ''
    if state == 'done':
        filterSwitch = True
    else:
        filterSwitch = False
    filtered_items = List.objects.filter(completed=filterSwitch)
    return render(request,'home.html',{'all_items' : filtered_items})