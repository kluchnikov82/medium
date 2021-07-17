from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
import random
from .models import Medium
from accounts.models import AppUser
from accounts.forms import CheckoutContactForm



def GetGuess(request):
    user = AppUser.objects.get(username=request.user)

    # Сравнение текущей суссии с сессией пользователя
    if request.session.session_key != user.session:
        user.number.clear()

    # Сохранение сессии в модели пользователя
    user.session = request.session.session_key
    user.save()

    # Получение массива введеных пользователем положительных, целых чисел для вывода
    numbers = user.number

    # Получение массива догадок экстрасенсов для вывода
    mediums = Medium.objects.all().order_by('-created')[0:2]
    guess1 = Medium.objects.filter(name='Экстрасенс №1').order_by('-created').values_list('guess', flat=True)
    guess2 = Medium.objects.filter(name='Экстрасенс №2').order_by('-created').values_list('guess', flat=True)

    return render(request, 'page1/index.html', locals())


def GetGuessesMedium(request):
    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if form.is_valid():
            print("yes")
            data = request.POST

            # Получение введеного пользователем положительного, целого числа
            number = data.get("number")

            # Сохранение введеного пользователем положительного, целого числа в БД
            user = AppUser.objects.get(username=request.user.username)
            user.number.append(number)
            user.save()

            # Получение объектов Экстрасенс для сравнения в последующем цикле их догадок с введенным числом пользователя
            mediums = Medium.objects.all().order_by('-created')[0:2]

            for medium in mediums:
                if str(medium.guess) == str(number):
                    # Увеличение уровня мастрества экстрасенса при совпадении с введеным числом пользователя
                    medium.level += 1
                else:
                    # Уменьшение уровня мастрества экстрасенса при совпадении с введеным числом пользователя
                    medium.level -= 1
                medium.save()
            return HttpResponseRedirect('guess')

    else:
        Medium.name = "Экстрасенс №1"
        Medium.guess = random.randint(1, 99)  # Генерация рэндомной догадки для Экстрасенс №1
        guess1 = Medium.guess

        try:
            user = AppUser.objects.get(username=request.user.username)

            # Получение уровня мастрества предыдущей записи для экстрасенса. Для корректного ведения учета уровня
            # мастрества для последующих записей в БД
            level = Medium.objects.filter(name='Экстрасенс №1').order_by('-created')[0].level
        except Exception as e:
            level = 0
        medium = Medium.objects.create(name=Medium.name, guess=Medium.guess, level=level)

        user = AppUser.objects.get(username=request.user.username)
        user.medium.clear()

        # Добавление связи для текущего пользователя с объетом Экстрасенс №1
        user.medium.add(medium)

        Medium.name = "Экстрасенс №2"
        Medium.guess = random.randint(1, 99) # Генерация рэндомной догадки для Экстрасенс №2
        guess2 = Medium.guess

        try:
            user = AppUser.objects.get(username=request.user.username)
            level = Medium.objects.filter(name='Экстрасенс №2').order_by('-created')[0].level
        except Exception as e:
            level = 0
        medium = Medium.objects.create(name=Medium.name, guess=Medium.guess, level=level)

        # Добавление связи для текущего пользователя с объетом Экстрасенс №1
        user.medium.add(medium)
        form = CheckoutContactForm()

    return render(request, 'page2/index.html', locals())