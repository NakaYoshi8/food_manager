import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from food_manager.models import User, Category, Tag, Food


class FoodModelTests(TestCase):

    def test_expiration_date_is_1_day_after_now(self):
        '''
        If the expiration date is 1 day after now, food.expiration_date() = 'near'.
        '''
        date = timezone.now() + datetime.timedelta(days=1)
        food = Food.objects.create(food_name='f', date=date, trash=False)
        
        self.assertIs(food.expiration_date(), 'near')

    def test_expiration_date_is_1_day_ago(self):
        '''
        If the expiration date has expired, food.expiration_date() = 'expired'.
        '''
        date = timezone.now() + datetime.timedelta(days=-1)
        food = Food.objects.create(food_name='f', date=date, trash=False)
        
        self.assertIs(food.expiration_date(), 'expired')


class UserIndexViewTests(TestCase):

    def test_not_authenticated(self):
        '''
        If request user is anonymous, login button and description of the application are displayed.
        '''
        client = Client()
        client.logout()
        response = client.get(reverse('food_manager:index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ログイン')
    
    def test_authenticated(self):
        '''
        If request user is authenticated, logout button and the user's data are displayed.
        '''
        user1 = User.objects.create_user('u1')
        user2 = User.objects.create_user('u2')
        client = Client()
        client.force_login(user1)
        category1 = Category.objects.create(category_name='c1', user=user1)
        category2 = Category.objects.create(category_name='c2', user=user2)
        tag1 = Tag.objects.create(tag_name='t1', user=user1)
        tag2 = Tag.objects.create(tag_name='t2', user=user2)
        food1 = Food.objects.create(food_name='f1', user=user1)
        food2 = Food.objects.create(food_name='f2', user=user2)
        response = client.get(reverse('food_manager:index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ログアウト' and 'u1')
        self.assertContains(response, category1 and tag1 and food1)
        self.assertNotContains(response, category2 and tag2 and food2)


class DashboardViewTests(TestCase):

    def test_category_does_not_exist(self):
        '''
        If category does not exist, the message indicating that is displayed.
        '''
        user = User.objects.create_user(username='u')
        client = Client()
        client.force_login(user)
        response = client.get(reverse('food_manager:index'))
        
        self.assertContains(response, 'カテゴリがありません')

    def test_tag_does_not_exist(self):
        '''
        If tag does not exist, the message indicating that is displayed.
        '''
        user = User.objects.create_user(username='u')
        client = Client()
        client.force_login(user)
        response = client.get(reverse('food_manager:index'))
        
        self.assertContains(response, 'タグがありません')

    def test_food_does_not_exist(self):
        '''
        If food does not exist, the message indicating that is displayed.
        '''
        user = User.objects.create_user(username='u')
        client = Client()
        client.force_login(user)
        response = client.get(reverse('food_manager:index'))
        
        self.assertContains(response, '食品がありません')


class ExpirationDateViewTests(TestCase):

    def test_food_near_expiration_does_not_exist(self):
        '''
        If food near expiration does not exist, the message indicating that is displayed.
        '''
        user = User.objects.create_user(username='u')
        client = Client()
        client.force_login(user)
        response = client.get(reverse('food_manager:expiration_date'))
        
        self.assertContains(response, '賞味期限間近の食品はありません')

    def test_expired_food_does_not_exist(self):
        '''
        If expired food does not exist, the message indicating that is displayed.
        '''
        user = User.objects.create_user(username='u')
        client = Client()
        client.force_login(user)
        response = client.get(reverse('food_manager:expiration_date'))
        
        self.assertContains(response, '賞味期限切れの食品はありません')


class TrashViewTests(TestCase):

    def test_display_of_food_in_trash_box(self):
        '''
        Trashed foods are displayed.
        '''
        user = User.objects.create_user(username='u')
        client = Client()
        client.force_login(user)
        food1 = Food.objects.create(food_name='f1', user=user, trash=True)  # trashed
        food2 = Food.objects.create(food_name='f2', user=user, trash=False)  # not trashed
        response = client.get(reverse('food_manager:trash'))
        
        self.assertContains(response, food1)  # trashed
        self.assertNotContains(response, food2)  # not trashed

    def test_trashed_food_does_not_exist(self):
        '''
        If trashed food does not exist, the message indicating that is displayed.
        '''
        user = User.objects.create_user(username='u')
        client = Client()
        client.force_login(user)
        response = client.get(reverse('food_manager:trash'))
        
        self.assertContains(response, 'ごみ箱に食品がありません')


class CategoryViewTests(TestCase):

    def test_tag_does_not_exist_in_category(self):
        '''
        If tag does not exist in category, the message indicating that is displayed.
        '''
        user = User.objects.create_user(username='u')
        client = Client()
        client.force_login(user)
        category = Category.objects.create(category_name='c', user=user, pk=1)
        response = client.get(reverse('food_manager:category', args=(1,)))
        
        self.assertContains(response, 'このカテゴリ内にタグがありません')


class TagViewTests(TestCase):

    def test_food_related_to_tag_does_not_exist(self):
        '''
        If food related to tag does not exist, the message indicating that is displayed.
        '''
        user = User.objects.create_user(username='u')
        client = Client()
        client.force_login(user)
        tag = Tag.objects.create(tag_name='t', user=user, pk=1)
        response = client.get(reverse('food_manager:tag', args=(1,)))
        
        self.assertContains(response, 'このタグに関連する食品がありません')

    def test_display_of_trashed_food_on_the_tag_page(self):
        '''
        Trashed foods are not displayed.
        '''
        user = User.objects.create_user(username='u')
        client = Client()
        client.force_login(user)
        tag = Tag.objects.create(tag_name='t', user=user, pk=1)
        food1 = Food.objects.create(food_name='f1', user=user, trash=False)  # not trashed
        food1.tags.add(tag)
        food2 = Food.objects.create(food_name='f2', user=user, trash=True)  # trashed
        food2.tags.add(tag)
        response = client.get(reverse('food_manager:tag', args=(1,)))
        
        self.assertContains(response, tag and food1)  # not trashed
        self.assertNotContains(response, food2)  # trashed


class FoodViewTests(TestCase):

    # date alert test
    
    def test_date_alert_3days_later(self):
        '''
        If the expiration date is more than 3 days from now, no alert will be displayed.
        '''
        user = User.objects.create_user(username='u')
        client = Client()
        client.force_login(user)
        date = timezone.now() + datetime.timedelta(days=10)
        food = Food.objects.create(food_name='f', user=user, date=date, pk=1)
        response = client.get(reverse('food_manager:food', args=(1,)))
        
        self.assertNotContains(response, '賞味期限が近づいています' or '賞味期限を過ぎています')

    def test_date_alert_within_3days(self):
        '''
        If the expiration date is within 3 days, an alert will be displayed
        indicating that the expiration date is approaching.
        '''
        user = User.objects.create_user(username='u')
        client = Client()
        client.force_login(user)
        date = timezone.now() + datetime.timedelta(days=3)
        food = Food.objects.create(food_name='f', user=user, date=date, pk=1)
        response = client.get(reverse('food_manager:food', args=(1,)))
        
        self.assertContains(response, '賞味期限が近づいています')
        self.assertNotContains(response, '賞味期限を過ぎています')

    def test_date_alert_expired(self):
        '''
        If the expiration date has passed, an alert indicating that the expiration date has passed is displayed.
        '''
        user = User.objects.create_user(username='u')
        client = Client()
        client.force_login(user)
        date = timezone.now() + datetime.timedelta(days=-1)
        food = Food.objects.create(food_name='f', user=user, date=date, pk=1)
        response = client.get(reverse('food_manager:food', args=(1,)))
        
        self.assertContains(response, '賞味期限を過ぎています')
        self.assertNotContains(response, '賞味期限が近づいています')