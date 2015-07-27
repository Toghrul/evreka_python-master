from django.db import models
from fields import AutoSlugField
from django.contrib.auth.models import User
import evreka.settings
from datetime import date
settings = evreka.settings
class RecentManager(models.Manager):
    """
    Returns a specific number of the most recent public Articles as defined by 
    the NEWS_NUM_RECENT setting.
    """
    def get_query_set(self):
        num_recent = getattr(settings, 'NEWS_NUM_RECENT', 10)
        return super(RecentManager, self).get_query_set().filter(is_public=True)[:num_recent]

class PublicManager(models.Manager):
    """
    Returns only the articles where is_public is True.
    """
    def get_query_set(self):
        return super(PublicManager, self).get_query_set().filter(is_public=True)

class Article(models.Model):
    """
    News Article.
    """
    title = models.CharField(max_length=250, verbose_name="Turkish Title")
    title_eng = models.CharField(max_length=250, verbose_name="English Title",blank=True, null=True)
    slug = AutoSlugField(populate_from='title', overwrite_on_save=True)
    body = models.TextField(help_text="This part will be shown in Turkish",verbose_name="Body (TR)")
    body_eng = models.TextField(blank=True,null=True, help_text="This part will be shown in English", verbose_name="Body (ENG)")
    author = models.ForeignKey(User, null=True, blank=True)
    is_public = models.BooleanField(default=True, help_text='When checked, the article is visible on the site.')
    date_created = models.DateTimeField(auto_now_add=True)
    news_image = models.ImageField(upload_to= 'news_images/', null=False, blank=False)


    objects = models.Manager()
    recent = RecentManager()
    public = PublicManager()

    @models.permalink
    def get_absolute_url(self):
        return ('news_detail', (), {
            'year':self.date_created.year,
            'month':self.date_created.month,
            'day':self.date_created.day,
            'slug':self.slug
        })
    
    def __str__(self):
        return str(self.title_eng)
        
    class Meta:
        ordering = ['-date_created','-id']
        get_latest_by = 'date_created'
