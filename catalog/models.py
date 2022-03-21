from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Gatunek(models.Model):
    nazwa = models.CharField(max_length=127, help_text="Wpisz gatunek książki")

    def __str__(self):
        return self.nazwa

class Ksiazka(models.Model):
    tytul = models.CharField(max_length=127)
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
    opis = models.TextField(max_length=4095, help_text="Wpisz krótki opis książki", blank=True)
    isbn = models.CharField('ISBN',max_length=13, help_text='<a href="https://www.isbn-international.org">Numer ISBN</a>')
    gatunek = models.ManyToManyField(Gatunek, help_text="Wybierz gatunek książki")
    obraz = models.CharField(max_length=255, null=True, blank=True, help_text="Wpisz link do obrazu")

    def __str__(self):
        return self.tytul

    def get_absolute_url(self):
        return reverse('szczegoly_ksiazki', args=[str(self.id)])

    def gatunki(self):
        return ', '.join([ gatunek.nazwa for gatunek in self.gatunek.all()[:3] ])
    gatunki.skrot = 'Gatunek'

class Egzemplarz(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unikalny ID dla konkretnego egzemplarza książki")
    ksiazka = models.ForeignKey('Ksiazka', on_delete=models.SET_NULL, null=True)
    wydawca = models.CharField(max_length=127)
    zwrot = models.DateField(null=True, blank=True)
    odbiorca = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    STATUS = (('k', 'Konserwacja'), ('w', 'Wypożyczona'), ('d', 'Dostępna'), ('z', 'Zarezerwowana'),)
 
    status = models.CharField(max_length=1, choices=STATUS, blank=True, default='k', help_text='Dostępność książki')

    class Meta:
        ordering = ["zwrot"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    @property
    def zalegly(self):
        if self.zwrot and date.today() > self.zwrot:
            return True
        return False


    def __str__(self):
        return '%s (%s)' % (self.id,self.ksiazka.tytul)

class Autor(models.Model):
    imie = models.CharField(max_length=127)
    nazwisko = models.CharField(max_length=127)
    data_urodzenia = models.DateField(null=True, blank=True)
    data_smierci = models.DateField(null=True, blank=True)
    zdiecie = models.CharField(max_length=255, null=True, blank=True, help_text="Wpisz link do zdięcia")
    zyciorys = models.TextField(max_length=2047, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('szczegoly_o_autorze', args=[str(self.id)])


    def __str__(self):
        return '%s, %s' % (self.nazwisko, self.imie)
