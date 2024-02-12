from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import DeliveryRegistrationRequests

@staff_member_required
def approve_requests(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        status = request.POST.get('status')
        feedback = request.POST.get('feedback')