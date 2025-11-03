from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from journal.models import JournalEntry
from .forms import JournalEntryForm
from django.db import models




@login_required#
def entries_home(request):
    q=request.GET.get('q', '')
    if q:# if the user types in a keyword and searches for something in the search bar, then filter it and show from newest to oldest entries.
        entries=JournalEntry.objects.filter(author=request.user).filter(models.Q(title__icontains=q)| models.Q(content__icontains=q)).order_by('-created_at')
    else:
        entries=JournalEntry.objects.filter(author=request.user).order_by('-created_at')

    form=JournalEntryForm()# empty form for creation
    if request.method=='POST':
        form=JournalEntryForm(request.POST, request.FILES) # include files for image upload
        if form.is_valid():
            entry=form.save(commit=False)# create object but don't save yet
            entry.author=request.user# assign current user as the author
            entry.save()# save to DB (includes image if provided)
            messages.success(request,'Journal entry created')
            return redirect('entries_home')# redirect to avoid re-posting on refresh
    context={'entries':entries, 'form':form, 'q':q}
    return render(request, 'journal/entries_home.html', context)

@login_required###
def entry_update(request,pk):
    entry=get_object_or_404(JournalEntry, id=pk, author=request.user)
    if request.method=='POST':
        form=JournalEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request,'Journal entry updated.')
            return redirect('entries_home')
        
    else:
        form=JournalEntryForm(instance=entry)# prefill with current data

    return render(request, 'journal/entry_update.html',{'form':form})

@login_required#
def entry_delete(request, pk):
    entry=get_object_or_404(JournalEntry, id=pk,  author=request.user)
    if request.method=='POST':
        entry.delete()
        messages.success(request, 'Journal entry deleted.')
        return redirect('entries_home')
    return render(request, 'journal/entry_delete.html', {'entry':entry})


@login_required#
def entry_detail(request,pk):
    entry=get_object_or_404(JournalEntry, id=pk, author=request.user)
    return render(request, 'journal/entry_detail.html', {'entry':entry})


def login_view(request): ###
    if request.method=='POST':
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
          user=form.get_user()# get the actual user object
          login(request, user) #create session
          return redirect('entries_home')
        else:
         messages.error(request, 'Invalid username or password')
    else:
     form=AuthenticationForm()
    return render(request, 'journal/login.html', {'form':form})

    
def logout_view(request): ###
    #Handles user logout.
    #- Ends the user session.
    #- Shows a simple logout confirmation page.
    logout(request)
    messages.info(request, '"You have been logged out successfully."')
    return render(request, 'journal/logout.html')


def signup_view(request):
    if request.method=='POST':

        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()

            messages.success(request, f"Welcome, {user.username}! Your account was created.")
            login(request, user) #login the user after sign up
            return redirect('entries_home')
        
    else:
         form = UserCreationForm()
    return render(request, 'journal/signup.html', {'form': form})
        