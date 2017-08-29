from django.shortcuts import render
from django.http import HttpResponse
from salary import salary_sheet

# Create your views here.
def index(request):
    return render(request, "index.html")


def count_salary(request):
    dateFrom = request.session.get("date_from")
    dateTo = request.session.get("date_to")
    salary_out = salary_sheet(dateFrom, dateTo)
    
    
    