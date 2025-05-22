import json
from datetime import datetime

from django.views import View
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.cache import cache

from .models import *
from .utils import *

def calculi_page_view(request, link):
    obj = get_object_or_404(Calculi, link=link, is_active=True)
    category = obj.category
    random_related = Calculi.objects.filter(
    category=category,
    is_active=True
    ).exclude(id=obj.id).order_by('?')[:4]
    return render(request, f"calculi/{obj.html}.html", {'calculi': obj, 'relatedLinks':random_related})

@require_POST
@login_required
def like_calculi(request):
    calculink = request.POST.get('calculink')
    action = request.POST.get('action')
    
    if calculink and action:
        try:
            calculi = Calculi.objects.get(link=calculink)
            if action == 'like':
                CaLike.objects.get_or_create(user=request.user, calculi=calculi)
            else:
                CaLike.objects.filter(user=request.user, calculi=calculi).delete()
            
            # Update denormalized count
            calculi.update_like_count()
            
            return JsonResponse({
                'status': 'ok',
                # 'total_likes': calculi.like_count,
                'is_liked': action == 'like',
            })
        except Calculi.DoesNotExist:
            pass
    
    return JsonResponse({'status': 'error'}, status=400)

class CalculusListView(ListView):
    model=CalCate
    template_name="calculi/calculus_list.html"

class CalcCateDetailView(DetailView):
    model=CalCate
    template_name="calculi/calcate_list.html"
    context_object_name = 'category'
    slug_url_kwarg = 'link'
    context_object_name = 'category'
    
    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(CalCate, link=slug)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calculus'] = Calculi.objects.filter(category=self.object)
        context['category'] = self.object
        return context

@login_required
def favorite_calculus(request):
    liked_calculus = request.user.liked_calculus.all().order_by('-date_created')
    
    context = {
        'liked_calculus': liked_calculus,
    }
    return render(request, 'calculi/fave_list.html', context)


class CalculateWeightZScoreView(View):
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        api_name = "CalculateWeightZScore"
        ip_address = request.META.get("REMOTE_ADDR")
        try:
            gender = request.GET.get('gender')
            age_months = float(request.GET.get('age_months'))
            X = float(request.GET.get('weight'))
        except Exception as e:
            CaLog.objects.create(
                user=user, api_name=api_name, status=500, error_data=str(e), ip_address=ip_address
            )
            return JsonResponse({"error": str(e)}, status=500)

        if gender not in ['1', '2']:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"G: {gender}", status=400, error_data="Gender is other than M or F.", ip_address=ip_address)
            return JsonResponse({'error': 'Choose Male or Female as a gender.'}, status=400)

        if X < 0.5 or X > 300:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"Weight: {X}", output="", status=400, error_data="Not a valid weight.", ip_address=ip_address
            )
            return JsonResponse({'error': 'This weight is not valid for a kid.'}, status=400)
        if age_months%0.5!=0:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"Age: {age_months}", output="", status=400, error_data="Not a valid decimal for month.", ip_address=ip_address)
            return JsonResponse({'error': 'The only acceptable decimal for Months is 5.'}, status=400)
        if age_months>240:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"Age: {age_months}", output="", status=400, error_data="Not a valid age.", ip_address=ip_address)
            return JsonResponse({'error': "This calculator doesn't work for those who are older than 20 years."}, status=400)
        
        try:
            result = find_LMS(X, weight_data, gender, age_months)
            result_content= json.loads(result.content)
            CaLog.objects.create(
                user=user,
                api_name=api_name,
                input_data=f"Weight: {X}, G: {gender}, Age: {age_months}",
                output=result_content.get("z_score"),
                status=200,
                ip_address=ip_address
            )
            if not user:
                cache_key = f"api_calls_{api_name}_{ip_address}_{datetime.today().date()}"
                api_calls = cache.get(cache_key, 0)
                if api_calls >= 5:
                    CaLog.objects.create(
                    user=user, api_name=api_name, input_data="", output="", status=429, error_data="Limit exceeded.", ip_address=ip_address
                    )
                    return JsonResponse({"error": "Limit exceeded. Please sign up or log in."}, status=429)
                cache.set(cache_key, api_calls + 1, 86400)
            return result
        except Exception as e:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data="", output="", status=500, error_data=str(e), ip_address=ip_address
            )
            return JsonResponse({"error": str(e)[:100]}, status=500)

class CalculateLengthZScoreView(View):
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        api_name = "CalculateLengthZScore"
        ip_address = request.META.get("REMOTE_ADDR")
        try:
            gender = request.GET.get('gender')
            age_months = float(request.GET.get('age_months'))
            X = float(request.GET.get('length'))
        except Exception as e:
            CaLog.objects.create(
                user=user, api_name=api_name, status=500, error_data=str(e), ip_address=ip_address
            )
            return JsonResponse({"error": str(e)}, status=500)

        if gender not in ['1', '2']:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"G: {gender}", status=400, error_data="Gender is other than M or F.", ip_address=ip_address)
            return JsonResponse({'error': 'Choose Male or Female as a gender.'}, status=400)
        if X < 30 or X > 250:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"Length: {X}", output="", status=400, error_data="Not a valid length.", ip_address=ip_address)
            return JsonResponse({'error': 'This length is not valid for a kid. Please check if you have entered the length in centimeters (cm).'}, status=400)
        if age_months%0.5!=0:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"Age: {age_months}", output="", status=400, error_data="Not a valid decimal for month.", ip_address=ip_address)
            return JsonResponse({'error': 'The only acceptable decimal for Months is 5.'}, status=400)
        if age_months>240:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"Age: {age_months}", output="", status=400, error_data="Not a valid age.", ip_address=ip_address)
            return JsonResponse({'error': "This calculator doesn't work for those who are older than 20 years."}, status=400)

        try:
            result = find_LMS(X, length_data, gender, age_months)
            result_content= json.loads(result.content)
            CaLog.objects.create(
                user=user,
                api_name=api_name,
                input_data=f"Length: {X}, G: {gender}, Age: {age_months}",
                output=result_content.get("z_score"),
                status=200,
                ip_address=ip_address
            )
            if not user:
                cache_key = f"api_calls_{api_name}_{ip_address}_{datetime.today().date()}"
                api_calls = cache.get(cache_key, 0)
                if api_calls >= 5:
                    CaLog.objects.create(
                    user=user, api_name=api_name, input_data="", output="", status=429, error_data="Limit exceeded.", ip_address=ip_address
                    )
                    return JsonResponse({"error": "Limit exceeded. Please sign up or log in."}, status=429)
                cache.set(cache_key, api_calls + 1, 86400)
            return result
        except Exception as e:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data="", output="", status=500, error_data=str(e), ip_address=ip_address
            )
            return JsonResponse({"error": str(e)[:100]}, status=500)

class CalculateHCZScoreView(View):
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        api_name = "CalculateHCZScore"
        ip_address = request.META.get("REMOTE_ADDR")
        try:
            gender = request.GET.get('gender')
            age_months = float(request.GET.get('age_months'))
            hc = float(request.GET.get('hc'))
        except Exception as e:
            CaLog.objects.create(
                user=user, api_name=api_name, status=500, error_data=str(e), ip_address=ip_address
            )
            return JsonResponse({"error": str(e)}, status=500)

        if gender not in ['1', '2']:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"G: {gender}", status=400, error_data="Gender is other than M or F.", ip_address=ip_address)
            return JsonResponse({'error': 'Choose Male or Female as a gender.'}, status=400)
        if hc < 20 or hc > 70:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"HC: {hc}", output="", status=400, error_data="Not a valid head circumference.", ip_address=ip_address)
            return JsonResponse({'error': 'This head circumference is not valid for a kid. Please check if you have entered the value in centimeters (cm).'}, status=400)
        if age_months%0.5!=0:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"Age: {age_months}", output="", status=400, error_data="Not a valid decimal for month.", ip_address=ip_address)
            return JsonResponse({'error': 'The only acceptable decimal for Months is 5.'}, status=400)
        if age_months>36:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"Age: {age_months}", output="", status=400, error_data="Not a valid age.", ip_address=ip_address)
            return JsonResponse({'error': "This calculator doesn't work for those who are older than 3 years."}, status=400)
        try:
        
            result = find_LMS(hc, head_circumference_data, gender, age_months)
            result_content= json.loads(result.content)
            CaLog.objects.create(
                user=user,
                api_name=api_name,
                input_data=f"Length: {hc}, G: {gender}, Age: {age_months}",
                output=result_content.get("z_score"),
                status=200,
                ip_address=ip_address
            )
            if not user:
                cache_key = f"api_calls_{api_name}_{ip_address}_{datetime.today().date()}"
                api_calls = cache.get(cache_key, 0)
                if api_calls >= 5:
                    CaLog.objects.create(
                    user=user, api_name=api_name, input_data="", output="", status=429, error_data="Limit exceeded.", ip_address=ip_address
                    )
                    return JsonResponse({"error": "Limit exceeded. Please sign up or log in."}, status=429)
                cache.set(cache_key, api_calls + 1, 86400)
            return result
        except Exception as e:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data="", output="", status=500, error_data=str(e), ip_address=ip_address
            )
            return JsonResponse({"error": str(e)[:100]}, status=500)
    
class CalculateBMIZScoreView(View):
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        api_name = "CalculateBMIZScore"
        ip_address = request.META.get("REMOTE_ADDR")
        try:
            gender = request.GET.get('gender')
            age_months = float(request.GET.get('age_months'))
            length = float(request.GET.get('length'))
            weight = float(request.GET.get('weight'))
        except Exception as e:
            CaLog.objects.create(
                user=user, api_name=api_name, status=500, error_data=str(e), ip_address=ip_address)
            return JsonResponse({"error": str(e)}, status=500)

        if gender not in ['1', '2']:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"G: {gender}", status=400, error_data="Gender is other than M or F.", ip_address=ip_address)
            return JsonResponse({'error': 'Choose Male or Female as a gender.'}, status=400)
        if length < 30 or length > 250:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"Length: {length}", output="", status=400, error_data="Not a valid length.", ip_address=ip_address)
            return JsonResponse({'error': 'This length is not valid for a kid. Please check if you have entered the length in centimeters (cm).'}, status=400)
        if weight < 0.5 or weight > 300:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"Age: {age_months}", output="", status=400, error_data="Not a valid decimal for month.", ip_address=ip_address)
            return JsonResponse({'error': 'This weight is not valid for a kid. Please check if you have entered the weight in kilograms (kg).'}, status=400)
        if age_months%0.5!=0:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"Age: {age_months}", output="", status=400, error_data="Not a valid decimal for month.", ip_address=ip_address)
            return JsonResponse({'error': 'The only acceptable decimal for Months is 5.'}, status=400)
        if age_months>240.5:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"Age: {age_months}", output="", status=400, error_data="Not a valid age.", ip_address=ip_address)
            return JsonResponse({'error': "This calculator doesn't work for those who are older than 20 years."}, status=400)
        elif  age_months < 24:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data=f"Age: {age_months}", output="", status=400, error_data="Not a valid age.", ip_address=ip_address)
            return JsonResponse({'error': "This calculator doesn't work for those who are younger than 2 years."}, status=400)

        bmi=round(((weight)/((length/100)**2)), 2)
        try:
            result = find_LMS(bmi, bmi_data, gender, age_months)
            result_content= json.loads(result.content)
            CaLog.objects.create(
                user=user,
                api_name=api_name,
                input_data=f"BMI: {bmi}, G: {gender}, Age: {age_months}",
                output=result_content.get("z_score"),
                status=200,
                ip_address=ip_address
            )
            if not user:
                cache_key = f"api_calls_{api_name}_{ip_address}_{datetime.today().date()}"
                api_calls = cache.get(cache_key, 0)
                if api_calls >= 5:
                    CaLog.objects.create(
                    user=user, api_name=api_name, input_data="", output="", status=429, error_data="Limit exceeded.", ip_address=ip_address
                    )
                    return JsonResponse({"error": "Limit exceeded. Please sign up or log in."}, status=429)
                cache.set(cache_key, api_calls + 1, 86400)
            return result
        except Exception as e:
            CaLog.objects.create(
                user=user, api_name=api_name, input_data="", output="", status=500, error_data=str(e), ip_address=ip_address
            )
            return JsonResponse({"error": str(e)[:100]}, status=500)

    
class CalculateAllZScoresView(View):
    def get(self, request):
        # user = request.user if request.user.is_authenticated else None
        # api_name = "CalculateAllZScores"
        # ip_address = request.META.get("REMOTE_ADDR")
        try:
            gender = request.GET.get('gender')
            age_months = float(request.GET.get('age_months'))
            weight = float(request.GET.get('weight'))
            height = float(request.GET.get('height'))
            hc = float(request.GET.get('hc'))

        except Exception as e:
            # CaLog.objects.create(
            #     user=user, api_name=api_name, status=500, error_data=str(e), ip_address=ip_address)
            return JsonResponse({"error": str(e)}, status=500)

        if gender not in ['1', '2']:
            # CaLog.objects.create(
            #     user=user, api_name=api_name, input_data=f"G: {gender}", status=400, error_data="Gender is other than M or F.", ip_address=ip_address)
            return JsonResponse({'error': 'Choose Boy or Girl as a gender.'}, status=400)
        if height < 30 or height > 250:
            # CaLog.objects.create(
            #     user=user, api_name=api_name, input_data=f"Height: {height}", output="", status=400, error_data="Not a valid height.", ip_address=ip_address)
            return JsonResponse({'error': 'This height is not valid for a kid. Please check if you have entered the height in centimeters (cm).'}, status=400)
        if weight < 0.5 or weight > 300:
            # CaLog.objects.create(
            #     user=user, api_name=api_name, input_data=f"Age: {age_months}", output="", status=400, error_data="Not a valid decimal for month.", ip_address=ip_address)
            return JsonResponse({'error': 'This weight is not valid for a kid. Please check if you have entered the weight in kilograms (kg).'}, status=400)
        if age_months%0.5!=0:
            # CaLog.objects.create(
            #     user=user, api_name=api_name, input_data=f"Age: {age_months}", output="", status=400, error_data="Not a valid decimal for month.", ip_address=ip_address)
            return JsonResponse({'error': 'The only acceptable decimal for Months is 5.'}, status=400)
        if age_months>240.5:
            # CaLog.objects.create(
            #     user=user, api_name=api_name, input_data=f"Age: {age_months}", output="", status=400, error_data="Not a valid age.", ip_address=ip_address)
            return JsonResponse({'error': "This calculator doesn't work for those who are older than 20 years."}, status=400)
        elif  age_months < 24:
            # CaLog.objects.create(
            #     user=user, api_name=api_name, input_data=f"Age: {age_months}", output="", status=400, error_data="Not a valid age.", ip_address=ip_address)
            return JsonResponse({'error': "This calculator doesn't work for those who are younger than 2 years."}, status=400)

        # bmi=round(((weight)/((height/100)**2)), 2)

        try:
            result = find_LMS_whole(weight, height, hc, gender, age_months)
            result_content= json.loads(result.content)
            # CaLog.objects.create(
            #     user=user,
            #     api_name=api_name,
            #     input_data=f"BMI: {bmi}, G: {gender}, Age: {age_months}",
            #     output=result_content.get("weight"),
            #     status=200,
            #     ip_address=ip_address
            # )
            # if not user:
            #     cache_key = f"api_calls_{api_name}_{ip_address}_{datetime.today().date()}"
            #     api_calls = cache.get(cache_key, 0)
            #     if api_calls >= 5:
            #         # CaLog.objects.create(
            #         # user=user, api_name=api_name, input_data="", output="", status=429, error_data="Limit exceeded.", ip_address=ip_address
            #         # )
            #         return JsonResponse({"error": "Limit exceeded. Please sign up or log in."}, status=429)
            #     cache.set(cache_key, api_calls + 1, 86400)
            return result
        except Exception as e:
            # CaLog.objects.create(
            #     user=user, api_name=api_name, input_data="", output="", status=500, error_data=str(e), ip_address=ip_address
            # )
            return JsonResponse({"error": str(e)[:100]}, status=500)

    
