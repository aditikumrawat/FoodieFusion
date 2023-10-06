from django.shortcuts import render, redirect


def vprofile(request):
    return render(request, 'vendor/vprofile.html')

