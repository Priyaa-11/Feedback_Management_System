from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def post_login_redirect(request):
    """
    Redirects users after login based on their role.
    Superusers/Staff go to admin dashboard.
    Regular users go to student dashboard.
    """
    if request.user.is_staff:
        return redirect('admin_dashboard')  
    else:
        return redirect('student_dashboard') 