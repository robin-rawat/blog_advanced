from django.conf import settings
from django.utils import timezone
from django.db import models
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from django.urls import reverse 
from comments.models import Comment
from posts.utils import get_read_time
from django.contrib.contenttypes.models import ContentType


#class PostManager(models.Manager):
	#def all(self,*args,**kwargs):
		#return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())

#here we set our won location for saving of image
def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)
# Create your models here.
class Post(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	
	title = models.CharField(max_length=120)
	#slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field = "width_field", height_field ="height_field")
	height_field = models.IntegerField(default=100)
	width_field = models.IntegerField(default=100)
	content = models.TextField()
	draft = models.BooleanField(default=False)
	publish = models.DateTimeField(auto_now=False,auto_now_add=False)
	read_time = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	#objects = PostManager()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"pk":self.id})
		#return "/posts/%s" %(self.id)

	def get_markdown(self):
		content = self.content
		markdown_text = markdown(content)
		return mark_safe(markdown_text)

	def read_time_fxn(self):
		if self.content:
			html_string = self.get_markdown()
			read_time_var = get_read_time(html_string)
			self.read_time = read_time_var

	class Meta:
		ordering = ["-timestamp","-updated"]

	@property
	def comments(self):
		instance=self
		qs=Comment.objects.filter_by_instance(instance)
		return qs

	@property
	def get_content_type(self):
		instance=self		
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type