# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

# Import the Category model
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm


def show_category(request, category_name_slug):
	# Create a context dictionary which we can pass
	# to the template rendering engine.
    context_dict = {}

    try:
		#Try to find a category with the provided name-slug
        category = Category.objects.get(slug=category_name_slug)

		# Retrieve all of the associated pages.
		# Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

		# Add the list of pages to the template context
        context_dict['pages'] = pages

		# Add the existing category object to the template context
        context_dict['category'] = category

    except Category.DoesNotExist:
    	# We get here if we didn't find the specified category.
    	# Don't do anything -
    	# the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    #initiate form instance to handle POST requests
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            #Direct the user back to the index page
            return index(request)
        else:
            # Print errors in the supplied form on the terminal
            print(form.errors)

    # Render a new form for GET requests or the form with errors
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try: 
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:  
                page = form.save(commit=False)
                page.category = category 
                page.views = 0
                page.save()
       
                return show_category(request, category_name_slug)

        else:
                print(form.errors)

    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

     
def index(request):
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by no. likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary
	# that will be passed to the template engine.

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

	
	#Render the response and send it back!
    return render(request, 'rango/index.html', context=context_dict)

	#return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About<a/>")
def about(request):
    context_dict = {'boldmessage': "This tutorial has been put together by Adi Dharma Pramudita."}
    return render(request, 'rango/about.html', context=context_dict)

