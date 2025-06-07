from django.urls import path
from .views import HomePageView, cottage_detail, review_edit, review_delete

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('<slug:slug>/', cottage_detail, name='cottage_detail'),
    path('<slug:slug>/edit_review/<int:review_id>/',
         review_edit, name='review_edit'),
    path('<slug:slug>/delete_review/<int:review_id>/',
         review_delete, name='review_delete'),
]
