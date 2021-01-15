from django.shortcuts import render, redirect
from .models import Post, Tag
# from .forms import TagForm, PostForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView


def posts_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(
            Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginator = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginator,
        'next_url': next_url,
        'prev_url': prev_url
    }
    return render(request, 'blog/index.html', context=context)


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'body', 'tags']
    raise_exception = True


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'body', 'tags']
    template_name_suffix = '_update_form'
    raise_exception = True


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('posts_list_url')
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html',
                  context={'tags': tags})


class TagCreate(LoginRequiredMixin, CreateView):
    model = Tag
    fields = ['title', 'slug']
    raise_exception = True


class TagUpdate(LoginRequiredMixin, UpdateView):
    model = Tag
    fields = ['title', 'slug']
    template_name_suffix = '_update_form'
    raise_exception = True


class TagDelete(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('tags_list_url')
    raise_exception = True


class TagDetailView(DetailView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
