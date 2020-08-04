from django.views import generic

from .models import Post


class IndexView(generic.ListView):
    template_name = 'posts/index.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        return Post.objects.all().order_by('-pub_date')


class DetailView(generic.DetailView):
    template_name = 'posts/detail.html'
    model = Post
