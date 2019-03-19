from urllib.parse import urlparse

from django.urls import resolve
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.files.storage import default_storage

from django.views import generic

from .forms import UploadFileForm
from .service import generate_visjs_graph
from .models import Service



@login_required
def security(request, service_id):

    service = Service.objects.get(id=service_id, owner_id=request.user.id)

    nodes, edges, all_edges = generate_visjs_graph(default_storage.open(service.service_file))

    basic_policies = service.securitypolicy_set.filter(policy_sla='B')
    pro_policies = service.securitypolicy_set.filter(policy_sla='P')
    unlimited_policies = service.securitypolicy_set.filter(policy_sla='U')

    return render(request, 'dashboard/security.html',
                  {'nodes': nodes,
                   'edges': edges,
                   'all_edges': all_edges,
                   'service': service,
                   'basic_policies': basic_policies,
                   'pro_policies': pro_policies,
                   'unlimited_policies': unlimited_policies})


@login_required
def services(request):

    service_list = Service.objects.filter(owner_id=request.user.id)

    return render(request, 'dashboard/services.html',
                  {'service_list': service_list})


@login_required
def slas(request):

    return render(request, 'dashboard/slas.html')


@login_required
def index(request):
    # form = UploadFileForm()
    # with open('/home/benjamin/code/astrid/dashboard/test/docker-compose.yml') as f:
    #     nodes, edges = generate_visjs_graph(f)
    nodes, edges = dict(), dict()
    return render(request, 'dashboard/index.html',
                  {"nodes": nodes, "edges": edges})


@login_required
def logout(request):
    django_logout(request)

    return redirect('dashboard:login')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next = request.POST['next']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            try:
                resolve(urlparse(next))
            except Http404:
                return redirect('dashboard:index')

        return redirect(next)

    next = request.GET['next'] if 'next' in request.GET else None
    return render(request, 'dashboard/login.html', {'next': next})
