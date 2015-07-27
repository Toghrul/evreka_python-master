from django.contrib import admin
from models import Article

class ArticleAdmin(admin.ModelAdmin):
	list_fields = ['title','title_eng' 'author', 'date_created', 'is_public']

admin.site.register(Article, ArticleAdmin)