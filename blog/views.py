from django.http import HttpResponse
from django.urls import reverse_lazy
from datetime import datetime
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from .tasks import hello, printer


class PostsList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class SearchPosts(ListView):
    paginate_by = 10
    model = Post
    ordering = '-date_time'
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['search_filter'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('blog.add_post',
                           'blog.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить статью"
        return context


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView, TemplateView):
    permission_required = ('blog.add_post',
                           'blog.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать статью"
        return context


class ArticleDelete(DeleteView):
    """ Представление для удаления статьи. """
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удалить статью"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('blog.add_post',
                           'blog.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить новость"
        return context


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView, TemplateView):
    permission_required = ('blog.add_post',
                           'blog.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать новость"
        return context


class NewsDelete(DeleteView):
    """ Представление для удаления новости. """
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удалить новость"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context

    class IndexView(LoginRequiredMixin, TemplateView):
        template_name = 'index.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
            return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


class CategoryListView(ListView, Post):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_posts_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории!'
    return render(request, 'subscribe_html', {'category':category, 'message': message})


class IndexView(View):
    def get(self, request):
        printer.delay(10)
        hello.delay()
        return HttpResponse('Hello!')


