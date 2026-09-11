from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm


# Create your views here.
def list_notes(request):
    notes = Note.objects.all()

    context = {
        'notes': notes,
        'page_title': 'Sticky Notes',
    }

    return render(request, 'notes/list.html', context)


def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            return redirect('list_notes')
    else:
        form = NoteForm()
    return render(request, 'notes/form.html', {'form': form})


def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('list_notes')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/form.html', {'form': form})


def delete_note(request, pk):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=pk)
        note.delete()
    return redirect('list_notes')
