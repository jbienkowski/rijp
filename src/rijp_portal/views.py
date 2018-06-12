from django.shortcuts import render
from django.views.generic import ListView, DetailView

# Create your views here.
class IndexListView(ListView):
    model = None
    context_object_name = 'ctx'
    template_name = 'base.html'

    def get_queryset(self):
        return None