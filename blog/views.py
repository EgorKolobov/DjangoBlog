from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'  # или будет искать <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = "blog/post_update_form.html"

    # need to be logged in order to update post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # only author can update post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    # only author can update post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm  # filds to be displayed in your form. You may also use your custom form_class
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')  # this is line sets post_id with pk from url
        form.instance.author = self.request.user  # in case you need to display author
        return super().form_valid(form)

    # returns url where you 'll be redirected after the form is correctly filled
    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse("post-detail", kwargs={"pk": pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_update_form.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user.username == comment.author

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, pk=self.kwargs.get('comment_pk'))

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse("post-detail", kwargs={"pk": pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user.username == comment.author

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, pk=self.kwargs.get('comment_pk'))

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse("post-detail", kwargs={"pk": pk})


class CommentReplyView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user.username
        form.instance.post_id = self.kwargs.get('pk')
        form.instance.parent_id = self.kwargs.get('comment_pk')
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse("post-detail", kwargs={"pk": pk})


def about(request):
    return render(request, 'blog/about.html', {'title': "About"})
