import json
from json.decoder import JSONDecodeError
from typing import KeysView
from django.views import View
from django.http  import JsonResponse
from users.utils  import login_decorator
from posts.models import Post
from users.models import User


class PostDetailView(View):
    def get(self, request, post_id):
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"MESSAGE": "POST DOES NOT EXIST"}, status=404)
        
        post = Post.objects.select_related('author').get(id=post_id)
        
        post_list = {
            "title": post.title,
            "author": post.author.name,
            "user_id": post.author.id,
            "content": post.content,
            "written": post.created_at.strftime('%Y.%m.%d %H:%M')
        }
        
        return JsonResponse({"RESULT": post_list}, status=200)

class PostListView(View):
    def get(self, request):
        posts = Post.objects.select_related('author').order_by('-created_at')
        OFFSET = request.GET.get('page', 1)
        LIMIT = 20

        if int(OFFSET) <= 0:
            return JsonResponse({"MESSAGE": "MUST START WITH GREATER THAN 0"}, status=404)
        
        START = (int(OFFSET)-1) * LIMIT

        post_list = [{
            "title": post.title,
            "author": post.author.name,
            "written": post.created_at.strftime('%Y.%m.%d %H:%M'),
            "post_id": post.id,
            "user_id": post.author.id,
        }for post in posts[START:START+LIMIT]]

        return JsonResponse({
            "RESULT": {
                "data": post_list,
                "post_count": len(post_list)
            }
        }, status=200)

class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            if data["title"].strip() == "":
                return JsonResponse({"MESSAGE": "TITLE MUST CONTAIN WORDS"}, status=404)
            
            if data["content"].strip() == "":
                return JsonResponse({"MESSAGE": "MUST CONTAIN WORDS"}, status=404)    
            elif len(data["content"].strip()) <= 10:
                return JsonResponse({"MESSAGE": "NEED_MORE_THAN_10_WORDS"}, status=404)
            
            user_id = request.user.id
            
            Post.objects.create(
                title     = data['title'],
                content   = data['content'],
                author_id = user_id
            )
            
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
        except JSONDecodeError:
            return JsonResponse({"message": "INVALID DATA FORMAT"}, status=400)

class PostManageView(View):
    @login_decorator
    def delete(self, request, post_id):
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"MESSAGE": "POST DOES NOT EXIST"}, status=404)
        
        post = Post.objects.get(id=post_id)
        id = request.user.id
        
        if post.author.id == id:
            post.delete()
        else:
            return JsonResponse({"MESSAGE": "INVALID USER"}, status=403)

        return JsonResponse({"MESSAGE": "SUCCESSFULLY DELETED"}, status=204)

    @login_decorator
    def patch(self, request, post_id):
        try:
            data = json.loads(request.body)
            
            try:
                title = data["title"]
            except:
                title = False
            try:
                content = data["content"]
            except:
                content = False
            
            if content:
                if data["content"].strip() == "":
                    return JsonResponse({"MESSAGE": "MUST CONTAIN WORDS"}, status=404)    
                elif len(data["content"].strip()) <= 10:
                    return JsonResponse({"MESSAGE": "NEED_MORE_THAN_10_WORDS"}, status=404)
            
            if title:
                if data["title"].strip() == "":
                    return JsonResponse({"MESSAGE": "TITLE MUST CONTAIN WORDS"}, status=404)
            
            if not Post.objects.filter(id=post_id).exists():
                return JsonResponse({"MESSAGE": "POST DOES NOT EXIST"}, status=404)
            
            post = Post.objects.get(id=post_id)
            id = request.user.id
            
            if post.author.id == id:
                if content and title:
                    post.content = content
                    post.title   = title
                elif not content and title:
                    post.title = title
                elif not title and content:
                    post.content = content
                
                post.save()
            else:
                return JsonResponse({"MESSAGE": "INVALID USER"}, status=404)
            
            return JsonResponse({"MESSAGE": "SUCCESSFULLY UPDATED"}, status=201)
        
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=404)
        except JSONDecodeError:
            return JsonResponse({"message": "INVALID DATA FORMAT"}, status=400)