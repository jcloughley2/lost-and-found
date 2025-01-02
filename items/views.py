from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LostItemForm, FoundItemForm
from .models import Item

def home(request):
    items = Item.objects.all()  # ordering is handled by model Meta
    return render(request, 'items/home.html', {'items': items})

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
