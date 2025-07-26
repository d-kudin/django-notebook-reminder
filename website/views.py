#/website/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, RecordForm
from .models import Record, Category
import requests
import os
from django.utils.timezone import now
from django.core.paginator import Paginator
from dotenv import load_dotenv

load_dotenv()

# Main view – dashboard/homepage
def home(request):

    # Fetch user records or return empty queryset
    if request.user.is_authenticated:
        records = Record.objects.filter(user=request.user).order_by('-created_at')
    else:
        records = Record.objects.none()
    
    # Filter records by category or date
    category_id = request.GET.get('category')
    date = request.GET.get('date')

    if category_id:
        records = records.filter(category_id=category_id)
    if date:
        records = records.filter(created_at__date=date)

    # Pagination
    paginator = Paginator(records, 10)
    page_number = request.GET.get('page')
    records = paginator.get_page(page_number)

    # Retrieve all categories
    categories = Category.objects.all()

    # Fetch news articles from NewsAPI
    news = []
    try:

        news_api = os.getenv('NEWS_API_KEY', 'demo_key')
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api}"
        response = requests.get(url)
        if response.status_code == 200:
            news_data = response.json()
            news = news_data.get('articles', [])
    except Exception as e:
        print(f"News fetch error: {e}")

    # Handle login form (if submitted on home page)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in.")
            return redirect('home')
        else:
            messages.error(request, "Login failed. Please try again.")
            return redirect('home')

    # Prepare reminders for incomplete tasks with a due date
    reminders = []
    if request.user.is_authenticated:
        for record in records:
            if record.reminder and record.reminder <= now() and not record.is_completed:
                reminders.append(record)

    # Pass context to template
    context = {
        'records': records,
        'categories': categories,
        'news': news,
        'reminders': reminders,
    }
    return render(request, 'home.html', context)

# Logout the current user
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

# Register a new user
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

# Display a single record's details
def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk, user=request.user)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('home')

# Delete a record
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk, user=request.user)
        delete_it.delete()
        messages.success(request, "Record deleted successfully.")
        return redirect('home')
    else:
        messages.error(request, "You must be logged in to perform this action.")
        return redirect('home')

# Add a new record
def add_record(request):
    form = RecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                record = form.save(commit=False)
                record.user = request.user
                record.save()
                messages.success(request, "Record added successfully.")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, "You must be logged in.")
        return redirect('home')

# Edit/update an existing record
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk, user=request.user)
        form = RecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully.")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.error(request, "You must be logged in.")
        return redirect('home')

# Mark a record as completed   
def complete_record(request, pk):
    if request.user.is_authenticated:
        try:
            record = Record.objects.get(id=pk, user=request.user)
            record.is_completed = True
            record.status_color = 'green'  
            record.save()
            messages.success(request, "Record marked as completed.")
            return redirect('home')
        except Record.DoesNotExist:
            messages.error(request, "Record not found.")
            return redirect('home')
    else:
        messages.error(request, "You must be logged in to perform this action.")
        return redirect('home')
