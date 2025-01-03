from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Item
from .forms import FoundItemForm, LostItemForm
import logging

logger = logging.getLogger(__name__)

def home(request):
    items = Item.objects.all().order_by('-date')
    return render(request, 'items/home.html', {'items': items})

def report_found(request):
    if request.method == 'POST':
        logger.debug("Processing POST request for found item")
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            logger.debug("Found item form is valid, saving")
            try:
                item = form.save()
                logger.debug(f"Found item saved successfully. ID: {item.id}")
                logger.debug(f"Tags after save: {list(item.tags.all())}")
                messages.success(request, 'Found item has been reported successfully!')
            except Exception as e:
                logger.error(f"Error saving found item: {str(e)}")
                messages.error(request, 'Error saving item')
            return redirect('home')
        else:
            logger.error(f"Form errors: {form.errors}")
    else:
        form = FoundItemForm()
    
    return render(request, 'items/report_found.html', {'form': form})

def report_lost(request):
    if request.method == 'POST':
        logger.debug("Processing POST request for lost item")
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            logger.debug("Lost item form is valid, saving")
            try:
                item = form.save()
                logger.debug(f"Lost item saved successfully. ID: {item.id}")
                logger.debug(f"Tags after save: {list(item.tags.all())}")
                messages.success(request, 'Lost item has been reported successfully!')
            except Exception as e:
                logger.error(f"Error saving lost item: {str(e)}")
                messages.error(request, 'Error saving item')
            return redirect('home')
        else:
            logger.error(f"Form errors: {form.errors}")
    else:
        form = LostItemForm()
    
    return render(request, 'items/report_lost.html', {'form': form})
