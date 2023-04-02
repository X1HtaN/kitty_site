from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .templatetags.kitty_tags import menu
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login
from django.views.generic.edit import FormView

from .forms import *
from .utils import *

# Create your views here.
class KittyHome(DataMixin, ListView):
    paginate_by = 5
    model = Kitty
    template_name = 'kitty/index.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return {**context, **c_def}
    
    #только опубликованные записи
    def get_queryset(self):
        return Kitty.objects.filter(is_published=True).select_related('cat')
    
class KittyCategory(DataMixin, ListView):
    model = Kitty
    template_name = 'kitty/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self,*, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.pk)
        return {**context, **c_def}

    def get_queryset(self):
        return Kitty.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
    
class ShowPost(DataMixin, DetailView):
    model = Kitty
    template_name = 'kitty/post.html'
    slug_url_kwarg = 'post_slug'
    #pk_url_kwarg для id
    context_object_name = 'post'

    def get_context_data(self,*, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return {**context, **c_def}
    
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = addPostForm
    template_name = 'kitty/addpage.html'
    #если нету get_absolute_url в models
    #success_url = reverse_lazy('home')
    login_url = '/admin/'

    def get_context_data(self,*, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return {**context, **c_def}
    
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'kitty/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return {**context, **c_def}
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
    
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'kitty/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return {**context, **c_def}
    
    # def get_success_url(self) -> str:
    #     return reverse_lazy('home')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'kitty/contact.html'
    sucess_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return {**context, **c_def}
    
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

def logout_user(request):
    logout(request)
    return redirect('login')

def about(request):
    return render(request, 'kitty/about.html', {'title': 'О сайте'})
    return HttpResponse('авторизация')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена(((</h1>')