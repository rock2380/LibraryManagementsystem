from django.conf.urls import url
from .views import (AuthorView, LanguageView, UserView, BookView, PublisherView, EbookView,
                    HardBookInfoView, SearchView , BookApproval, FavouriteBookView, Subscription, UpdateAuthorImg)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url('language_details',csrf_exempt(LanguageView.as_view())),
    url('author_details',csrf_exempt(AuthorView.as_view())),
    url('user_details',csrf_exempt(UserView.as_view())),
    url('book_details',csrf_exempt(BookView.as_view())),
    url('publisher_details',csrf_exempt(PublisherView.as_view())),
    url('favourite',csrf_exempt(FavouriteBookView.as_view())),
    url('ebook',csrf_exempt(EbookView.as_view())),
    url('book_info',csrf_exempt(HardBookInfoView.as_view())),
    url('search_book',csrf_exempt(SearchView.as_view())),
    url('subscription',csrf_exempt(Subscription.as_view())),
    url('approval',csrf_exempt(BookApproval.as_view())),
    url('updateauthorimg',csrf_exempt(UpdateAuthorImg.as_view())),
]