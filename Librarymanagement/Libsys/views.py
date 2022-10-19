from pickle import TRUE
from django.views.generic import View
from django.core.paginator import Paginator
import traceback
from .response import *

#Libsys import
from .constants import (LANGUAGE_SUCCESSFULLY_ADDED, LANGUAGE_DETAILS_FOUND, LANGUAGE_UPDATED_SUCCESSFULLY,
                        AUTHOR_SUCCESSFULLY_ADDED,AUTHOR_SUCCESSFULLY_FOUND, AUTHOR_DETAILS_UPDATED, AUTHOR_DETAILS_DELETED, AUTHOR_IMG_UPDATED,
                        AUTHOR_NOT_EXIST, 
                        BOOK_SUCCESSFULLY_ADDED,BOOK_DETAILS_FOUND, BOOK_DELETED, BOOK_INFO_FOUND, BOOK_ISSUED, BOOK_INFO_FOUND,
                        BOOK_STATUS_CHANGE, BOOK_LIMIT_EXCEED, BOOK_ISSUE_ERR,
                        USER_ADDED, USER_DETAILS_FOUND, USER_DETAILS_UPDATED, USER_DELETED, USER_SUBSCRIPTION_ERR, USER_NOT_EXIST,
                        USER_PERMISSION_DENIED, INVALID_USER_IDS, USER_EXIST_ERR,
                        PUBLISHER_ADDED, PUBLISHER_DETAILS_FOUND, PUBLISHER_DETAILS_UPDATED, PUBLISHER_DELETED, PUBLISHER_NOT_EXIST,
                        EBOOK_ADDED, EBOOK_DETAILS_FOUND, BOOK_LOCATION_UPDATED, EBOOK_DELETED,BOOK_DETAILS_NOT_FOUND,
                        FAVOURITE_BOOK_ADDED, MISSING_KEYS, MISSING_KEY_VALUE, LANGUAGE_EXIST, LANGUAGE_NOT_EXIST,
                        SUBSCRIPTION_ACTIVATED, SUBSCRIPTION_DEACTIVATED, INVALID_CHOICES, INVALID_ID, INVALID_IDS, EBOOK_ID_ERR, HARD_COPY_ID_ERR)

from .models import (Language, Author, Publisher, 
                    Book, HardBookInfo, Ebook, User ) 

from .exception import (FavouriteException, BookException, LanguageException,
                         AuthorException, PublisherException,
                        UserException, EbookException, HardBookInfoException, 
                        SubscriptionException, BookApprovalException )




class LanguageView(View):
    def __init__(self):
        self.response = init_response()

    def validate_language_name(self,language_name):
        language_list = Language.objects.all().values_list('name', flat=True)
        if language_name in language_list:
            raise LanguageException(LANGUAGE_EXIST) 

    def validate_language_ids(self, language_ids):
        language_objs = Language.objects.filter(language_id__in=language_ids)
        if not language_objs:
            raise LanguageException(LANGUAGE_NOT_EXIST)
    def validate_language_param_keys(self,params):
      
        missing_key=[]
        for key in ['name','script','about']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key       
        
    def validate_lang_value_params(self,params):
        keys=[]
        for key, value in params.items():
            if not value:
                keys.append(key)              
        return keys          

    def post(self, request):
        params = request.POST.dict()
        try:
            missing_key = self.validate_language_param_keys(params)
            if missing_key:
                raise LanguageException(MISSING_KEYS) 
            missing_key_value = self.validate_lang_value_params(params)
            if missing_key_value:
                raise LanguageException(MISSING_KEY_VALUE)
            language_name = params.get('name')
            self.validate_language_name(language_name)
            Language.objects.add_language_details(params)
            self.response['res_str'] = LANGUAGE_SUCCESSFULLY_ADDED
            return send_201(self.response)
        except LanguageException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key
            self.response['res_str'] = str(ex)
            return send_400(self.response)     
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)


    def validate_language_params(self,params):
        missing_key=[]
        key = 'language_id'
        if not key in params.keys():
            missing_key.append(key)   
        return missing_key    

        
    def get(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_language_params(params)
            if missing_key:
                raise LanguageException(MISSING_KEYS)
            missing_key_value = self.validate_lang_value_params(params)
            if missing_key_value:
                raise LanguageException(MISSING_KEY_VALUE)
            language_ids = params.get('language_id').strip().split(',')
            self.validate_language_ids(language_ids)
            language_details = Language.objects.get_langauge_details(language_ids)
            self.response['res_data'] = language_details
            self.response['res_str'] = LANGUAGE_DETAILS_FOUND
            return send_200(self.response)
        except LanguageException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key
            self.response['res_str'] = str(ex)
            return send_400(self.response)    
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

    def validate_language_params_keys(self,params):
        missing_key=[]
        for key in ['language_id','about','name','script']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key                         

    def put(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_language_params_keys(params)
            if missing_key:
                raise LanguageException(MISSING_KEYS)
            missing_key_value = self.validate_lang_value_params(params)
            if missing_key_value:
                raise LanguageException(MISSING_KEY_VALUE)
            language_id = params.get('language_id').strip().split(',')
            self.validate_language_ids(language_id)
            language_details = Language.objects.update_langauge_details(params)
            self.response['res_data'] = language_details
            self.response['res_str'] = LANGUAGE_UPDATED_SUCCESSFULLY 
            return send_200(self.response)
        except LanguageException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key
            self.response['res_str'] = str(ex)
            return send_400(self.response)        
        except Exception as ex:
            self.response['res_str'] =  traceback.format_exc()
            return send_400(self.response)          

class AuthorView(View):
    def __init__(self):
        self.response = init_response()

    def validate_author_ids(self,author_ids):
        author_objs = Author.objects.filter(author_id__in=author_ids)
        if not author_objs:
            raise AuthorException(AUTHOR_NOT_EXIST)

    def validate_author_param(self,params):
        missing_key = []
        for key in ['email_id','name']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key
                
    def validate_author_params_value(self,params):
        keys=[]
        for key, value in params.items():
            if not value:
                keys.append(key)              
        return keys 
       
    def post(self, request):
        params = request.POST.dict()
        try:
            missing_key = self.validate_author_param(params)
            if missing_key:
                raise AuthorException(MISSING_KEYS)
            missing_key_value = self.validate_author_params_value(params)
            if missing_key_value:
                raise AuthorException(MISSING_KEY_VALUE)
            author_image = request.FILES['picture']
            Author.objects.add_author(params,author_image)
            self.response['res_str'] = AUTHOR_SUCCESSFULLY_ADDED
            return send_201(self.response)
        except AuthorException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

    def validate_author_params_key(self,params):
        missing_key = []
        key = 'author_id'
        if not key in params.keys():
            missing_key.append(key)
        return missing_key
                
    def get(self,request):
        params = request.GET.dict()
        try:
            missing_key =self.validate_author_params_key(params)
            if missing_key:
                raise AuthorException(MISSING_KEYS)
            missing_key_value = self.validate_author_params_value(params)
            if missing_key_value:
                raise AuthorException(MISSING_KEY_VALUE)
            author_ids = params.get('author_id').strip().split(',')
            self.validate_author_ids(author_ids)
            author_detail = Author.objects.get_author_details(author_ids)
            self.response['res_data'] = author_detail
            self.response['res_str'] = AUTHOR_SUCCESSFULLY_FOUND
            return send_200(self.response)
        except AuthorException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

    def validate_author_params(self,params):
        missing_key = []
        for key in ['author_id','email_id','name']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key        
                 
  
    def put(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_author_params(params)
            if missing_key:
                raise AuthorException(MISSING_KEYS)
            missing_key_value = self.validate_author_params_value(params)
            if missing_key_value:
                raise AuthorException(MISSING_KEY_VALUE)
            author_id = params.get('author_id').strip().split(',')
            self.validate_author_ids(author_id)
            author_detail = Author.objects.update_author_details(params)
            self.response['res_data'] = author_detail
            self.response['res_str'] = AUTHOR_DETAILS_UPDATED
            return send_200(self.response)
        except  AuthorException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] =traceback.format_exc()
            return send_400(self.response)          
  
    def delete(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_author_params_key(params)
            if missing_key:
                raise AuthorException(MISSING_KEYS)
            missing_key_value = self.validate_author_params_value(params)
            if missing_key_value:
                raise AuthorException(MISSING_KEY_VALUE)
            author_ids = params.get('author_id').strip().split(',')
            self.validate_author_ids(author_ids)
            Author.objects.filter(author_id__in=author_ids).delete()
            self.response['res_str'] = AUTHOR_DETAILS_DELETED   
            return send_200(self.response)
        except  AuthorException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key
            self.response['res_str'] = str(ex)
            return send_400(self.response)             
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)  

class BookView(View):
    def __init__(self):
        self.response = init_response()

    def validate_book_ids(self,book_id):
        book_objs = Book.objects.filter(book_id__in=book_id)
        if not book_objs:
            raise BookException("Invalid Book id") 

    def validate_language_id_author_id_publisher_id(self,language_id,publisher_id,author_id):
        language_obj = Language.objects.get(language_id = language_id)
        publisher_obj = Publisher.objects.get(publisher_id = publisher_id)
        author_obj = Author.objects.get(author_id=author_id)
        if not (language_obj and publisher_obj and author_obj):
            raise BookException(INVALID_IDS)
        return publisher_obj,language_obj,author_obj


    def validate_book_param(self,params):
        missing_key =[]
        for key in ['name','language_id','publisher_id','author_id','book_type','category','extra_det']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key         
                

    def validate_book_params_value(self,params):
        keys=[]
        for key, value in params.items():
            if not value:
                keys.append(key)              
        return keys                                   

    def post(self,request,*args, **kwargs):

        def __init__(self):
            self.response = init_response()

        params = request.POST.dict()   
        try:   
            missing_key = self.validate_book_param(params)
            if missing_key:
                raise BookException(MISSING_KEYS) 
            missing_key_value = self.validate_book_params_value(params)
            if not len(missing_key_value)==0:
                raise BookException(MISSING_KEY_VALUE)                
            language_id = params.get('language_id')
            publisher_id = params.get('publisher_id')
            author_id = params.get('author_id')
            publisher_obj,language_obj,author_obj = self.validate_language_id_author_id_publisher_id(language_id,publisher_id,author_id)
            Book.objects.add_book_details(params,publisher_obj,language_obj,author_obj)
            self.response['res_str'] = BOOK_SUCCESSFULLY_ADDED
            return send_201(self.response)
        except BookException as ex:
            if len(missing_key)==0:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key   
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response) 

    def validate_book_params(self,params):
        missing_key = []
        for key in ['book_id','per_page','page']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key             
   
 

    def get(self, request):
        params=request.GET.dict()
        try:
            missing_key = self.validate_book_params(params)
            if missing_key:
                raise BookException(MISSING_KEYS)
            missing_key_value = self.validate_book_params_value(params)
            if not len(missing_key_value)==0:
                raise BookException(MISSING_KEY_VALUE) 
            per_page= params.get('per_page')
            book_ids = params.get('book_id').strip().split(',')
            self.validate_book_ids(book_ids)
            book = Book.objects.get_book_details(book_ids)
            paginator = Paginator(book,per_page)
            page_number = request.GET.get('page')
            page_obj = paginator.page(page_number)
            book_data = page_obj.object_list
            self.response['res_data'] = book_data
            self.response['res_str'] = BOOK_DETAILS_FOUND
            return send_200(self.response)
        except BookException as ex:
            if len(missing_key)==0:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key    
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

    def validate_book_params_key(self,params):
        missing_key =[]
        key = 'book_id'
        if not key in params.keys():
            missing_key.append(key)
        return missing_key             
   
    def delete(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_book_params_key(params)
            if missing_key:
                raise BookException(MISSING_KEYS)
            missing_key_value = self.validate_book_params_value(params)
            if not len(missing_key_value)==0:
                raise BookException(MISSING_KEY_VALUE)         
            book_id = params.get('book_id').strip().split(',')
            self.validate_book_ids(book_id)
            Book.objects.filter(book_id__in=book_id).delete()
            self.response['res_str'] = BOOK_DELETED 
            return send_200(self.response)       
        except BookException as ex:
            if len(missing_key)==0:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key
            self.response['res_str'] = str(ex)
            return send_400(self.response)  
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

class UserView(View):
    def __init__(self):
        self.response = init_response()


    def validate_user_ids(self,user_id):
        user_objs = self.filter(user_id__in = user_id)
        if not user_objs:
            raise UserException(INVALID_USER_IDS)

    def validate_existing_user(self,aadhar_id):
        user_obj = self.filter(aadhar_id=aadhar_id)
        if user_obj:
            raise UserException(USER_EXIST_ERR) 
            
    def validate_user_param(self,params):
        missing_key = []
        for key in ['first_name', 'last_name', 'mobile_no', 'email_id', 'aadhar_id', 'role']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key    
                

    def validate_user_params_value(self,params):
        keys=[]
        for key, value in params.items():
            if not value:
                keys.append(key)
        return keys        
       
    def post(self, request):
        params = request.POST.dict()
        try:
            missing_key = self.validate_user_param(params)
            if missing_key:
                raise UserException(MISSING_KEYS)
            missing_key_value = self.validate_user_params_value(params)
            if missing_key_value:
                raise UserException(MISSING_KEY_VALUE)
            aadhar_id = params.get("aadhar_id")
            self.validate_existing_user(aadhar_id)
            User.objects.add_user(params)
            self.response['res_str'] = USER_ADDED
            return send_201(self.response)
        except UserException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key    
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)  


    def validate_user_params_key(self,params):
        missing_key = []
        key = 'user_id'
        if not key in params.keys():
            missing_key.append(key)
        return missing_key              

    def get(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_user_params_key(params)
            if missing_key:
                raise UserException(MISSING_KEYS)
            missing_key_value = self.validate_user_params_value(params)
            if missing_key_value:
                raise UserException(MISSING_KEY_VALUE)
            user_ids = params.get('user_id').strip().split(',')
            self.validate_user_ids(user_ids)
            user = User.objects.get_user_details(user_ids)
            self.response['res_data'] = user
            self.response['res_str'] = USER_DETAILS_FOUND
            return send_200(self.response)
        except UserException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)    
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)   

    def validate_user_params(self,params):
        missing_key = []
        for key in ['user_id','mobile_no', 'email_id', 'role']:
            if not key in params.keys():
                missing_key.append(key)   
        return missing_key                   

    def put(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_user_params(params)
            if missing_key:
                raise UserException(MISSING_KEYS)
            missing_key_value = self.validate_user_params_value(params)
            if missing_key_value:
                raise UserException(MISSING_KEY_VALUE)
            user_id = params.get('user_id')
            self.validate_user_ids(user_id)
            user =  User.objects.update_user_details(params)
            self.response['res_str'] = USER_DETAILS_UPDATED
            self.response['res_data'] = user
            return send_200(self.response)
        except UserException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response) 
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)       

    def delete(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_user_params_key(params)
            if missing_key:
                raise UserException(MISSING_KEYS)
            missing_key_value  = self.validate_user_params_value(params)
            if missing_key_value:
                raise UserException(MISSING_KEY_VALUE)
            user_id = params.get('user_id').strip().split(',')
            self.validate_user_ids(user_id)
            User.objects.filter(user_id__in=user_id).delete()
            self.response['res_str'] = USER_DELETED
            return send_200(self.response)
        except UserException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)     
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)       
   
class PublisherView(View):
    def __init__(self):
        self.response = init_response()

    def validate_publisher_ids(self,publisher_ids):
        publisher_objs = Publisher.objects.filter(publisher_id__in = publisher_ids)
        if not publisher_objs:
            raise PublisherException(PUBLISHER_NOT_EXIST) 

    def validate_publisher_params(self,params):
        missing_key = []
        for key in ['name', 'contact_details']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key         

    def validate_publisher_params_value(self,params):
        keys=[]
        for key, value in params.items():
            if not value:
                keys.append(key)
        return keys 
         

    def post(self, request):
        params = request.POST.dict()
        try:
            missing_key = self.validate_publisher_params(params)
            if missing_key:
                raise PublisherException(MISSING_KEYS)
            missing_key_value = self.validate_publisher_params_value(params)
            if missing_key_value:
                raise PublisherException(MISSING_KEY_VALUE)
            Publisher.objects.add_publisher_details(params)
            self.response['res_str'] = PUBLISHER_ADDED
            return send_201(self.response)
        except PublisherException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex: 
            self.response['res_str'] = traceback.format_exc() 
            return send_400(self.response)            

    def validate_publisher_params_key(self,params):
        missing_key=[]
        key ='publisher_id'
        if not key in params.keys():
            missing_key.append(key)
        return missing_key 

    def get(self, request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_publisher_params_key(params)
            if missing_key:
                raise PublisherException(MISSING_KEYS)
            missing_key_value = self.validate_publisher_params_value(params)
            if missing_key_value:
                raise PublisherException(MISSING_KEY_VALUE)
            publisher_ids = params.get('publisher_id').strip().split(',')
            self.validate_publisher_ids(publisher_ids)
            publisher_det = Publisher.objects.get_publisher_details(publisher_ids)
            self.response['res_data'] = publisher_det
            self.response['res_str'] = PUBLISHER_DETAILS_FOUND
            return send_200(self.response)
        except PublisherException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)          

    def validate_publisher_param(self,params):
        missing_key =[]
        for key in ['publisher_id','name','contact_details']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key      

    def put(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_publisher_param(params)
            if missing_key:
                raise PublisherException(MISSING_KEYS)
            missing_key_value = self.validate_publisher_params_value(params)
            if missing_key_value:
                raise PublisherException(MISSING_KEY_VALUE)
            publisher_id = params.get('publisher_id').strip().split(',')
            self.validate_publisher_ids(publisher_id)
            publisher_details = Publisher.objects.update_publisher_details(params)
            self.response['res_data'] = publisher_details
            self.response['res_str'] = PUBLISHER_DETAILS_UPDATED
            return send_200(self.response)
        except PublisherException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response) 
    
    def delete(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_publisher_params_key(params)
            if missing_key:
                raise PublisherException(MISSING_KEYS) 
            missing_key_value = self.validate_publisher_params_value(params)
            if missing_key_value:
                raise PublisherException(MISSING_KEY_VALUE)
            publisher_id = params.get('publisher_id').strip().split(',')
            self.validate_publisher_ids(publisher_id)
            Publisher.objects.filter(publisher_id__in=publisher_id).delete()
            self.response['res_str'] = PUBLISHER_DELETED
            return send_200(self.response)
        except PublisherException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

class EbookView(View):

    def __init__(self):
        self.response = init_response()

    def validate_ebook_ids(self,book_id):
        ebook_objs = self.filter(book_id__in = book_id)
        if not ebook_objs:
            raise EbookException(EBOOK_ID_ERR)        
    def check_ebook_existing(self,book_id):
        ebook_obj = self.select_related("ebook").all().values_list("ebook", flat=True)[::1]
        if int(book_id) in ebook_obj:
            raise EbookException("Ebook already exist")
    def validate_book_id_user_id(self,book_id):
        book_obj = Book.objects.filter(book_id=book_id)
        user_obj = Book.objects.filter(book_id=book_id)
        if not (user_obj and book_obj):
            raise EbookException(INVALID_ID)

    def validate_book_type(self,book_id):
        book_obj = Book.objects.get(book_id=book_id)
        book_type = book_obj.book_type
        if not (book_type=="ebook"):
            raise EbookException(EBOOK_ID_ERR)


    def validate_ebook_params(self,params):
        missing_key=[]
        for key in ['book_id','user_id','location']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key
               

    def validate_ebook_params_value(self,params):
        keys=[]
        for key, value in params.items():
            if not value:
                keys.append(key)
        return keys 
        
    def post(self,request):
        params = request.POST.dict()
        try:
            missing_key = self.validate_ebook_params(params)
            if missing_key:
                raise EbookException(MISSING_KEYS)
            missing_key_value = self.validate_ebook_params_value(params)
            if missing_key_value:
                raise EbookException(MISSING_KEY_VALUE)
            book_id = params.get('book_id')
            user_id = params.get('user_id')
            location = params.get('location')
            self.validate_book_id_user_id(book_id)
            self.check_ebook_existing(book_id)
            self.validate_book_type(book_id)
            book_obj = Book.objects.get(book_id = book_id)
            user_obj = User.objects.get(user_id=user_id)
            location = params.get("location")
            Ebook.objects.add_ebook(book_obj, location, user_obj)
            self.response['res_str'] = EBOOK_ADDED
            return send_201(self.response)
        except EbookException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)   
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response) 

    def validate_ebook_params_key(self,params):
        missing_key = []
        key ='ebook_id'
        if not key in params.keys():
            missing_key.append(key)
        return missing_key              

    def get(self,request):
        params =  request.GET.dict()
        try:
            missing_key = self.validate_ebook_params_key(params)
            if missing_key:
                 raise EbookException(MISSING_KEYS)
            missing_key_value = self.validate_ebook_params_value(params)
            if missing_key_value:
                raise EbookException(MISSING_KEY_VALUE)
            book_id = params.get('ebook_id').strip().split(',')
            self.validate_ebook_ids(book_id)
            ebook = Ebook.objects.get_ebook_info(book_id)
            self.response['res_data'] = ebook
            self.response['res_str'] = EBOOK_DETAILS_FOUND
            return send_200(self.response)
        except EbookException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

    def validate_ebook_param(self,params):
        missing_key=[]
        for key in ['ebook_id','location']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key           

    def put(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_ebook_param(params)
            if missing_key:
                 raise EbookException(MISSING_KEYS)
            missing_key_value = self.validate_ebook_params_value(params)
            if missing_key_value:
                raise EbookException(MISSING_KEY_VALUE)
            ebook_id = params.get("ebook_id").strip().split(',')
            location = params.get('location')
            self.validate_ebook_ids(ebook_id)
            book_obj = Ebook.objects.get(book_id__in=ebook_id)
            book_obj.book_location = location   
            book_obj.save(update_fields=['book_location'])  
            self.response['res_str'] = BOOK_LOCATION_UPDATED
            return send_200(self.response)
        except EbookException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

    def delete(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_ebook_params_key(params)
            if missing_key:
                 raise EbookException(MISSING_KEYS)
            missing_key_value = self.validate_ebook_params_value(params)
            if missing_key_value:
                raise EbookException(MISSING_KEY_VALUE)
            book_id = params.get("ebook_id").strip().split(',')
            self.validate_ebook_ids(book_id)
            Ebook.objects.filter(book_id__in=book_id).delete()
            self.response['res_str'] = EBOOK_DELETED
            return send_200(self.response)
        except EbookException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

class HardBookInfoView(View):
    def __init__(self):
        self.response = init_response()

    def validate_hardcopy_ids(self,hardCopy_id):
        bookinfo_objs = HardBookInfo.objects.filter(hardCopy_id__in = hardCopy_id)
        if not bookinfo_objs:
            raise HardBookInfoException(HARD_COPY_ID_ERR) 

    def valiate_book_count(self,user_id):
        hardcopybook_list = list(HardBookInfo.objects.select_related("lentTo").all().values_list("lentTo", flat=True))
        book_count = hardcopybook_list.count(int(user_id))
        if book_count >5:
            raise HardBookInfoException(BOOK_LIMIT_EXCEED)


    def check_nbook_existing(self,user_id,book_id):
        user_list = list(HardBookInfo.objects.select_related("lentTo").all().values_list("lentTo", flat=True))
        book_lis = list(HardBookInfo.objects.select_related("book_name").all().values_list("book_name", flat=True))
        if ((int(user_id) in user_list) and (int(book_id) in book_lis)):
            raise HardBookInfoException(BOOK_ISSUE_ERR)            

    def validate_book_id(self,book_id):
        book_obj = Book.objects.filter(book_id=book_id)
        if not book_obj:
            raise HardBookInfoException(HARD_COPY_ID_ERR)

    def validate_book_type(self,book_id):
        book_obj = Book.objects.get(book_id=book_id)
        book_type = book_obj.book_type
        if not (book_type=="nbook" and book_obj):
            raise HardBookInfoException(HARD_COPY_ID_ERR)

    def validate_hardbook_params(self,params):
        missing_key=[]
        for key in ['book_id', 'user_id','isLent']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key 

    def validate_hardcopy_book_params_value(self,params):
        keys=[]
        for key, value in params.items():
            if not value:
                keys.append(key)
        return keys  
       

    def post(self,request):
        params = request.POST.dict()
        try:
            missing_key = self.validate_hardbook_params(params)
            if missing_key:
                raise HardBookInfoException(MISSING_KEYS)
            missing_key_value = self.validate_hardcopy_book_params_value(params)
            if missing_key_value:
                raise HardBookInfoException(MISSING_KEY_VALUE)
            user_id = params.get('user_id')
            book_id = params.get('book_id')
            self.validate_book_id(book_id)
            self.validate_book_type(book_id)
            self.check_nbook_existing(user_id,book_id)
            book_obj = Book.objects.get(book_id=book_id)
            isLent = params.get('isLent')
            self.valiate_book_count(user_id)
            user_obj = User.objects.get(user_id=user_id)
            if user_obj.subscription == True:
                HardBookInfo.objects.issue_book(book_obj,isLent,user_obj)
                self.response['res_str'] = BOOK_ISSUED
            else:
                self.response['res_str'] = USER_SUBSCRIPTION_ERR   
            return send_201(self.response)
        except HardBookInfoException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)   
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response) 


    def validate_hardbook_params_key(self,params):
        missing_key=[]
        key = 'hardCopy_id'
        if not key in params.keys():
            missing_key.append(key)
        return missing_key                

    def get(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_hardbook_params_key(params)
            if missing_key:
                raise HardBookInfoException(MISSING_KEYS)
            missing_key_value = self.validate_hardcopy_book_params_value(params)
            if missing_key_value:
                raise HardBookInfoException(MISSING_KEY_VALUE)            
            hardCopy_id = params.get('hardCopy_id').strip().split(',')
            self.validate_hardcopy_ids(hardCopy_id)
            book_info =  HardBookInfo.objects.get_issue_book_info(hardCopy_id)
            self.response['res_data'] = book_info
            self.response['res_str'] = BOOK_INFO_FOUND
            return send_200(self.response)
        except HardBookInfoException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)
        

    def delete(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_hardbook_params_key(params)
            if missing_key:
                raise HardBookInfoException(MISSING_KEYS)
            missing_key_value = self.validate_hardcopy_book_params_value(params)
            if missing_key_value:
                raise HardBookInfoException(MISSING_KEY_VALUE)            
            hardCopy_id = params.get('hardCopy_id').strip().split(',')
            self.validate_hardcopy_ids(hardCopy_id)
            HardBookInfo.objects.filter(hardCopy_id__in=hardCopy_id).delete()
            self.response['res_str'] = BOOK_DELETED
            return send_200(self.response)
        except HardBookInfoException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)    

class BookApproval(View):
    def __init__(self):
        self.response = init_response()

    def validate_user_role(self,user_id):
        user_obj = User.objects.get(user_id=user_id)
        user_role = user_obj.role
        if not (user_role=="moderator"):
            raise BookApprovalException(USER_PERMISSION_DENIED)
    def validate_book_id(self,book_id):
        book_objs = Ebook.objects.filter(book_id=book_id)
        if not book_objs:
            raise BookApprovalException(EBOOK_ID_ERR)

    def validate_book_approval_params(self,params):
        missing_key=[]
        for key in ['book_id', 'user_id','approval_status']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key 

    def validate_book_approval_params_value(self,params):
        keys=[]
        for key, value in params.items():
            if not value:
                keys.append(key)
        return keys 
       
    def post(self,request):
        params = request.POST.dict()
        try:
            missing_key = self.validate_book_approval_params(params)
            if missing_key:
                raise BookApprovalException(MISSING_KEYS)
            missing_key_value = self.validate_book_approval_params_value(params)
            if missing_key_value:
                raise BookApprovalException(MISSING_KEY_VALUE)
            book_id = params.get('book_id')
            user_id = params.get('user_id')
            approval_status = params.get('approval_status')
            self.validate_user_role(user_id)
            self.validate_book_id(book_id)
            book_obj = Ebook.objects.get(book_id=book_id)
            book_obj.approval_status =  approval_status 
            book_obj.save(update_fields = ['approval_status'])
            self.response['res_str'] = BOOK_STATUS_CHANGE
            return send_201(self.response)    
        except BookApprovalException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)            
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

class SearchView(View):

    def __init__(self):
        self.response = init_response()

    def validate_search_params_value(self,params):
        keys = []
        for key , value in params.items():
            if not value:
                keys.append(key)
        return keys        
   

    def validate_search_params(self,params):
        if len(params)==0:
            raise BookApprovalException("'book_name' or 'author_name' or 'publisher_name' or 'category' keys is required")

    def get(self, request):
        params = request.GET.dict()
        try:
            self.validate_search_params(params)
            missing_key_value = self.validate_search_params_value(params)
            if missing_key_value:
                raise BookApprovalException(MISSING_KEY_VALUE)
            book_list = Book.objects.search_book(params)
            if not len(book_list)==0:
                self.response['res_data'] = book_list
                self.response['res_str'] = BOOK_DETAILS_FOUND     
            else:
                self.response['res_str'] = BOOK_DETAILS_NOT_FOUND 
            return send_200(self.response)  
        except BookApprovalException as ex:
            if missing_key_value:
                self.response['res_data'] = missing_key_value
            self.response['res_str'] = str(ex)
            return send_400(self.response)            
        except Exception as ex:
            self.response['res_data'] = traceback.format_exc()
            self.response['res_str'] = str(ex)
            return send_400(self.response)     

class FavouriteBookView(View):
    
    def __init__(self):
        self.response = init_response()

    def validate_user_book_ids(self,book_id, user_id):
        user_obj = User.objects.filter(user_id=user_id)
        book_objs = Book.objects.filter(book_id__in=book_id)
        if not (book_objs and user_obj):
            raise FavouriteException(INVALID_ID) 

    def validate_favourite_params(self,params):
        missing_key = []
        for key in ['user_id', 'book_id']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key  
    def validate_fav_key_params(self,params):
        keys=[]
        for key, value in params.items():
            if not value:
                keys.append(key)
        return keys 
        

    def post(self,request):
        params = request.POST.dict()
        try:
            missing_key = self.validate_favourite_params(params)
            if missing_key:
                 raise FavouriteException(MISSING_KEYS)
            missing_key_value = self.validate_fav_key_params(params)
            if missing_key_value:
                raise FavouriteException(MISSING_KEY_VALUE)
            book_id = params.get('book_id').strip().split(',')
            user_id = params.get('user_id')
            self.validate_user_book_ids(book_id,user_id)
            User.objects.add_favourite_book(book_id,user_id)
            self.response['res_str'] = FAVOURITE_BOOK_ADDED
            return send_201(self.response)
        except FavouriteException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)
                   

class Subscription(View):

    def __init__(self):
        self.response = init_response()

    def validate_user(self,user_id):
        user_obj = User.objects.filter(user_id=user_id)
        if not user_obj:
            raise SubscriptionException(USER_NOT_EXIST)

    def validate_subscription_choice(self,choice):
        if not (int(choice)==1 or int(choice)==0):
            raise SubscriptionException(INVALID_CHOICES)

    def validate_subscription_params(self,params):
        missing_key =[]
        for key in ['user_id', 'choice']:
            if not key in params.keys():
                missing_key.append(key)
        return missing_key  

    def validate_subscription_key_params_value(self,params):
        keys=[]
        for key, value in params.items():
            if not value:
                keys.append(key)
        return keys 
   
    def put(self,request):
        params = request.GET.dict()
        try:
            missing_key = self.validate_subscription_params(params)
            if missing_key:
                 raise SubscriptionException(MISSING_KEYS)
            missing_key_value = self.validate_subscription_key_params_value(params)
            if missing_key_value:
                raise SubscriptionException(MISSING_KEY_VALUE)
            user_id= params.get('user_id')
            choice = params.get('choice')
            self.validate_user(user_id)
            self.validate_subscription_choice(choice)
            user_det = User.objects.update_subscription(user_id, choice)
            if int(choice)==1:
                self.response['res_str'] = SUBSCRIPTION_ACTIVATED
            else:
                self.response['res_str'] = SUBSCRIPTION_DEACTIVATED  
            self.response['res_data'] = user_det
            return send_200(self.response)
        except SubscriptionException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response) 


class UpdateAuthorImg(View):
    
    def __init__(self):
        self.response = init_response()

    def validate_author_id_key(self,params):
        missing_key =[]
        key = 'author_id'
        if not key in params.keys():
            missing_key.append(key)
        return missing_key  

    def validate_author_key_params(self,params):
        keys=[]
        for key, value in params.items():
            if not value:
                keys.append(key)
        return keys 
              
                
    def validate_author_id(self,author_id):
        author_objs = Author.objects.filter(author_id=author_id)
        if not author_objs:
            raise AuthorException(AUTHOR_NOT_EXIST)


    def post(self,request):
        params = request.POST.dict()
        try:
            missing_key = self.validate_author_id_key(params)
            if missing_key:
                raise AuthorException(MISSING_KEYS)
            missing_key_value = self.validate_author_key_params(params)
            if missing_key_value:
                raise AuthorException(MISSING_KEY_VALUE)
            picture = request.FILES['picture']
            author_id = params.get('author_id')
            self.validate_author_id(author_id)
            author_obj = Author.objects.get(author_id=author_id)
            author_obj.picture = picture
            author_obj.save(update_fields=['picture'])
            self.response['res_str'] = AUTHOR_IMG_UPDATED
            return send_201(self.response)
        except AuthorException as ex:
            if not missing_key:
                self.response['res_data'] = missing_key_value
            else:
                self.response['res_data'] = missing_key 
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response) 

        
