"""Defines functionality of all the buttons on the website."""
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from netwio.models import Comment
from netwio.models import Post


NUM_OF_POSTS = 5


def home(request, username=None):
    """Provides support for data representation on the home page."""
    first_name = ''
    last_name = ''
    if username:
        user = User.objects.get(username=username)
        first_name = user.first_name
        last_name = user.last_name
        post_list = Post.objects.filter(user=user)
    else:
        post_list = Post.objects.all()

    post_list = post_list.order_by('-pub_date')

    paginator = Paginator(post_list, NUM_OF_POSTS)  # Show NUM_OF_PAGES posts per page
    page = request.GET.get('page')

    posts = paginator.get_page(page)

    return render(request, 'netwio/home.html', {'posts': posts,
                                                'first_name': first_name,
                                                'last_name': last_name})


class CommentCreate(LoginRequiredMixin, CreateView):
    """Provides logic of comment creation."""
    model = Comment
    fields = ['body']
    template_name = 'netwio/create_comment.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('netwio:post', kwargs={'pk': self.kwargs['pk']})


class PostCreate(LoginRequiredMixin, CreateView):
    """Provides logic of post creation."""
    model = Post
    fields = ['title', 'body']
    template_name = 'netwio/create_post.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Provides logic of changing the published post."""
    model = Post
    fields = ['title', 'body']
    template_name = 'netwio/create_post.html'
    login_url = reverse_lazy('login')

    def test_func(self):
        return Post.objects.get(id=self.kwargs['pk']).user == self.request.user


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Provides logic of post deletion."""
    model = Post
    success_url = reverse_lazy('netwio:home')
    login_url = reverse_lazy('login')

    def test_func(self):
        return Post.objects.get(id=self.kwargs['pk']).user == self.request.user


class PostView(generic.DetailView):
    """Provides logic of a created post representation."""
    model = Post
    template_name = 'netwio/post.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the username
        comments = Comment.objects.filter(post=self.kwargs['pk'])
        context['comments'] = comments
        return context


class RegisterView(CreateView):
    """Signes the user up."""
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'email']
    template_name = 'netwio/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Hash password before sending it to super
        form.instance.password = make_password(form.instance.password)
        return super().form_valid(form)
