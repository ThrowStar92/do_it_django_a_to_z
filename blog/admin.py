from django.contrib import admin

from.models import Post, Category , Tag

admin.site.register(Post)

# 슬러그 생성을 위한 클래스 추가
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields =  {'slug': ('name',)}



admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
