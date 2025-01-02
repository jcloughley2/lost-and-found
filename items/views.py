from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Item
from .forms import ItemForm

def home(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item reported successfully!')
            return redirect('home')
    else:
        form = ItemForm()
    
    items = Item.objects.all().order_by('-date')
    return render(request, 'items/home.html', {
        'form': form,
        'items': items
    })

def report_found(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Found item has been successfully listed!')
            return redirect('home')
    else:
        form = FoundItemForm()
    
    return render(request, 'items/report_found.html', {'form': form})

def report_lost(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lost item has been successfully listed!')
            return redirect('home')
    else:
        form = LostItemForm()
    
    return render(request, 'items/report_lost.html', {'form': form})
