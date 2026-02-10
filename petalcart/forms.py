from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from petalcart.models import Flower, Comment
from django.forms import ModelForm


class ShopRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Shop username',
            'autocomplete': 'username'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Shop email',
            'autocomplete': 'email'
        })
    )
    shop_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your shop name (e.g., "Rose Garden Flowers")'
        })
    )
    shop_address = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Complete shop address',
            'rows': 3
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a strong password',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-enter your password',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'shop_name', 'shop_address']


class FlowerForm(ModelForm):
    flowername = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Flower name (e.g., Rose, Tulip)',
            'required': True
        })
    )
    img = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'required': True
        })
    )
    desc = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe the flower (type, color, care tips)',
            'rows': 4,
            'required': True
        })
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Price per unit',
            'step': '0.01',
            'min': '0',
            'required': True
        })
    )

    class Meta:
        model = Flower
        exclude = ["shop"]


class CommentForm(ModelForm):
    body = forms.CharField(
        label='Your Review',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Share your experience with this flower...',
            'rows': 4,
            'required': True
        })
    )
    rating = forms.IntegerField(
        label='Rating (1-5)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '5',
            'type': 'number',
            'placeholder': 'Rate 1-5 stars'
        })
    )

    class Meta:
        model = Comment
        fields = ["body", "rating"]