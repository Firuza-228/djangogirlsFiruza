from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.all()  # Получаем все статьи из базы данных
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)  # Получаем статью по id (pk)
    return render(request, 'blog/post_detail.html', {'post': post})