from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Post
from .forms import PostForm, PageForm
from .forms import UploadFileForm
import json
import requests

from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    # if request.method == "POST":
    #     form = PostForm(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.author = request.user
    #         post.save()
    #         return redirect('post_detail', pk=post.pk)
    # else :
    #     form = PostForm()
    form = PageForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # if request.method == "POST":
    #     form = PostForm(request.POST, instance=post)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.author = request.user
    #         post.save()
    #         return redirect('post_detail', pk=post.pk)
    # else:
    #     form = PostForm(instance=post)

    form = PageForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fileModel = form.save()
            return HttpResponse(json.dumps({
                "uploadPath": 'media' + '/' + fileModel.file.name
            }).encode('utf8'))
        else:
            form = UploadFileForm({})
        return JsonResponse({
            "uploadPath": ''
        })

@csrf_exempt
def import_doc(request):
    if request.method == "POST":
        docFile = request.FILES['docFile']
        fs = FileSystemStorage()
        doc = fs.save('docs/' + docFile.name, docFile)
        response = requests.post("http://synapeditor.iptime.org:7419/importDoc", files = {'docFile': doc})
        return HttpResponse(response.text)
