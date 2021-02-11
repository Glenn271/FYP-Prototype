from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from . import models
from django.contrib.gis.geos import Point


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def update_location(request):
    try:
        print('in update location')
        user = request.user
        print(user)
        user_profile = models.Profile.objects.get(user__username=user)
        print(user_profile)
        if not user_profile:
            raise ValueError("Can't get User details")

        print('user_profile')
        print(user_profile)

        point = request.POST["point"].split(",")
        point = [float(part) for part in point]
        point = Point(point, srid=4326)

        print('point')
        print(point)

        user_profile.last_location = point
        user_profile.save()

        return JsonResponse({"message": f"Set location to {point.wkt})."}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)
