from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


class Przedluzenie(forms.Form):
    odswiezona_data = forms.DateField(help_text="Wpisz datę pomiędzy teraz i 4 tygodni do przodu")

    def formatowanie(self):
        data = self.cleaned_data['odswiezona_data']

        if data < datetime.date.today():
            raise ValidationError(_('Zła data - nie wolno zmienić na przyszłą datę'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Zła data - przedłużenie więcej niż na 4 tygodnie'))

        return data

class DodanieAutora(forms.Form):
    imie = forms.CharField(help_text="Wpisz imię autora")
    nazwisko = forms.CharField(help_text="Wpisz nazwisko autora")

    def formatowanie(self):
        dane = self.cleaned_data
        return imie, nazwisko

class DodanieKsiazki(forms.Form):
    tytul = forms.CharField(help_text="Wpisz tytuł")
    isbn = forms.CharField(help_text="Wpisz numer ISBN")
    def formatowanie(self):
        dane = self.cleaned_data
        return dane