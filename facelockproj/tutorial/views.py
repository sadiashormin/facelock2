from django.shortcuts import redirect
#dgd
def login_redirect(request):
    return redirect('/account/login')
