import datetime

from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from .models import User, Category, Tag, Food
from .forms import *


class IndexView(generic.ListView):
    template_name = 'food_manager/index.html'
    
    def get_template_names(self):
        if self.request.user.is_authenticated:
            template_name = 'food_manager/dashboard.html'
        else:
            template_name = self.template_name
        return template_name
    
    def get_context_data(self):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            context['category_list'] = Category.objects.filter(user=self.request.user)
            context['tag_list'] = Tag.objects.filter(user=self.request.user)
            context['food_list'] = Food.objects.filter(user=self.request.user, trash=False)
            context['category_add_form'] = CategoryForm()
            tag_add_form = TagForm()
            tag_add_form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
            context['tag_add_form'] = tag_add_form
            context['food_add_form'] = FoodForm()
        return context
    
    def get_queryset(self):
        queryset = ()
        if self.request.user.is_authenticated:
            queryset = (
                Category.objects.filter(user=self.request.user),
                Tag.objects.filter(user=self.request.user),
                Food.objects.filter(user=self.request.user, trash=False),
            )
        return queryset
    
    def post(self, request):
        if 'category-add-btn' in request.POST:
            category_add_form = CategoryForm(request.POST)
            
            if category_add_form.is_valid():
                category = category_add_form.save(commit=False)
                category.user = request.user
                category.save()
                
                return HttpResponseRedirect(reverse('food_manager:index'))
        
        elif 'tag-add-btn' in request.POST:
            tag_add_form = TagForm(request.POST)
            
            if tag_add_form.is_valid():
                tag = tag_add_form.save(commit=False)
                tag.user = request.user
                tag.save()
                
                return HttpResponseRedirect(reverse('food_manager:index'))

        elif 'food-add-btn' in request.POST:
            food_add_form = FoodForm(request.POST)
            
            if food_add_form.is_valid():
                food = food_add_form.save(commit=False)
                food.user = request.user
                food.save()
                
                return HttpResponseRedirect(reverse('food_manager:food_tags', args=(food.pk,)))
        
        return HttpResponseRedirect(reverse('food_manager:index'))


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('food_manager:index'))
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})


def account_edit(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.user != user:
        raise PermissionDenied

    if request.method == 'POST':
        if 'username-edit-btn' in request.POST:
            username_form = UsernameForm(request.POST, instance=user)
            if username_form.is_valid():
                user = username_form.save()
                user.save()
                return HttpResponseRedirect(reverse('food_manager:account_edit', args=(pk,)))
        
        elif 'email-edit-btn' in request.POST:
            email_form = EmailForm(request.POST, instance=user)
            if email_form.is_valid():
                user = email_form.save()
                user.save()
                return HttpResponseRedirect(reverse('food_manager:account_edit', args=(pk,)))
        
        return HttpResponseRedirect(reverse('food_manager:account_edit', args=(pk,)))

    username_form = UsernameForm(instance=user)
    email_form = EmailForm(instance=user)

    return render(request, 'registration/account_edit.html', {
        'username_form': username_form,
        'email_form': email_form,
    })


def account_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.user != user:
        raise PermissionDenied
    
    if request.method == 'POST':
        user.is_active = False
        user.save()
        logout(request)
        return HttpResponseRedirect(reverse('food_manager:index'))
    
    return render(request, 'registration/account_delete.html', {})


class PasswordChange(auth_views.PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('food_manager:password_change_done')
    template_name = 'registration/password_change.html'


class PasswordChangeDone(auth_views.PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'registration/password_change_done.html'


class ExpirationDateView(generic.ListView):
    template_name = 'food_manager/expiration_date.html'

    def get_context_data(self):
        context = super().get_context_data()
        now = timezone.now()
        near_expiration_date = now + datetime.timedelta(days=3)
        # 賞味期限が現在から3日以内の食品リスト
        context['near_expiration_food_list'] = Food.objects.filter(
            date__lte=near_expiration_date, date__gt=now, user=self.request.user, trash=False
        )
        # 賞味期限が現在以前の食品リスト
        context['expired_food_list'] = Food.objects.filter(date__lte=now, user=self.request.user, trash=False)
        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Food.objects.filter(user=self.request.user, trash=False)


class TrashView(generic.ListView):
    template_name = 'food_manager/trash.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['food_list'] = Food.objects.filter(user=self.request.user, trash=True)
        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Food.objects.filter(user=self.request.user, trash=True)
    
    def post(self, request):
        food_list = Food.objects.filter(user=self.request.user, trash=True)
        checked_pk_list = request.POST.getlist('food')
        checked_food_list = []
        
        for food_pk in checked_pk_list:
            food = Food.objects.get(pk=food_pk)
            checked_food_list.append(food)
        
        if 'delete-btn' in request.POST:
            for food in food_list:
                if food in checked_food_list:
                    food.delete()
            
            return HttpResponseRedirect(reverse('food_manager:trash'))

        elif 'restore-btn' in request.POST:
            for food in food_list:
                if food in checked_food_list:
                    food.trash = False
                    food.save()
                
            return HttpResponseRedirect(reverse('food_manager:trash'))
        
        return HttpResponseRedirect(reverse('food_manager:trash'))


class CategoryView(UserPassesTestMixin, generic.DetailView):
    model = Category
    template_name = 'food_manager/category.html'
    raise_exception = True
    
    def test_func(self):
        category = Category.objects.get(pk=self.kwargs['pk'])
        return self.request.user == category.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['category_edit_form'] = CategoryForm(instance=Category.objects.get(pk=self.kwargs['pk']))
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user)
        return queryset
    
    def post(self, request, pk):
        if 'category-edit-btn' in request.POST:
            category_edit_form = CategoryForm(request.POST, instance=Category.objects.get(pk=self.kwargs['pk']))
            
            if category_edit_form.is_valid():
                category = category_edit_form.save()
                category.save()
                
                return HttpResponseRedirect(reverse('food_manager:category', args=(pk,)))
        
        return HttpResponseRedirect(reverse('food_manager:category', args=(pk,)))


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.user != category.user:
        raise PermissionDenied

    if request.method == 'POST':
        category.delete()
        
        return HttpResponseRedirect(reverse('food_manager:index'))
    
    return render(request, 'food_manager/category_delete.html', {'category': category})


def category_tags(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)

    if request.user != category.user:
        raise PermissionDenied

    tag_list = Tag.objects.filter(user=request.user)

    if request.method == 'POST':
        checked_pk_list = request.POST.getlist('tag')
        checked_tag_list = []
        
        for tag_pk in checked_pk_list:
            tag = Tag.objects.get(pk=tag_pk)
            checked_tag_list.append(tag)

        for tag in tag_list:
            if tag in checked_tag_list:
                tag.category = category
            else:
                if tag.category == category:
                    tag.category = None
            tag.save()
        
        return HttpResponseRedirect(reverse('food_manager:category', args=(category_pk,)))

    return render(request, 'food_manager/category_tags.html', {
        'category': category,
        'tag_list': tag_list,
    })


class TagView(UserPassesTestMixin, generic.DetailView):
    model = Tag
    template_name = 'food_manager/tag.html'
    raise_exception = True
    
    def test_func(self):
        tag = Tag.objects.get(pk=self.kwargs['pk'])
        return self.request.user == tag.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tag = Tag.objects.get(pk=self.kwargs['pk'])
        tag_edit_form = TagForm(instance=Tag.objects.get(pk=self.kwargs['pk']))
        tag_edit_form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        tag_food_list = Food.objects.filter(user=self.request.user, tags__in=[tag,], trash=False)
        context = {
            'tag': tag,
            'tag_edit_form': tag_edit_form,
            'tag_food_list': tag_food_list,
        }
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user)
        return queryset
    
    def post(self, request, pk):
        if 'tag-edit-btn' in request.POST:
            tag_edit_form = TagForm(request.POST, instance=Tag.objects.get(pk=self.kwargs['pk']))
            
            if tag_edit_form.is_valid():
                tag = tag_edit_form.save()
                tag.save()
                
                return HttpResponseRedirect(reverse('food_manager:tag', args=(pk,)))
        
        return HttpResponseRedirect(reverse('food_manager:tag', args=(pk,)))


def tag_foods(request, tag_pk):
    tag = get_object_or_404(Tag, pk=tag_pk)

    if request.user != tag.user:
        raise PermissionDenied

    food_list = Food.objects.filter(user=request.user, trash=False)

    if request.method == 'POST':
        checked_pk_list = request.POST.getlist('food')
        checked_food_list = []
        
        for food_pk in checked_pk_list:
            food = Food.objects.get(pk=food_pk)
            checked_food_list.append(food)

        for food in food_list:
            if food in checked_food_list:
                food.tags.add(tag)
            else:
                food.tags.remove(tag)
            
            food.save()
        
        return HttpResponseRedirect(reverse('food_manager:tag', args=(tag_pk,)))

    return render(request, 'food_manager/tag_foods.html', {
        'tag': tag,
        'food_list': food_list,
    })


def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)

    if request.user != tag.user:
        raise PermissionDenied

    if request.method == 'POST':
        tag.delete()
        
        return HttpResponseRedirect(reverse('food_manager:index'))
    
    return render(request, 'food_manager/tag_delete.html', {'tag': tag})


def food_view(request, pk):
    food = get_object_or_404(Food, pk=pk)

    if request.user != food.user:
        raise PermissionDenied

    if request.method == 'POST':
        if 'food-name-edit-btn' in request.POST:
            name_form = FoodNameForm(request.POST, instance=food)
            
            if name_form.is_valid():
                food = name_form.save()
                food.save()
            
            return HttpResponseRedirect(reverse('food_manager:food', args=(pk,)))
        
        elif 'food-trash-btn' in request.POST:
            food.trash = True
            food.save()
        
            return HttpResponseRedirect(reverse('food_manager:index'))
        
        elif 'food-edit-btn' in request.POST:
            date_form = FoodDateForm(request.POST, instance=food)
            quantity_form = FoodQuantityForm(request.POST, instance=food)
            unit_form = FoodUnitForm(request.POST, instance=food)
            description_form = FoodDescriptionForm(request.POST, instance=food)
            
            if date_form.is_valid() and quantity_form.is_valid() \
            and unit_form.is_valid() and description_form.is_valid():
                food = date_form.save()
                food = quantity_form.save()
                food = unit_form.save()
                food = description_form.save()
                food.save()
            
            return HttpResponseRedirect(reverse('food_manager:food', args=(pk,)))

    name_form = FoodNameForm(instance=food)
    date_form = FoodDateForm(instance=food)
    quantity_form = FoodQuantityForm(instance=food)
    unit_form = FoodUnitForm(instance=food)
    description_form = FoodDescriptionForm(instance=food)

    date_alert = ''
    if food.expiration_date() == 'near':
        date_alert = '賞味期限が近づいています'
    elif food.expiration_date() == 'expired':
        date_alert = '賞味期限を過ぎています'

    return render(request, 'food_manager/food.html', {
        'food': food,
        'name_form': name_form,
        'date_alert': date_alert,
        'date_form': date_form,
        'quantity_form': quantity_form,
        'unit_form': unit_form,
        'description_form': description_form,
    })


def food_tags(request, food_pk):
    food = get_object_or_404(Food, pk=food_pk)

    if request.user != food.user:
        raise PermissionDenied

    tag_list = Tag.objects.filter(user=request.user)

    if request.method == 'POST':
        checked_pk_list = request.POST.getlist('tag')
        checked_tag_list = []
        
        for tag_pk in checked_pk_list:
            tag = Tag.objects.get(pk=tag_pk)
            checked_tag_list.append(tag)

        for tag in tag_list:
            if tag in checked_tag_list:
                food.tags.add(tag)
            else:
                food.tags.remove(tag)
            
            food.save()
        
        return HttpResponseRedirect(reverse('food_manager:food', args=(food_pk,)))

    return render(request, 'food_manager/food_tags.html', {
        'food': food,
        'tag_list': tag_list,
    })