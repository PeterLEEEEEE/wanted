import re
from django.http import response
import jwt
import json 
import unittest
from django.test import TestCase, Client, client
from users.models import User 
from posts.models import Post
from my_settings import ALGORITHM, SECRET_KEY

class PostTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            name     = "peter",
            email    = "dissgogo@gmail.com",
            password = "dlangus1234!",
        )
        
        self.token1 = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, algorithm = ALGORITHM)
        
        User.objects.create(
            id       = 2,
            name     = "kim",
            email    = "kimkim@naver.com",
            password = "iamkim123123!",
        )
        
        self.token2 = jwt.encode({'id': User.objects.get(id=2).id}, SECRET_KEY, algorithm = ALGORITHM)
        
        Post.objects.create(
            id      = 1,
            title   = "title for post1",
            content = "this is peter's post",
            author_id  = User.objects.get(id = 1).id,
        )

        Post.objects.create(
            id      = 2,
            title   = "title for post2",
            content = "this is peter's second post",
            author_id  = User.objects.get(id = 1).id,
        )

        Post.objects.create(
            id      = 3,
            title   = "title for post3",
            content = "this is peter's third post",
            author_id  = User.objects.get(id = 1).id,
        )

    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()
    
    def test_create_newpost_post_success(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['id'])
        
        newpost = {
            "id"     : 4,
            "title"  : "title for post1",
            "content": "this is kim's first post",
            "author" : User.objects.get(id = user.id).id
        }
        
        response = client.post('/posts/newpost', json.dumps(newpost), **header, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS"})

    def test_create_newpost_post_keyerror(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['id'])
        
        newpost = {
            "id"     : 4,
            "content": "this is kim's first post",
            "author" : User.objects.get(id = user.id).id
        }
        
        response = client.post('/posts/newpost', json.dumps(newpost), **header, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "KEY_ERROR"})
    
    def test_create_newpost_post_jsondecodeerror(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['id'])
        
        response = client.post('/posts/newpost', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID DATA FORMAT"})

    def test_create_newpost_post_title_no_word(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['id'])
        
        newpost = {
            "id"     : 4,
            "title"  : " ",
            "content": "this is kim's first post",
            "author" : User.objects.get(id = user.id).id
        }
        
        response = client.post('/posts/newpost', json.dumps(newpost), **header, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "TITLE MUST CONTAIN WORDS"})

    def test_create_newpost_post_content_no_word(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['id'])
        
        newpost = {
            "id"     : 4,
            "title"  : "title for post1",
            "content": "      ",
            "author" : User.objects.get(id = user.id).id
        }
        
        response = client.post('/posts/newpost', json.dumps(newpost), **header, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "MUST CONTAIN WORDS"})
    
    def test_create_newpost_post_content_too_short(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['id'])
        
        newpost = {
            "id"     : 4,
            "title"  : "title for post1",
            "content": "tooshort",
            "author" : User.objects.get(id = user.id).id
        }
        
        response = client.post('/posts/newpost', json.dumps(newpost), **header, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "NEED_MORE_THAN_10_WORDS"})
    
    def test_post_delete_success(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        response = client.delete('/posts/post/manage/1', **header)
        self.assertEqual(response.status_code, 204)
    
    def test_post_delete_does_not_exist(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        response = client.delete('/posts/post/manage/111', **header)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "POST DOES NOT EXIST"})
    
    def test_post_delete_invalid_user(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        
        response = client.delete('/posts/post/manage/1', **header)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"MESSAGE": "INVALID USER"})
    
    def test_post_update_success(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        update_post = {
            "title": "update peter's post1",
            "content": "update peter's title",
        }

        response = client.patch('/posts/post/manage/1', json.dumps(update_post), **header, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESSFULLY UPDATED"})
    
    def test_post_update_content_no_word(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        update_post = {
            "title": "update peter's post1",
            "content": "   ",
        }

        response = client.patch('/posts/post/manage/1', json.dumps(update_post), **header, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "MUST CONTAIN WORDS"})
    
    def test_post_update_content_too_short(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        update_post = {
            "title": "update peter's post1",
            "content": "tooshort",
        }

        response = client.patch('/posts/post/manage/1', json.dumps(update_post), **header, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "NEED_MORE_THAN_10_WORDS"})
    
    def test_post_update_title_no_word(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        update_post = {
            "title": "    ",
            "content": "update peter's title",
        }

        response = client.patch('/posts/post/manage/1', json.dumps(update_post), **header, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "TITLE MUST CONTAIN WORDS"})
    
    def test_post_update_post_not_exist(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        update_post = {
            "title": "update peter's post1",
            "content": "update peter's title",
        }

        response = client.patch('/posts/post/manage/111', json.dumps(update_post), **header, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "POST DOES NOT EXIST"})
    
    def test_post_update_jsondecodeerror(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token1}
        
        response = client.patch('/posts/post/manage/1', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID DATA FORMAT"})
    
    def test_post_update_invalid_user(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token2}
        
        update_post = {
            "title": "update peter's post1",
            "content": "hihihihihihihi",
        }

        response = client.patch('/posts/post/manage/1', json.dumps(update_post),**header, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "INVALID USER"})
    
    def test_postdetail_get_success(self):
        client = Client()
        response = client.get('/posts/post/1')

        written = Post.objects.get(id=1).created_at.strftime('%Y.%m.%d %H:%M')

        test = {
            "RESULT": {
                "title"   : "title for post1",
                "author"  : "peter",
                "content" : "this is peter's post",
                "user_id" : 1,
                "written" : written
            }
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test)
    
    def test_postdetail_get_post_not_exist(self):
        client = Client()
        response = client.get('/posts/post/111')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "POST DOES NOT EXIST"})
    
    def test_postlist_get_success(self):
        client = Client()
        response = client.get('/posts/main')
        written1 = Post.objects.get(id=1).created_at.strftime('%Y.%m.%d %H:%M')
        written2 = Post.objects.get(id=2).created_at.strftime('%Y.%m.%d %H:%M')
        written3 = Post.objects.get(id=3).created_at.strftime('%Y.%m.%d %H:%M')
        
        test = {
            "RESULT": {
                "data":[
                    {
                        "title": "title for post3",
                        "author": "peter",
                        "written": written3,
                        "post_id": 3,
                        "user_id": 1,
                    },
                    {
                        "title": "title for post2",
                        "author": "peter",
                        "written": written2,
                        "post_id": 2,
                        "user_id": 1,
                    },
                    {
                        "title": "title for post1",
                        "author": "peter",
                        "written": written1,
                        "post_id": 1,
                        "user_id": 1,
                    }
                ],
                "post_count": 3,
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test)

    def test_postlist_get_page_number_negative(self):
        client = Client()
        response = client.get('/posts/main?page=-2')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "MUST START WITH GREATER THAN 0"})