from django.urls import path
from . import views
from django.urls import include, re_path

urlpatterns = [
	path('', views.index, name='index'),
	re_path(r'^ksiazki/$', views.KsiazkaListView.as_view(), name='ksiazki'),
	re_path(r'^ksiazka/(?P<pk>\d+)$', views.KsiazkaDetailView.as_view(), name='szczegoly_ksiazki'),
	re_path(r'^autorzy/$', views.AutorzyListView.as_view(), name='autorzy'),
	re_path(r'^autor/(?P<pk>\d+)$', views.AutorDetailView.as_view(), name='szczegoly_o_autorze'),
]

urlpatterns += [
    re_path(r'^pozyczone/$', views.LoanedBooksByUserListView.as_view(), name='pozyczone'),
    re_path(r'^wszystkie/$', views.LoanedBooksAllListView.as_view(), name='wszystkie')
]

urlpatterns += [
    re_path(r'^ksiazka/(?P<pk>[-\w]+)/renew/$', views.przedluzenie, name='przedluzenie'),
    re_path(r'^autor/dodanie_autora$', views.dodanie_autora, name='dodanie_autora'),
    re_path(r'^ksiazka/dodanie_ksiazki$', views.dodanie_ksiazki, name='dodanie_ksiazki'),
    re_path(r'^administrowanie$', views.administrowanie, name='administrowanie')
]