from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, View
from django.template import loader


# Create your views here.


class IndexView(generic.View):
    template_name = 'UI/index.html'

    def get(self, request):
        return render_to_response('UI/index.html', {'output': "OUTPUT"})
