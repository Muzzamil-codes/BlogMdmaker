from django.shortcuts import render, redirect, HttpResponse
from .models import BlogModel
from .forms import PostForm
from django.contrib.auth import logout
import os
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.

def userpanel(request):
    if request.user.is_authenticated:
        context = {}

        try:
            blog_objs = BlogModel.objects.filter(user=request.user)
            for obj in blog_objs:
                obj.image.name = obj.image.name[12:]
                print(obj.image.name)
            context['blog_objs'] = blog_objs
        except Exception as e:
            print(e)

        return render(request, 'userpanel.html', context)
    else:
        return redirect("login")

def login(request):
    if request.user.is_authenticated:
        return redirect("/user_panel/")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect("/")

# def blog_detail(request, slug):
#     context = {}
#     try:
#       blog_obj = BlogModel.objects.filter(slug = slug).first()
#       blog_obj.views = blog_obj.views + 1
#       blog_obj.save()
#       context['blog_obj'] = blog_obj
#       context['blogs'] = BlogModel.objects.exclude(slug=slug)
#       context['blogs'] = context['blogs'].filter(genre=blog_obj.genre)
#       context['views'] = blog_obj.views
#     except Exception as e:
#         print(e)
#     return render(request, 'blog_detail.html', context)

def add_blog(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        print(request.FILES)
        user = request.user
        title = request.POST.get('title')
        description = request.POST.get("description")
        image = request.FILES.get('image', '')
        
        categories = request.POST.get('categories')
        categories = categories.split(',') if categories else []

        tags = request.POST.get('tags', '')
        tags = tags.split(',') if tags else []

        

        if form.is_valid():
            content = form.cleaned_data['content']
            draft = form.cleaned_data['draft']
        # if form.is_valid():
        #     form.save()
        #     return redirect('add_blog')

        BlogModel.objects.create(
            user=user, title=title, description=description, image=image, caption=caption, categories=categories, tags=tags, draft=draft, content=content
        )
        messages.success(request, "Blog has been saved!")
        return redirect('/')

    else:
        form = PostForm()
    return render(request, 'add_blog.html', {'form': form})

def update_blog(request, slug):
    context = {'form': PostForm}
    try:

        blog_obj = BlogModel.objects.get(slug=slug)
        blog_image = blog_obj.image.name[8:]

        if blog_obj.user != request.user:
            return redirect('/')

        initial_dict = {'draft': blog_obj.draft ,'content': blog_obj.content}
        form = PostForm(initial=initial_dict)
        if request.method == 'POST':
            form = PostForm(request.POST)
            print(request.FILES)
            title = request.POST.get('title')
            description = request.POST.get("description")
            
            categories = request.POST.get('categories')
            categories = categories.split(',') if categories else []

            tags = request.POST.get('tags', '')
            tags = tags.split(',') if tags else []

            

            if form.is_valid():
                content = form.cleaned_data['content']
                draft = form.cleaned_data['draft']

            if 'image' in request.FILES:
                image = request.FILES.get('image', '')

                # if blog.image and os.path.exists(self.image.path):
                os.remove(blog_obj.image.path)

                blog_obj.title, blog_obj.description, blog_obj.image, blog_obj.caption, blog_obj.categories, blog_obj.tags, blog_obj.draft, blog_obj.content = title, description, image, caption, categories, tags, draft,content
                blog_obj.save()
                
            blog_obj.title, blog_obj.description, blog_obj.caption, blog_obj.categories, blog_obj.tags, blog_obj.draft, blog_obj.content = title, description, caption, categories, tags, draft, content
            blog_obj.save()

            messages.success(request, "Blog has been updated!")

            return redirect("/")

        # categoires in string format
        incategories = ''
        for category in blog_obj.categories:
            incategories = incategories + f"{category},"
            
        # tags in string format
        intags = ''
        for tag in blog_obj.tags:
            print(tag)
            intags = intags + f"{tag},"
        context['blog_image'] = blog_image
        context['blog_obj'] = blog_obj
        context['intags'] = intags
        context['incategories'] = incategories
        context['form'] = form
    except Exception as e:
        print(e)

    return render(request, 'update_blog.html', context)


def delete_blog(request, slug):
    try:
        blog_obj = BlogModel.objects.get(slug=slug)

        if blog_obj.user == request.user:
            blog_obj.delete()

    except Exception as e:
        print(e)

    return redirect('/user_panel/')


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keep the user logged in after password change
            messages.success(request, 'Password changed successfully!')
            return redirect('/')  # Redirect to the desired page after success
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'reset_password.html', {'form': form})


