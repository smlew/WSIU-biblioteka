from django.shortcuts import render

# Create your views here.

from .models import Ksiazka, Autor, Egzemplarz, Gatunek
from django.views import generic
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
# from django.views.generic.edit import FormMixin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from django.http import HttpResponseRedirect
from django.urls import reverse

import datetime
from django import forms
from .forms import Przedluzenie, DodanieAutora, DodanieKsiazki
from django.db import models



from django.views.generic.edit import CreateView, UpdateView, DeleteView

def index(request):
    ilosc_ksiazek = Ksiazka.objects.all().count()
    ilosc_egzemplarzy = Egzemplarz.objects.all().count()
    ilosc_dostepnych_egzemplarzy = Egzemplarz.objects.filter(status__exact='d').count()
    ilosc_autorow = Autor.objects.count()
    ilosc_gatunkow = Gatunek.objects.count()


    context = {
        'ilosc_ksiazek': ilosc_ksiazek,
        'ilosc_egzemplarzy': ilosc_egzemplarzy,
        'ilosc_dostepnych_egzemplarzy': ilosc_dostepnych_egzemplarzy,
        'ilosc_autorow': ilosc_autorow,
        'ilosc_gatunkow': ilosc_gatunkow,
    }

    return render(request, 'index.html', context=context)

class KsiazkaListView(generic.ListView):
    model = Ksiazka
    template_name = 'catalog/lista_ksiazek.html'
    paginate_by = 10

class KsiazkaDetailView(generic.DetailView):
    model = Ksiazka
    template_name = 'catalog/szczegoly_ksiazki.html'
    
    def post(self, request, *args,**kwargs):
        if request.method == 'POST' :
            ksiazka = Ksiazka.objects.get(pk=self.kwargs.get('pk'))
            
            print(ksiazka.obraz)

            wybor_wydawcy = request.POST.get('wybor_wydawcy')
            
            egzem = Egzemplarz.objects.get(id=wybor_wydawcy)
            uzytk = request.user

            if uzytk.egzemplarz_set.count() < 3:

                if egzem.status == 'z' and egzem.odbiorca == uzytk:
                    egzem.status = 'd'
                    egzem.odbiorca = None
                        
                elif egzem.status == 'd':
                    egzem.status = 'z'
                    egzem.odbiorca = uzytk
                
            egzem.save()
        return render(request, self.template_name, context={'ksiazka': ksiazka})

class AutorzyListView(generic.ListView):
    model = Autor
    template_name = 'catalog/lista_autorow.html'

class AutorDetailView(generic.DetailView):
    model = Autor
    template_name = 'catalog/szczegoly_o_autorze.html'

class RedirectLogin(LoginRequiredMixin, generic.View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = Egzemplarz
    template_name = 'catalog/lista_pozyczonych_egzemplarzy.html'
    paginate_by = 10

    def get_queryset(self):
        return Egzemplarz.objects.filter(odbiorca=self.request.user).filter(status__exact='w').order_by('zwrot')

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = Egzemplarz
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/lista_wszystkich_pozyczonych_egzemplarzy.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Egzemplarz.objects.filter(status__exact='w').order_by('zwrot')


@permission_required('catalog.can_mark_returned')
def dodanie_autora(request):
    if request.method == 'POST':
        form = DodanieAutora(request.POST)

        if form.is_valid():
            autor = Autor(imie=form.cleaned_data['imie'], nazwisko=form.cleaned_data['nazwisko'])
            autor.save()

            return HttpResponseRedirect(reverse('index'))
    else: form = DodanieAutora()

    return render(request, 'catalog/autor_form.html', {'form': form})


def dodanie_ksiazki(request):
    model = Autor.objects.all()

    if request.method == 'POST':
        form = DodanieKsiazki(request.POST)

        wybor_autora = request.POST.get('wybor_autora')
        autor = Autor.objects.get(id=wybor_autora)

        print(autor)

        if form.is_valid():
            ksiazka = Ksiazka(tytul=form.cleaned_data['tytul'], isbn=form.cleaned_data['isbn'], autor=autor)
            ksiazka.save()

    else: form = DodanieKsiazki()
    return render(request, 'catalog/ksiazka_form.html', {'form': form, 'lista_autorow': model})

def administrowanie(request):

    return render(request, 'catalog/administrowanie.html')

def przedluzenie(request, pk):
    egzempl = get_object_or_404(Egzemplarz, pk=pk)

    if request.method == 'POST':

        form = Przedluzenie(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():

            egzempl.zwrot = form.cleaned_data['odswiezona_data']
            egzempl.save()

            return HttpResponseRedirect(reverse('wszystkie') )

    else:
        proponowana_odswiezona_data = datetime.date.today() + datetime.timedelta(weeks=3)
        form = Przedluzenie(initial={'odswiezona_data': proponowana_odswiezona_data,})

    return render(request, 'catalog/przedluzenie.html', {'form': form, 'egzempl':egzempl})
