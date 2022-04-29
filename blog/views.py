from django.shortcuts import render, reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
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
    template_name = 'blog/home.html'  # или будет искать <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


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
        form.instance.post_id = self.kwargs['pk']  # this is line sets post_id with pk from url
        form.instance.author = self.request.user  # in case you need to display author
        return super().form_valid(form)

    # returns url where you 'll be redirected after the form is correctly filled
    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("post-detail", kwargs={"pk": pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['comment_pk']
        form.instance.author = self.request.user.username
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user.username == comment.author

    def get_success_url(self):
        pk = self.kwargs['comment_pk']
        return reverse("post-detail", kwargs={"pk": pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user.username == comment.author

    def get_success_url(self):
        pk = self.kwargs['comment_pk']
        return reverse("post-detail", kwargs={"pk": pk})


class CommentReplyView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user.username
        form.instance.post_id = self.kwargs['pk']
        form.instance.parent_id = self.kwargs['comment_pk']
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse("post-detail", kwargs={"pk": pk})


def about(request):
    return render(request, 'blog/about.html', {'title': "About"})
