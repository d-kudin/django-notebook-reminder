#/website/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Record, Category

# User registration form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))

    # Link the form to the built-in User model
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Max 150 characters. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>At least 8 characters</li>'
            '<li>Cannot be entirely numeric</li>'
            '</ul>'
        )

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<small class="form-text text-muted">Enter the same password as before, for verification.</small>'

# Form for creating and editing user notes (records)
class RecordForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}),
        label='Title'
    )
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Note content', 'class': 'form-control', 'rows': 6}),
        label='Content'
    )
    deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Deadline'
    )
    reminder = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Reminder'
    )
    is_priority = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Priority'
    )
    status_color = forms.ChoiceField(
        choices=Record.STATUS_COLOR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Status'
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Category'
    )

    # Link the form to the Record model and define editable fields
    class Meta:
        model = Record
        fields = ['title', 'content', 'deadline', 'reminder', 'is_priority', 'status_color', 'category']
