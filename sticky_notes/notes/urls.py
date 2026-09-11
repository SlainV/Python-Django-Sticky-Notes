from django.urls import path
from .views import (
    create_note,
    edit_note,
    delete_note,
    list_notes,
)

urlpatterns = [
    path('', list_notes, name='list_notes'),
    path('notes/create/', create_note, name='create_note'),
    path('notes/<int:pk>/edit/', edit_note, name='edit_note'),
    path('notes/<int:pk>/delete/', delete_note, name='delete_note'),
]
