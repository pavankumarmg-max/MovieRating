from posixpath import basename
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from watchlist_app.api import views
from watchlist_app import models
# print('appurls IN')

router = DefaultRouter()
router.register('stream',views.StreamPlatformViewSet,basename='streamplatform'),


urlpatterns = [
    # path('list/',views.movie_list,name='movie_list'),
    # path('detail/<int:pk>',views.movie_details, name='movie_details'),
    # path('list/',views.MovieListAPIView.as_view(), name='movie_list'),
    # path('detail/<int:pk>',views.MovieDetailAPIView.as_view(), name='movie_detail'),
    ## path('stream/',views.StreamPlatformAPIView.as_view(), name='stream'),
    # #path('stream/detail/<int:pk>',views.StreamPlatformDetailedAPIView.as_view(), name='stream_detail'),
    path('',include(router.urls)),

    path('list/',views.WatchListAPIView.as_view(), name='movie_list'),
    path('lists/',views.WatchList.as_view(), name='movie_list'),

    path('detail/<int:pk>',views.WatchDetailAPIView.as_view(), name='movie_details'),
    # path('review/',views.ReviewList.as_view(), name='review'),
    # path('review/<int:pk>',views.ReviewDetails.as_view(), name='review_detail'),
    path('<int:pk>/reviewcreate', views.ReviewCreate.as_view(),name='review_create'),

    path('<int:pk>/reviews/', views.ReviewList.as_view(),name='review_list'),
    path('stream/review/<int:pk>', views.ReviewDetails.as_view(), name='review_details'),
    # path('reviews/<str:username>/',views.UserReviwefilter.as_view(),name ='user-review-details'),
    path('reviews/',views.UserReviwefilter.as_view(),name ='user-review-details'),
    

]
# print('appurls OUT')