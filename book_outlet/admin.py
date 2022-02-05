from django.contrib import admin

from .models import Book,Author,Address,Country

# Register your models here.

class BookAdmin(admin.ModelAdmin): #allows to set various options/properties that refelct in admin page
    #readonly_fields = ("slug",) #makes our field readonly
    prepopulated_fields ={"slug":("title",)} #prepoluate the fields before creating and saving in admin page
        #how does django knows to prepopulate the fields??
            # if we consider slug field; it uses SlugField by calling slugify
    list_filter=("author","rating",) #to set filters
            #the above filters by author and rating
    list_display =("title","author",) #displaying of books in admin panel
admin.site.register(Book,BookAdmin)
admin.site.register(Author)
admin.site.register(Address)
admin.site.register(Country)