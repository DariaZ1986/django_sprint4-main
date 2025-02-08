from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:profile', username=user.username)
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})
