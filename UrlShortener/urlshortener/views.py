import random
import string

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import ShortURL
from .forms import CreateNewShortURL
from datetime import datetime


# Create your views here.
def home(request):
    return render(request, 'home.html')


def createShortURL(request):
    if request.method == 'POST':
        form = CreateNewShortURL(request.POST)
        if form.is_valid():
            original_link = form.cleaned_data['original_url']
            random_char_list = list(string.ascii_letters)
            random_char = ''.join(random.sample(random_char_list, 6))
            while len(ShortURL.objects.filter(short_url=random_char)) != 0:
                random_char = ''.join(random.sample(random_char_list, 6))
            now = datetime.now()
            url_form = ShortURL(original_url=original_link, short_url=random_char, date_created=now)
            url_form.save()
            return render(request, 'urlcreated.html', {'s_url': random_char})
    else:
        form = CreateNewShortURL()
        context = {'form': form}
        return render(request, 'create.html', context)


def redirect(request, url):
    current_object = ShortURL.objects.filter(short_url=url)
    if len(current_object) == 0:
        return render(request, 'pagenotfound.html')
    context = {'obj': current_object[0]}
    return render(request, 'redirect.html', context)
