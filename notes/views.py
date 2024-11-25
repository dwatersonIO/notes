from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q

from .models import Note, Tag
from .forms import NoteForm, NoteSearchForm, TagForm

def index(request):
	notes = Note.objects.prefetch_related("tags").order_by('-date_created') # order_by not needed since order in Model Meta field
	# Better than Note.objects.all() since avoids n+1 problem. ie template issuing multiple sql queries to find the many-to-many queries
	# If the relationship is one to many then use "select_related." "prefetch_related" used on many to many relationships.
 
 
	context = {'notes':notes}
	return render(request, 'notes/index.html', context)


def detail_note(request, pk):
	note = Note.objects.get(id=pk)

	if request.method == 'POST':
		form = NoteForm(request.POST, instance=note)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form = NoteForm() # GET Request returns empty form

	context = {'note': note, 'form':form}
	return render(request, 'notes/detail_note.html', context)

def create_note(request):

	form = NoteForm()
	tags = Tag.objects.all()
	if request.method =='POST':
		form = NoteForm(request.POST)
		print (form)
		if form.is_valid():
			form.save()
		return redirect('/')

	context = {'form':form,'tags':tags}
	return render(request, 'notes/create_note.html', context)

def update_note(request, pk):
	note = Note.objects.get(id=pk)

	if request.method == 'POST':
		form = NoteForm(request.POST, instance=note)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form = NoteForm(instance=note) # if Get request just show current data

	context = {'form':form}
	return render(request, 'notes/update_note.html', context)

def delete_note(request, pk):
	note = Note.objects.get(id=pk)

	if request.method == 'POST':
		note.delete()
		return redirect('/')

	context = {'note':note}
	return render(request, 'notes/delete_note.html', context)



def search_note(request):
    # Always use GET for search forms
    form = NoteSearchForm(request.GET or None)
    notes = Note.objects.all()  # Start with all notes
    print (request.GET)

    if form.is_valid():
        # Get the search text and tags from the form
        search_text = form.cleaned_data.get('search_text')
        search_tags = form.cleaned_data.get('search_tags')
        
        # Filter notes by search_text if provided
        if search_text:
            notes = notes.filter(Q(text__icontains=search_text) | Q(summary__icontains=search_text))
        
        # Filter notes by tags if tags are provided
        if search_tags:
            notes = notes.filter(tags__in=search_tags).distinct()
            form.search_text=""

    else:
        notes = Note.objects.all().order_by('-date_created')

    context = {
        'form': form,
        'notes': notes,
    }
    return render(request, 'notes/search_note.html', context)


def create_tag(request):

	form = TagForm()
	tags = Tag.objects.all()
	
	if request.method =='POST':
		form = TagForm(request.POST)
		
		if form.is_valid():
			form.save()
		return redirect('/')

	context = {'form':form,'tags':tags}
	return render(request, 'notes/create_tag.html', context)


def h_search_note_text(request): 

	# Always use GET for search forms
	form = NoteSearchForm(request.GET or None)
	notes = Note.objects.all()  # Start with all notes
	print(request.GET)
	
	# HTMX Search request
	if request.htmx:

		print ("This is a HTMX request")
	

		if form.is_valid():
			# Get the search text and tags from the form
			search_text = form.cleaned_data.get('search_text')
			search_tags = form.cleaned_data.get('search_tags')
			print (search_tags)

			
			
			

			
			        # Filter notes by tags if tags are provided
			if search_tags:
				notes = notes.filter(tags__in=search_tags).distinct()

			
	else:
		notes = Note.objects.all().order_by('-date_created')
		

	context = {
	'form': form,
	'notes': notes,
}
	if request.htmx:
		return render(request, 'notes\h_partial_search_note.html', context)
	else:
		return render(request, 'notes\h_search_note_text.html', context)

	
def h_search_note_tag(request): 

	# Always use GET for search forms
	form = NoteSearchForm(request.GET or None)
	notes = Note.objects.all()  # Start with all notes
	print(request.GET)
	
	# HTMX Search request
	if request.htmx:

		print ("This is a HTMX request")
	

		if form.is_valid():
			# Get the search text and tags from the form
			search_text = form.cleaned_data.get('search_text')
			search_tags = form.cleaned_data.get('search_tags')
			print (search_tags)

			
			# Filter notes by search_text if provided
			if search_tags:
				notes = notes.filter(tags__in=search_tags).distinct()
			
			if search_text:
				notes = notes.filter(Q(text__icontains=search_text) | Q(summary__icontains=search_text))
			



			
	else:
		notes = Note.objects.all().order_by('-date_created')
		

	context = {
	'form': form,
	'notes': notes,
}
	if request.htmx:
		return render(request, 'notes\h_partial_search_note.html', context)
	else:
		return render(request, 'notes\h_search_note_tag.html', context)