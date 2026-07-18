from django.shortcuts import render


def home(request):
    """Render the application home page."""
    return render(request, "home.html")
