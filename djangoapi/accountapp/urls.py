from django.urls import path,include

from accountapp.views import hello_world, hello_world_drf, TextEntryView

urlpatterns = [
    path('hello_world/', hello_world),
    path('hello_world_drf/', hello_world_drf),
    path('text-entry/',TextEntryView.as_view())
]