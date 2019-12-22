from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import BlogPostForm

def get_posts(request):
    """ Creates a list that returns a list of posts that were
    published prior to now. """

    posts = Post.object.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, "blogposts.html", {'posts': posts})


def post_detail(request, pk):
    """ Create a view that returns a single post object
    based on the ID (pk) and render it to the post detail.html
    template. Or return error if not found. """

    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    return render(request, "postdetail.html", {'post': post})


def create_or_edit_post(request, pk=None):
    """ Create a view that allows us to create or edit a post,
    depending on if the post id is null or not """

    post = get_object_or_404(Post, pk=pk) if pk else None
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blogpostform.html', {'form': form})




