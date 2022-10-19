from django.contrib import admin
from Libsys.models import Language, Author, Book, Ebook, User, Publisher, HardBookInfo
class languageAdmin(admin.ModelAdmin):
      list_per_page = 20
      list_display=('language_id', 'name', 'script', 'about')
      list_display_links=['language_id']

class BookAdmin(admin.ModelAdmin):
      list_per_page = 20
      list_display=('book_id','name','author', 'language', 'publisher','book_type')
      raw_id_fields=['language', 'author', 'publisher']     
      search_fields=['author__name', 'language__name', 'name', 'category','publisher__pub_id'] 
      def author(self, obj):
            return "\n".join([author.author for author in obj.author.all()])
      def language(self, obj):
            return "\n".join([Lang.language for Lang in obj.language.all()])  

class AuthoAdmin(admin.ModelAdmin):
      list_per_page = 20
      list_display=('author_id', 'name', 'email_id', 'picture')
      list_display_links=['author_id']

class ebookAdmin(admin.ModelAdmin):
      list_per_page = 20
      list_display=('book_id', 'ebook', 'approval_status', 'book_location', 'uploaded_by')    
      search_fields=['ebook_id']

class userAdmin(admin.ModelAdmin):
      list_per_page = 20
      list_display=('user_id','first_name', 'email_id', 'mobile_no', 'aadhar_id','subscription', 'created_on', 'updated_on',
            'favourite', 'role')
      raw_id_fields=['favourite']
      def favourite(self, obj):
        return "\n".join([fav.favourite for fav in obj.favourite.all()])

class publisherAdmin(admin.ModelAdmin):
      list_per_page = 20
      list_display=('publisher_id', 'name', 'contact_details')               


class BookInfoAdmin(admin.ModelAdmin):
      list_per_page = 20
      list_display=('hardCopy_id', 'book_name', 'isLent', 'lentTo')
      raw_id_fields=['lentTo']


admin.site.register(Language, languageAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthoAdmin)
admin.site.register(Ebook, ebookAdmin)
admin.site.register(User ,userAdmin)
admin.site.register(Publisher ,publisherAdmin)
admin.site.register(HardBookInfo ,BookInfoAdmin)

