from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from functools import wraps
from accounts.models import StudentProfile, ProfessorProfile

def student_profile_state(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            # Checks if Student Profile object exists:
            profile = request.user.student_profile

            if not profile.completed:
                ## Makes the user to complete:
                # return redirect('')
                return redirect('new_user_profile')
                pass
            
            elif not profile.verified:
                return redirect('profile_verification_pending')
        
        except StudentProfile.DoesNotExist:
            # Makes the user to make one:
            if request.user.university in ['MUMS']:
                # Show add profile page.
                return redirect('new_user_profile')
            else:
                raise Http404("Your university is not registered in the project")

        
        return view_func(request, *args, **kwargs)
    return _wrapped_view