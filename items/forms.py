from django import forms
from .models import Item

class ItemFormBase(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'location', 'contact_info', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class FoundItemForm(ItemFormBase):
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = 'found'
        if commit:
            instance.save()
        return instance

class LostItemForm(ItemFormBase):
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = 'lost'
        if commit:
            instance.save()
        return instance 