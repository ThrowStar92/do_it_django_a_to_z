from django.contrib import admin

from.models import Post, Category

admin.site.register(Post)

# 슬러그 생성을 위한 클래스 추가
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
admin.site.register(Category, CategoryAdmin)
