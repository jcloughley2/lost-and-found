from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Item
from .forms import FoundItemForm, LostItemForm, ImageUploadForm
import logging
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .ai_utils import analyze_image
from django.db import models

logger = logging.getLogger(__name__)

def home(request):
    items = Item.objects.all().order_by('-date')[:5]
    return render(request, 'items/home.html', {'items': items})

def all_items(request):
    query = request.GET.get('q', '')
    items = Item.objects.all().order_by('-date')
    
    if query:
        items = items.filter(
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(location__icontains=query) |
            models.Q(tags__name__icontains=query)
        ).distinct()
    
    return render(request, 'items/all_items.html', {
        'items': items,
        'query': query
    })

@login_required
def report_found(request):
    if request.method == 'POST':
        logger.debug("Processing POST request for found item")
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            logger.debug("Found item form is valid, saving")
            try:
                item = form.save(commit=False)
                item.user = request.user  # Associate with logged-in user
                item.save()
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
    
    image_form = ImageUploadForm()

    return render(request, 'items/report_found.html', {'form': form, 'image_form': image_form})

@login_required
def report_lost(request):
    if request.method == 'POST':
        logger.debug("Processing POST request for lost item")
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            logger.debug("Lost item form is valid, saving")
            try:
                item = form.save(commit=False)
                item.user = request.user  # Associate with logged-in user
                item.save()
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
    
    image_form = ImageUploadForm()
    return render(request, 'items/report_lost.html', {'form': form, 'image_form': image_form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'items/register.html', {'form': form})

@login_required
def account(request):
    user_items = Item.objects.filter(user=request.user).order_by('-date')
    return render(request, 'items/account.html', {'user_items': user_items})

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            # Send image to OpenAI for title and description suggestions
            suggested_title, suggested_description = analyze_image(image)
            return JsonResponse({
                'suggested_title': suggested_title,
                'suggested_description': suggested_description
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)
