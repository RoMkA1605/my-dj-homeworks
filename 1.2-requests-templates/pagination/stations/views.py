import csv
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_rows = [row for row in reader]

    paginator = Paginator(all_rows, 10)

    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)