from django.http import HttpResponseRedirect
from django.shortcuts import render
import random
from .models import Medium, History
from .forms import CheckoutContactForm
# Create your views here.


def GetGuess(request):
    history = History.objects.all()
    mediums = Medium.objects.order_by("-id")[:2]
    return render(request, 'page1/index.html', locals())

def GetGuessesMedium(request):
    Medium.name = "Экстрасенс №1"
    Medium.guess1 = random.randint(1, 99)
    Medium.guess2 = random.randint(1, 99)

    try:
        element = Medium.objects.order_by("-id")[:1]
        level = element[0].level
    except Exception as e:
        level = 0
    Medium.objects.create(name=Medium.name, guess1=Medium.guess1, guess2=Medium.guess2, level=level)

    Medium.name = "Экстрасенс №2"
    Medium.guess1 = random.randint(1, 99)
    Medium.guess2 = random.randint(1, 99)
    element = Medium.objects.order_by("-id")[:2]
    level = element[0].level
    Medium.objects.create(name=Medium.name, guess1=Medium.guess1, guess2=Medium.guess2, level=level)

    mediums = Medium.objects.order_by("-id")[:2]

    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if form.is_valid():
            print("yes")
            data = request.POST
            number = data.get("number")

            History.number = number
            History.objects.create(number=History.number)

            mediums = Medium.objects.order_by("-id")[:2]
            for element in mediums:
                if element.guess1 == number or element.guess2 == number:
                    element.level += 1
                else:
                    element.level -= 1
                element.save()
            return HttpResponseRedirect('guess')

    else:
        form = CheckoutContactForm()
    return render(request, 'page2/index.html', locals())