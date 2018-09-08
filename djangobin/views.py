import datetime
from smtpd import usage

from django.contrib.auth.context_processors import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import mail_admins
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, reverse, get_list_or_404
from djangobin.forms import SnippetForm, ContactForm, LoginForm
from django.contrib import messages
from djangobin.models import Language, Snippet, Tag
from djangobin.utils import paginate_result
from django.contrib.auth.models import User
from django.contrib import auth
def index(request):
    if request.method=='POST':
        f=SnippetForm(request.POST)
        if f.is_valid():
            snippet=f.save(request)
            return redirect(reverse('djangobin:snippet_detail', args=[snippet.slug]))
    else:
        f=SnippetForm()
    return render(request, 'djangobin/index.html',{'form':f})

def snippet_detail(request, snippet_slug):
    snippet = get_object_or_404(Snippet, slug=snippet_slug)
    snippet.hits += 1
    snippet.save()
    # return render(request, 'djangobin/snippet_detail.html', {'snippet': snippet})
    return render(request, 'djangobin/snippet_detail.html', {'snippet': snippet})

def download_snippet(request, snippet_slug):
    snippet=get_object_or_404(Snippet, slug=snippet_slug)
    file_extension=snippet.language.file_extension
    filename=snippet.slug+file_extension
    res=HttpResponse(snippet.original_code)
    res['content-disposition']='attachment; filename='+filename+';'
    return res

def raw_snippet(request, snippet_slug):
    snippet=get_object_or_404(Snippet, slug=snippet_slug)
    return HttpResponse(snippet.original_code, content_type=snippet.language.mime)

def trending_snippets(request, language_slug=''):
    lang=None
    snippets=Snippet.objects
    if language_slug:
        snippets=snippets.filter(language__slug=language_slug)
        lang=get_object_or_404(Language, slug=language_slug)
    snippets=snippets.all()
    snippet_list=get_list_or_404(snippets.filter(exposure='public').order_by('-hits'))
    snippets=paginate_result(request, snippet_list, 5)
    return render(request, 'djangobin/trending.html',{'snippets':snippets, 'lang':lang})

def tag_list(request, tag):
    t=get_object_or_404(Tag, name=tag)
    snippet_list=get_list_or_404(t.snippet_set)
    snippets=paginate_result(request, snippet_list, 5)
    return render(request, 'djangobin/tag_list.html', {'snippets':snippets, 'tag':t})

def profile(request, username):
    return HttpResponse('<p> Profile page for #{}</p>'.format(username))

def contact(request):
    if request.method=='POST':
        f=ContactForm(request.POST)
        if f.is_valid():
            name=f.cleaned_data['name']
            subject="You have a new feedback from {}:<{}>".format(name, f.cleaned_data['email'])
            message="Purpose: {}\n\nDate: {}\n\nMessage:\n\n {}".format(
                dict(f.purpose_choices).get(f.cleaned_data['purpose']),
                datetime.datetime.now(),
                f.cleaned_data['message']
            )
            mail_admins(subject, message)
            messages.add_message(request, messages.INFO, 'Thanks for submitting your feedback')
            return redirect('djangobin:contact')
    else:
        f=ContactForm()
    return render(request, 'djangobin/contact.html', {'form':f})

def login(request):
    if request.user.is_authenticated:
        return redirect('djangobin:profile', username=request.user.username)
    if request.method=='POST':
        f=LoginForm(request.POST)
        if f.is_valid():
            user=User.objects.filter(email=f.cleaned_data['email'])
            if user:
                user=auth.authenticate(
                    username=user[0].username,
                    password=f.cleaned_data['password'],
                )
                if user:
                    auth.login(request, user)
                    return redirect(request.GET.get('next') or 'djangobin:index')
            messages.add_message(request, messages.INFO, 'Invalid email/password.')
            return redirect('djangobin:login')
    else:
        f=LoginForm()
    return render(request, 'djangobin/login.html', {'form':f})

@login_required
def logout(request):
    auth.logout(request)
    return render(request, 'djangobin/logout.html')

@login_required
def user_details(request):
    user=get_object_or_404(User, id=request.user.id)
    return render(request, 'djangobin/user_details.html', {'user':user})

def signup(request):
    if request.user.is_authenticated:
        return redirect('djangobin:profile', username=request.user.username)
    if request.method=='POST':
        f=UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('signup')
    else:
        f=UserCreationForm()
    return render(request, 'djangobin/signup.html', {'form':f})