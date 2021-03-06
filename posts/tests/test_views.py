
from django.test import TestCase
from django.urls import reverse 

from posts.models import Blogger , Blog 
from django.contrib.auth.models import User

class BlogListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_bloggers = 13

        for blogger_id in range(number_of_bloggers):

            
            user= User.objects.create_user(f'user{blogger_id}', 'myemail@crazymail.com', 'mypassword')
              
            user.save()
            

            Blog.objects.create(title = f'Test title {blogger_id}',
            content =  f'Test content {blogger_id}',
            user = Blogger.objects.get(id = blogger_id +1)

             )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/posts/blogs/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/blog_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blog_list']) == 10)

    def test_lists_all_bloggers(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('blogs')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blog_list']) == 3)

    

        
    

class BloggerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_bloggers = 13

        for blogger_id in range(number_of_bloggers):

             User.objects.create_user(f'user{blogger_id}', 'myemail@crazymail.com', 'mypassword')
            

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/posts/bloggers/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/blogger_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blogger_list']) == 10)

    def test_lists_all_bloggers(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('bloggers')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blogger_list']) == 3)




class BlogsByLoggedInUserListViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        blogger1 = test_user1.blogger
        blogger2 = test_user2.blogger

        blogger1.save()
        blogger2.save()

        number_of_blogs = 30

        for blogs in range(number_of_blogs):
            Blog.objects.create(
                title = blogs,
                user = blogger2,
                content = 'This is content'
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-blog'))
        self.assertRedirects(response, '/accounts/login/?next=/posts/myblog')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-blog'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'posts/blogs_by_user_loggedIn.html')

    def test_pagination_is_ten(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('my-blog'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blog_list']) == 10)



    def test_only_user_blogs_in_list(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-blog'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        self.assertTrue('blog_list' in response.context)
        self.assertEqual(len(response.context['blog_list']), 0)

        self.assertEqual(str(response.context['user']), 'testuser1')

        self.assertEqual(response.status_code, 200)

        login2 = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

        response = self.client.get(reverse('my-blog'))

        self.assertTrue('blog_list' in response.context)
        self.assertEqual(len(response.context['blog_list']), 10)


class BlogCreateViewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        
        # blogger1 = Blogger.objects.create(user=test_user1,biography='test1')

        # blogger1.save()



    def notLoggedInRedirect(self):
        response = self.client.get(reverse('blog-create'))
        self.assertTrue( response.status_code, 200)
        self.assertRedirects(response, '/accounts/login/?next=/posts/blog/create/')

    def notLoggedInPostAttemptForbidden(self):
        response = self.client.post(reverse('blog-create'))
        self.assertTrue(response.status_code, 403)

    def loggedInStatus200 (self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('blog-create'))
        self.assertTrue( response.status_code, 200)

    def loggedInCorrectTemplate (self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('blog-create'))
        self.assertTrue( response.status_code, 200)
        self.assertTemplateUsed(response , 'blog_form.html') 

    def checkFormFields (self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('blog-create'))
        form = response.context['form']
       
        
        self.assertEquals( form.fields['title'].label , 'title')

        self.assertEquals( form.fields['content'].label , 'content')

        self.assertEquals( form.fields['post_date'].label , 'post date')

     

    def checkFormFilledWithLoggedInUser(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('blog-create'))
        form = response.context['form']

        self.assertEquals (form.fields['user'] , Blogger.objects.get(self.user.id))

    def test_redirect_if_post_logged_in (self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('blog-create'), {'title':'Title', 'content':'Fake Post'})
        self.assertAlmostEqual(response.status_code, 302)

        self.assertRedirects(response, '/posts/blogs/1')
