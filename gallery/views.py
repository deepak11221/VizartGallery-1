from django.shortcuts import render, redirect
from django.contrib import messages
from .models import snippet, category
from .forms import categoryForm, snippetForm
from graph.models import graph
# Create your views here.

def home_gallery(request):
    categories = category.objects.all()
    ctx = {'categories': categories}
    return render(request, 'gallery/home_gallery.html', ctx)


def add_category(request):
    # add person form
    form = category(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save() # save the form data to model
            messages.success(request, 'Your details added successfully')
            return redirect('home')
        else:
            messages.error(request, 'Error adding your details')
    ctx = {'form': form}
    return render(request, 'gallery/add_category.html', ctx)

def add_snippet(request):
    # add person form
    form = snippet(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save() # save the form data to model
            messages.success(request, 'Your details added successfully')
            return redirect('home_snippet.html')
        else:
            messages.error(request, 'Error adding your details')
    ctx = {'form': form}
    return render(request, 'gallery/add_snippet.html', ctx)

def view_category(request, id):
    cat = category.objects.get(id=id)
    Snippets = snippet.objects.filter(category=cat)
    ctx = {'cat': cat, 'snippets': Snippets}
    return render(request, 'gallery/view_category.html', ctx)

def view_snippet(request, id):
    Snippet1 = snippet.objects.get(id=id)
    ctx1 = {'snippet': Snippet1}
    return render(request, 'gallery/view_snippet.html', ctx1)

def edit_category(request, id):
    cat = category.objects.get(id=id)
    form = categoryForm(request.POST or None, request.FILES or None, instance=cat)
    if request.method == 'POST':
        if form.is_valid():
            form.save() # save the form data to model
            messages.success(request, 'Your details added successfully')
            return redirect('home_category.html')
        else:
            messages.error(request, 'Error adding your details')
    ctx = {'form': form}
    return render(request, 'gallery/edit_category.html', ctx)

def edit_snippet(request, id):
    snippet = snippet.objects.get(id=id)
    form = snippetForm(request.POST or None, request.FILES or None, instance=snippet)
    if request.method == 'POST':
        if form.is_valid():
            form.save() # save the form data to model
            messages.success(request, 'Your details added successfully')
            return redirect('home_snippet.html')
        else:
            messages.error(request, 'Error adding your details')
    ctx = {'form': form}
    return render(request, 'gallery/edit_snippet.html', ctx)


def delete_category(request, id):
    cat = category.objects.get(id=id)
    cat.delete()
    messages.success(request, 'Your details added successfully')
    return redirect('home_category.html')

def delete_snippet(request, id):
    snippet = snippet.objects.get(id=id)
    snippet.delete()
    messages.success(request, 'Your details added successfully')
    return redirect('home_snippet.html')

def search(request):
    if request.method == 'POST':
        searched = request.POST['query']
        snippets = snippet.objects.filter(code__icontains=searched)
        categories = category.objects.filter(name__icontains=searched)
        graphs = graph.objects.filter(name__icontains=searched)
        ctx = {'query': searched, 'snippets': snippets, 'categories': categories, 'graphs': graphs}
        return render(request, 'gallery/search.html', ctx)
    else:
        return render(request, 'gallery/search.html', {})
