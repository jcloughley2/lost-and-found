from django import forms
from .models import Item, Tag

class ItemForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'data-role': 'tagsinput',
            'placeholder': 'Add tags...'
        })
    )

    class Meta:
        model = Item
        fields = ['title', 'description', 'location', 'status', 'contact_info', 'tags_input']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_tags_input(self):
        tags_input = self.cleaned_data.get('tags_input', '')
        if not tags_input:
            return []
        tag_names = [t.strip().lower() for t in tags_input.split(',') if t.strip()]
        tags = []
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        return tags

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            instance.tags.set(self.cleaned_data.get('tags_input', []))
        return instance 