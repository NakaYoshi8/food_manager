from django.urls import path

from . import views


app_name = 'food_manager'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),

    path('signup/', views.signup, name='signup'),
    path('account/<int:pk>/edit/', views.account_edit, name='account_edit'),
    path('account/<int:pk>/delete/', views.account_delete, name='account_delete'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),

    path('expiration-date/', views.ExpirationDateView.as_view(), name='expiration_date'),

    path('trash/', views.TrashView.as_view(), name='trash'),

    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('category/<int:category_pk>/tags/', views.category_tags, name='category_tags'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('tag/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('tag/<int:tag_pk>/foods/', views.tag_foods, name='tag_foods'),
    path('tag/<int:pk>/delete/', views.tag_delete, name='tag_delete'),

    path('food/<int:pk>/', views.food_view, name='food'),
    path('food/<int:food_pk>/tags/', views.food_tags, name='food_tags'),
]