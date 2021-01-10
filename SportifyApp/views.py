from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'aboutUs.html', {'title': 'About'})

def courses(request):
    context = {
        'courses': Course.objects.all().order_by('-date_posted'),
    }
    return render(request, 'courses.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if "stud.fh-campuswien.ac.at" in email:
                form.save()
                messages.success(request, f'Hello {username}. Your account has been created! You are now able to log in!')
                return redirect('sportifyLogin')
            else:
                messages.error(request, f'You must have stud.fh-campuswien.ac.at in your email')
                return redirect('sportifyRegister')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('sportifyProfile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'courses': Course.objects.all().order_by('-date_posted'),
    }

    return render(request, 'profile.html', context)
#decorators are adding functionalities to an existing function

class courseDetailView(DetailView):
    model = Course
    template_name = 'courseDetail.html'

class offerCourse(CreateView):
    model = Course
    template_name = "offerCourse.html"
    fields = ['sport', 'description', 'places']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def booking(request, pk):
    course = get_object_or_404(Course, id=request.POST.get('course_id'))
    course.bookings.add(request.user)
    return redirect('sportifyCourses')