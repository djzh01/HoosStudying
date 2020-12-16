from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from .models import Profile, Event, Post, Comment, Group
from .views import ScheduleView, PostCreateView, PostView, PostsListView
import datetime
from django.utils import timezone
from django.urls import reverse

# Test user data


class profileData(TestCase):
    def test_user_creation(self):
        user1 = User.objects.create_user(username = 'testuser1', email = "lol@gmail.com", password = 'N&6@F.NXcD')
        user2 = User.objects.create_user(username = 'testuser2', email = "lol2@gmail.com", password = '8JX.bnS{n8')

        self.assertEqual(user1.username, "testuser1")
        self.assertFalse(user2.username == user1.username)
        # self.assertEqual(user1.username, "testuser1")
        self.assertEqual(user2.username ,user2.username)
        self.assertEqual(User.objects.get_by_natural_key('testuser1'), user1)
        self.assertEqual(User.objects.get_by_natural_key('testuser2'), user2)

    def test_profile_creation(self):
        user1 = User.objects.create_user(username = 'testuser1', email = "lol@gmail.com", password = 'N&6@F.NXcD')
        user2 = User.objects.create_user(username = 'testuser2', email = "lol2@gmail.com", password = '8JX.bnS{n8')
        # Profile.objects.create(user = user1, major = "Computer Science", year = "2nd", max_group_size = "4")
        self.assertEqual(user1.profile.year, "First")
        self.assertEqual(user1.profile.major, "Enter Major")
        self.assertFalse(user2.profile.major == " Wrong Major")
        self.assertEqual(user1.profile.max_group_size, "Two")

    def test_profile_edit(self):
        user1 = User.objects.create_user(username = 'testuser1', email = "lol@gmail.com", password = 'N&6@F.NXcD')
        user2 = User.objects.create_user(username = 'testuser2', email = "lol2@gmail.com", password = '8JX.bnS{n8')
        user1.profile.major = "Computer Science"
        user2.profile.major = "English"
        user1.profile.max_group_size = "2"
        user2.profile.max_group_size = "3"
        self.assertEqual(user1.profile.major, "Computer Science")
        self.assertEqual(user2.profile.major, "English")
        self.assertEqual(user1.profile.max_group_size, "2")
        self.assertEqual(user2.profile.max_group_size, "3")

# Create your tests here.quit
def create_event(user, event_name, event_description, length):
    time = timezone.now() + datetime.timedelta(hours=length)
    return Event.objects.create(user=user, event_name=event_name, event_description=event_description,
                                event_start_time=timezone.now(), event_end_time=time, event_date=timezone.localdate())


class ScheduleTests(TestCase):
    def test_event_creation(self):
        user1 = User.objects.create_user(username='testuser1', email="lol@gmail.com", password='N&6@F.NXcD')
        user2 = User.objects.create_user(username='testuser2', email="lol2@gmail.com", password='8JX.bnS{n8')
        event = create_event(user1, '', '', 2)
        self.assertEqual(event.user, user1, "Should be user 1")
        self.assertIsNot(event.user, user2, "Should not be user 2")


class ScheduleIndexViewTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='testuser1', email="lol@gmail.com", password='N&6@F.NXcD')
        user2 = User.objects.create_user(username='testuser2', email="lol2@gmail.com", password='8JX.bnS{n8')

        user1.save()
        user2.save()

        event1 = create_event(user1, 'testuser1event1', 'testevent1', 1)
        event2 = create_event(user1, 'testuser1event2', 'testevent2', 2)
        event3 = create_event(user2, 'testuser2event1', 'testevent3', 3)

    def test_response(self):
        request = RequestFactory().get('/schedule')
        view_class = ScheduleView()
        request.user = User()
        response = ScheduleView.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, 200)

    def test_logged_in_shows_events_user1(self):
        login = self.client.login(username='testuser1', password='N&6@F.NXcD')
        response = self.client.get(reverse('SBFapp:schedule'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser1event1', response.context['calendar'])
        self.assertIn('testuser1event2', response.context['calendar'])
        self.assertNotIn('testuser2event1', response.context['calendar'])

    def test_logged_in_shows_events_user2(self):
        login = self.client.login(username='testuser2', password='8JX.bnS{n8')
        response = self.client.get(reverse('SBFapp:schedule'))
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser2event1', response.context['calendar'])
        self.assertNotIn('testuser1event2', response.context['calendar'])

    def test_get_event_detail(self):
        user1 = User.objects.create_user(username='testuserupdate', email="lol@gmail.com", password='N&6@F.NXcD')
        event3 = create_event(user1, 'testuser1event3', 'testevent1', 1)
        login = self.client.login(username='testuserupdate', password='N&6@F.NXcD')
        response = self.client.get(reverse('SBFapp:event_detail', args=(event3.id,)), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_update_event(self):
        user1 = User.objects.create_user(username='testuserupdate', email="lol@gmail.com", password='N&6@F.NXcD')
        event3 = create_event(user1, 'testuser1event3', 'testevent1', 1)
        login = self.client.login(username='testuserupdate', password='N&6@F.NXcD')
        response = self.client.post(reverse('SBFapp:event_edit', args=(event3.id,)), data={'event_name': 'newname'}, follow=True)
        self.assertEqual(response.status_code, 200)
        # try assert redirects

def create_post(user, post_title,post_type, post_content):
    return Post.objects.create(user=user, post_title=post_title, post_type=post_type,
                                post_content=post_content)
class CommunityTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='testuser1', email="lol@gmail.com", password='N&6@F.NXcD')
        user2 = User.objects.create_user(username='testuser2', email="lol2@gmail.com", password='8JX.bnS{n8')
        post1 = create_post(user1,'testpost1','help','postcontent')
        post2 = create_post(user1,'testpost2','find','postcontent')
        post3 = create_post(user2,'testpost3','find','postcontent')
    def test_view_all_posts(self):
        login = self.client.login(username='testuser2', password='8JX.bnS{n8')
        response = self.client.get(reverse('SBFapp:community'))
        self.assertQuerysetEqual(response.context['latest_post_list'].order_by('id'),['<Post: testpost1>','<Post: testpost2>','<Post: testpost3>'])
    def test_view_help_posts(self):
        login = self.client.login(username='testuser2', password='8JX.bnS{n8')
        response = self.client.get('/community/?post_type=help')
        print(response)
        self.assertQuerysetEqual(response.context['latest_post_list'].order_by('id'),['<Post: testpost1>'])
    def test_view_buddy_posts(self):
        login = self.client.login(username='testuser2', password='8JX.bnS{n8')
        response = self.client.get('/community/?post_type=find')
        self.assertQuerysetEqual(response.context['latest_post_list'].order_by('id'),['<Post: testpost2>','<Post: testpost3>'])

class PostTest(TestCase):
    def test_post_creation(self):
        user1 = User.objects.create_user(username='testuser1', email="lol@gmail.com", password='N&6@F.NXcD')
        user2 = User.objects.create_user(username='testuser2', email="lol2@gmail.com", password='8JX.bnS{n8')
        post1 = create_post(user1,'testpost1','help','postcontent')
        self.assertEqual(post1.user, user1)
        self.assertIsNot(post1.user, user2)
    def test_post_attributes(self):
        user1 = User.objects.create_user(username='testuser1', email="lol@gmail.com", password='N&6@F.NXcD')
        user2 = User.objects.create_user(username='testuser2', email="lol2@gmail.com", password='8JX.bnS{n8')
        post1 = create_post(user1,'testpost1','help','postcontent')
        response = self.client.get(reverse('SBFapp:post',kwargs={'pk':1}))
        self.assertEqual(post1.post_title,'testpost1')
        self.assertEqual(post1.post_content,'postcontent')
        self.assertEqual(post1.post_type,'help')
    def test_undefined_post(self):
        response = self.client.get(reverse('SBFapp:post',kwargs={'pk':1}))
        self.assertEqual(response.status_code,302)
        

def comment(user, text, post):
    return Comment.objects.create(user=user, text=text,post=post)
    
class CommentTest(TestCase):
    def test_create_comment(self):
        user1 = User.objects.create_user(username='testuser1', email="lol@gmail.com", password='N&6@F.NXcD')
        user2 = User.objects.create_user(username='testuser2', email="lol2@gmail.com", password='8JX.bnS{n8')
        post1 = create_post(user1,'testpost1','help','postcontent')
        comment1 = comment(user1,'commentcontent',post1)
        self.assertEqual(comment1.post,post1)
        self.assertEqual(comment1.user,user1)
        self.assertIsNot(comment1.user,user2)
    def test_comment_text(self):
        user1 = User.objects.create_user(username='testuser1', email="lol@gmail.com", password='N&6@F.NXcD')
        user2 = User.objects.create_user(username='testuser2', email="lol2@gmail.com", password='8JX.bnS{n8')
        post1 = create_post(user1,'testpost1','help','postcontent')
        comment1 = comment(user1,'commentcontent',post1)
        response = self.client.get(reverse('SBFapp:post',kwargs={'pk':1}))
        self.assertEqual(comment1.text,'commentcontent')

def create_group(user,group_name,group_descr):
    return Group.objects.create(user=user,group_name=group_name,group_descr=group_descr, private=False)
class GroupTest(TestCase):
    def test_create_group(self):
        user1 = User.objects.create_user(username='testuser1', email="lol@gmail.com", password='N&6@F.NXcD')
        user2 = User.objects.create_user(username='testuser2', email="lol2@gmail.com", password='8JX.bnS{n8')
        group1 = create_group(user1,'testgroup1','groupdescr')
        self.assertEqual(group1.user, user1)
        self.assertIsNot(group1.user, user2)
    def test_view_group(self):
        user1 = User.objects.create_user(username='testuser1', email="lol@gmail.com", password='N&6@F.NXcD')
        user2 = User.objects.create_user(username='testuser2', email="lol2@gmail.com", password='8JX.bnS{n8')
        group1 = create_group(user1,'testgroup1','groupdescr')
        response = self.client.get(reverse('SBFapp:group',kwargs={'pk':1}))
        self.assertEqual(group1.group_name,'testgroup1')
        self.assertEqual(group1.group_descr,'groupdescr')
    def test_join_group(self):
        a=1
    def test_undefined_group(self):
        response = self.client.get(reverse('SBFapp:group',kwargs={'pk':1}))
        self.assertEqual(response.status_code,302)

class RoomTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='testuser1', email="lol@gmail.com", password='N&6@F.NXcD')
        user1.save()
      
    def test_logged_in_shows_room_user1(self):
        login = self.client.login(username='testuser1', password='N&6@F.NXcD')
        response = self.client.get(reverse('SBFapp:room', args = "t"))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

class VideoTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='testuser1', email="lol@gmail.com", password='N&6@F.NXcD')
        user1.save()
  
    def test_logged_in_shows_video_user1(self):
        login = self.client.login(username='testuser1', password='N&6@F.NXcD')
        response = self.client.get(reverse('SBFapp:video', args = "t"))
        self.assertEqual(response.status_code, 200)
