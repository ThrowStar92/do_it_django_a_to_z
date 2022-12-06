from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from.models import Post, Category , Tag ,Comment

admin.site.register(Post , MarkdownxModelAdmin)
admin.site.register(Comment)
# 슬러그 생성을 위한 클래스 추가
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields =  {'slug': ('name',)}



admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
