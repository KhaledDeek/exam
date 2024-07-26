from django.urls import path
from . import views

urlpatterns = [
    path('' , views.main),
    path('dashboard' , views.pies),
    path('login' , views.validate_login),
    path('register' , views.register),
    path('create_pie' , views.create_pie),
    path('pies/edit/<int:id>' , views.edit_pie),
    path('update_pie/<int:id>' , views.update_pie),
    path('pies' , views.all_pies),
    path('pies/<int:id>' , views.info),
    path('logout' , views.logout),
    path('pies/delete/<int:id>' , views.delete_pie),
    path('voteplus/<int:id>' , views.voteplus),
    path('voteminus/<int:id>' , views.voteminus),
    path('remove_vote/<int:id>' , views.remove_vote)
]