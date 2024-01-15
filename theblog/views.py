from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView #builtin query functions
from .models import Post, Category, Comment #calling model Post
from .forms import PostForm, EditForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

#def home(request):
	#return render(request, 'home.html', {})

def LikeView(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked = False
	else: 
		post.likes.add(request.user)
		liked = True

	return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        cat_menu2 = Category.objects.all()[:6]

        single_post = Post.objects.all().order_by('-post_date')[:1]
        two_posts = Post.objects.all().order_by('-post_date')[1:2]
        one_posts2 = Post.objects.all().order_by('-post_date')[2:3]
        two_posts1 = Post.objects.all().order_by('-post_date')[3:5]
        five_posts = Post.objects.all().order_by('-post_date')[5:10]

        single_posts5 = Post.objects.filter(category__name='Tech').order_by('-post_date')[:1]
        single_posts7 = Post.objects.filter(category__name='Tech').order_by('-post_date')[1:2]
        single_posts8 = Post.objects.filter(category__name='Tech').order_by('-post_date')[2:3]
        single_posts9 = Post.objects.filter(category__name='Tech').order_by('-post_date')[3:4]
        single_posts10 = Post.objects.filter(category__name='Tech').order_by('-post_date')[4:5]

        single_posts11 = Post.objects.filter(category__name='Africa News').order_by('-post_date')[0:1]
        single_posts12 = Post.objects.filter(category__name='Africa News').order_by('-post_date')[1:2]
        single_posts13 = Post.objects.filter(category__name='Africa News').order_by('-post_date')[2:3]
        single_posts14 = Post.objects.filter(category__name='Africa News').order_by('-post_date')[3:4]
        single_posts15 = Post.objects.filter(category__name='Africa News').order_by('-post_date')[4:5]

        single_posts16 = Post.objects.filter(category__name='World Topic').order_by('-post_date')[0:1]
        single_posts17 = Post.objects.filter(category__name='World Topic').order_by('-post_date')[1:2]
        single_posts18 = Post.objects.filter(category__name='World Topic').order_by('-post_date')[2:3]
        single_posts19 = Post.objects.filter(category__name='World Topic').order_by('-post_date')[3:4]
        single_posts20 = Post.objects.filter(category__name='World Topic').order_by('-post_date')[4:5]
        single_posts6 = Post.objects.filter(category__name='Tv Shows').order_by('-post_date')[:3]

        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        context["cat_menu2"] = cat_menu2
        context["single_post"] = single_post
        context["two_posts"] = two_posts
        context["one_posts2"] = one_posts2
        context["two_posts1"] = two_posts1
        context["five_posts"] = five_posts
        context["single_posts5"] = single_posts5
        context["single_posts7"] = single_posts7
        context["single_posts6"] = single_posts6
        context["single_posts8"] = single_posts8
        context["single_posts9"] = single_posts9
        context["single_posts10"] = single_posts10
        context["single_posts11"] = single_posts11
        context["single_posts12"] = single_posts12
        context["single_posts13"] = single_posts13
        context["single_posts14"] = single_posts14
        context["single_posts15"] = single_posts15
        context["single_posts16"] = single_posts16
        context["single_posts17"] = single_posts17
        context["single_posts18"] = single_posts18
        context["single_posts19"] = single_posts19
        context["single_posts20"] = single_posts20
        return context



def CategoryListView(request):
	cat_menu_list = Category.objects.all()
	return render(request, 'category_list.html', {'cat_menu_list':cat_menu_list})

def CategoryView(request, cats):
    category = get_object_or_404(Category, name=cats.replace('-', ' ').title())
    category_posts = Post.objects.filter(category=category)
    return render(request, 'categories.html', {'cats': cats.title().replace('-', ' '), 'category_posts': category_posts})


class ArticleDetailView(DetailView):
	model = Post
	template_name = 'article_details.html'

	def get_context_data(self, *args, **kwargs):
		cat_menu = Category.objects.all()
		# Retrieve the current article using self.object
		article = self.object
		pull_related_post = Post.objects.filter(category=article.category).exclude(pk=article.id)[:3]
		context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
		

		stuff = get_object_or_404(Post, id=self.kwargs['pk'])
		total_likes = stuff.total_likes()

		liked = False
		if stuff.likes.filter(id=self.request.user.id).exists():
			liked = True

		context["cat_menu"] = cat_menu
		context["article"] = article
		context["pull_related_post"] = pull_related_post
		context["total_likes"] = total_likes
		context["liked"] = liked
		return context

class AddPostView(CreateView):
	model = Post
	form_class = PostForm
	template_name = 'add_post.html'
	#fields = '__all__' #//for selecting all fields 
	#fields = ('title', 'title_tag', 'body') #to select only title and body from model

	def get_context_data(self, *args, **kwargs):
		cat_menu = Category.objects.all()
		context = super(AddPostView, self).get_context_data(*args, **kwargs)
		context["cat_menu"] = cat_menu
		return context

class AddCommentView(CreateView):
	model = Comment
	form_class = CommentForm
	template_name = 'add_comment.html'
	#fields = '__all__' #//for selecting all fields 
	#fields = ('title', 'title_tag', 'body') #to select only title and body from model
	success_url = reverse_lazy('home') #change to redirect to aricle page

	def form_valid(self, form):
		form.instance.post_id = self.kwargs['pk']
		return super().form_valid(form)


class AddCategoryView(CreateView):
	model = Category
	
	#form_class = PostForm
	template_name = 'add_category.html'
	fields = '__all__' #//for selecting all fields 
	#fields = ('title', 'title_tag', 'body') #to select only title and body from model

	def get_context_data(self, *args, **kwargs):
		cat_menu = Category.objects.all()
		context = super(AddCategoryView, self).get_context_data(*args, **kwargs)
		context["cat_menu"] = cat_menu
		return context

class UpdatePostView(UpdateView):
	model = Post
	form_class = EditForm
	template_name = 'update_post.html'
	#fields = ['title', 'title_tag', 'body']

	def get_context_data(self, *args, **kwargs):
		cat_menu = Category.objects.all()
		context = super(UpdatePostView, self).get_context_data(*args, **kwargs)
		context["cat_menu"] = cat_menu
		return context

class DeletePostView(DeleteView):
	model = Post
	template_name = 'delete_post.html'
	success_url = reverse_lazy('home')

	def get_context_data(self, *args, **kwargs):
		cat_menu = Category.objects.all()
		context = super(DeletePostView, self).get_context_data(*args, **kwargs)
		context["cat_menu"] = cat_menu
		return context


def search(request):
	if request.method== "POST":
		search = request.POST['search']
		searched = Post.objects.filter(body__contains = search)
		return render(request, 'search.html', {'search':search, 'searched':searched})
	else:
		return render(request, 'search.html', {})