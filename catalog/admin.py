from django.contrib import admin
from catalog import models

# admin.site.register(models.Author)
# admin.site.register(models.Book)
# admin.site.register(models.BookInstance)
# admin.site.register(models.Genre)

class BookInline(admin.TabularInline):
    model = models.Book
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','date_of_birth','date_of_death',]
    fields = ['first_name','last_name',('date_of_birth','date_of_death'),]
    inlines = [ BookInline ]
admin.site.register(models.Author, AuthorAdmin)

class BookIntanceInline(admin.TabularInline):
    model = models.BookInstance
    extra = 0

@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title','author','display_genre',]
    inlines = [ BookIntanceInline ]

@admin.register(models.BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ['book', 'status', 'due_back', 'id']

    fieldsets = (
        (None, {
            'fields' : ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields' : ('status', 'due_back')
        }),
    )

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    pass
