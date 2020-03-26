from django.shortcuts import render, get_object_or_404
from .forms import UserForm, UserProfileForm, PostForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from .models import Post, UserProfile
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request,
                'base.html',
                {'userprofile' : UserProfile.objects.all()})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request,
                'users/register.html',
                {'user_form': user_form,
                'profile_form': profile_form,
                'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is disabled")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'users/login.html')


def create_post(request):
    if request.user and request.method == 'POST':
        post_form = PostForm(data=request.POST)
       
        if post_form.is_valid():
            seeker = request.user.userprofile
            post = post_form.save(commit=False)
            post.seeker = seeker
            post.save()
            return HttpResponseRedirect(reverse('posts:post-list'))
        else:
            print(post_form.errors)
    else:
        post_form = PostForm()

    return render(request, 
        'posts/post_form.html',
        {'post_form': post_form})




class PostView(generic.DetailView):
    model = Post
    template_name = "posts/post.html"


class PostListView(generic.ListView):
    template_name = 'posts/post-list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.all()


class ProfileView(generic.ListView):
    model = Post
    template_name = "posts/profile.html"
    context_object_name = 'post_list'

    def get_queryset(self):
        id = self.kwargs['pk']
        target_profile = get_object_or_404(UserProfile, pk = id)
        return Post.objects.filter(seeker=target_profile)


class PostCreate(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'description', 'points', 'req_skill']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



