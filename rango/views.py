from django.shortcuts import render
from rango.models import Page
from django.http import HttpResponse
from rango.models import Category
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse

def about(request):
    context_dict2={'boldmessage':'Rango says here is the about page.'}
    return render(request,'rango/about.html',context=context_dict2)
def index(request):
# Construct a dictionary to pass to the template engine as its context.
    category_list=Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict={}
    context_dict['boldmessage']= 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories']=category_list
    context_dict['pages'] = page_list
# Return a rendered response to send to the client.
    return render(request, 'rango/index.html', context=context_dict)
def show_category(request, category_name_slug):
# Create a context dictionary which we can pass
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
# The filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
# Go render the response and return it to the client.
    return render(request, 'rango/category.html', context=context_dict)
def add_category(request):
    form = CategoryForm()
    if request.method =='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
# Save the new category to the database.
            form.save(commit=True)
# For now, just redirect the user back to the index view.
            return redirect('/rango/')
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    if category is None:
        return redirect(reverse('rango:index'))
    form = PageForm()
    if request.method =='POST':
        form = PageForm(request.POST)
    if form.is_valid():
        if category:
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect(reverse('rango:show_category',kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

