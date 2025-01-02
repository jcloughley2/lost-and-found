from django import forms
from .models import Item

class FoundItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'location', 'contact_info']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'location': 'Location where found'
        }

    def save(self, commit=True):
        instance = super().save(False)
        instance.item_type = Item.FOUND
        if commit:
            instance.save()
        return instance

class LostItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'location', 'contact_info']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'location': 'Last known location'
        }

    def save(self, commit=True):
        instance = super().save(False)
        instance.item_type = Item.LOST
        if commit:
            instance.save()
        return instance 