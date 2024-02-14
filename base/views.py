from django.shortcuts import render

def custom_error_400(request, exception):
    print(exception)
    return render(request, 'errors/400.html', {})

def custom_error_403(request, exception):
    print(exception)
    return render(request, 'errors/403.html', {})
    
def custom_error_404(request, exception):
    print(exception)
    return render(request, 'errors/404.html', {})

def custom_error_500(request, exception):
    print(exception)
    return render(request, 'errors/500.html', {})