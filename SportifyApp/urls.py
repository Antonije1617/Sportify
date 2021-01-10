from django.urls import path
from .views import home, about, courses, register, profile, offerCourse, courseDetailView, booking
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', home, name='sportifyHome'),
    path('about/', about, name='sportifyAbout'),
    path('courses/', courses, name='sportifyCourses'),
    path('register/', register, name='sportifyRegister'),
    path('profile/', profile, name='sportifyProfile'),
    path('offer/', login_required(offerCourse.as_view()), name='sportifyOffer'),
    path('course/<int:pk>/', courseDetailView.as_view(), name='sportifyDetail'),
    path('booking/<int:pk>/', booking, name="sportifyBooking"),

]