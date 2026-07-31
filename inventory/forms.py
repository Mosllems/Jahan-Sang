from django import forms

from .models import Stone, Tool


class StoneForm(forms.ModelForm):
    class Meta:
        model = Stone
        fields = ['name', 'category', 'image', 'quantity', 'origin', 'dimensions', 'thickness']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'نام'}),
            'image': forms.FileInput(attrs={'placeholder': 'تصویر'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'مقدار'}),
            'category': forms.Select(attrs={'placeholder': 'دسته بندی'}),
            'origin': forms.TextInput(attrs={'placeholder': 'منشا'}),
            'dimensions': forms.TextInput(attrs={'placeholder': 'ابعاد'}),
            'thickness': forms.TextInput(attrs={'placeholder': 'ضخامت'}),
        }


class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['name', 'category', 'image', 'brand', 'condition']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'نام'}),
            'category': forms.Select(attrs={'placeholder': 'دسته بندی'}),
            'image': forms.FileInput(attrs={'placeholder': 'تصویر'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'مقدار'}),
            'brand': forms.TextInput(attrs={'placeholder': 'برند'}),
            'condition': forms.Select(attrs={'placeholder': 'وضعیت'}),}
