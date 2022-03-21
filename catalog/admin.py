from django.contrib import admin

# Register your models here.

from .models import Autor, Gatunek, Ksiazka, Egzemplarz


admin.site.register(Gatunek)

class AutorAdmin(admin.ModelAdmin):
    list_display = ('imie', 'nazwisko', 'data_urodzenia', 'data_smierci')
    fields = ['imie', 'nazwisko', ('data_urodzenia', 'data_smierci'), 'zdiecie', 'zyciorys']

admin.site.register(Autor, AutorAdmin)



class EgzemplarzInLine(admin.TabularInline):
    model = Egzemplarz
    extra = 0

@admin.register(Ksiazka)
class KsiazkaAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'autor', 'gatunki')
    inlines = [EgzemplarzInLine]



@admin.register(Egzemplarz)
class EgzemplarzAdmin(admin.ModelAdmin):
    list_display = ('ksiazka', 'status', 'odbiorca', 'zwrot', 'id')
    list_filter = ('status', 'zwrot', 'odbiorca')

    fieldsets = (
    	(None, {
    		'fields': ('ksiazka', 'wydawca', 'id')
    		}),
    	('Dostępność', {
    		'fields': ('status', 'zwrot', 'odbiorca')
    		})
    )
