from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend


from watchlist_app import models
from watchlist_app.api import permissions
from.import serializers

class UserReviwefilter(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return models.Review.objects.filter(user_review__username=username)




#---PART -4-----------
class ReviewCreate(generics.CreateAPIView):
    serializer_class=serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Review.objects.all()

    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
        
        watchlist = models.WatchList.objects.get(pk=pk)
        serializer.save(watchlist=watchlist)
        user_review= self.request.user
        review_queryset=models.Review.objects.filter(watchlist=watchlist,user_review=user_review)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this watch!")
        if watchlist.number_rating ==0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.average_rating+serializer.validated_data['rating'])/2
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        serializer.save(watchlist=watchlist,user_review=user_review)


class ReviewList(generics.ListAPIView):
    # queryset= models.Review.objects.all()
    # permission_classes =[IsAuthenticated]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    filter_backends=[DjangoFilterBackend]
    filterset_fields = ['user_review__username', 'active']


    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Review.objects.filter(watchlist=pk)

class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset= models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes =[permissions.ReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]

class WatchList(generics.ListAPIView):
    queryset= models.WatchList.objects.all()
    serializer_class=serializers.WatchListSerializer
    # permission_classes =[IsAuthenticated]
    # throttle_classes = [UserRateThrottle,AnonRateThrottle]
    filter_backends=[DjangoFilterBackend]
    filterset_fields = ['title', 'platform__name']



#---PART -3-----------
##Adding more models




# class ReviewDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = models.Review.objects.all()
#     serializer_class = serializers.ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)



# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = models.Review.objects.all()
#     serializer_class = serializers.ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
###-----------Model viewsets---
class StreamPlatformViewSet(viewsets.ModelViewSet):
    queryset = models.StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer


#----viewsets----
# class StreamPlatformViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     def list(self, request):
#         queryset = models.StreamPlatform.objects.all()
#         serializer = serializers.StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = models.StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = serializers.StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
#     def create(self, request):
#         serializer = serializers.StreamPlatformSerializer(data =request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#     def update(self, request, pk=None):
#         queryset = models.StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = serializers.StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)


#     def destroy(self, request, pk=None):
#         queryset = models.StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = serializers.StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)


class StreamPlatformAPIView(APIView):
    

    def get(self, request):
        platform= models.StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformSerializer(platform, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.StreamPlatformSerializer(data =request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailedAPIView(APIView):
    permissions=[permissions.IsAdminOrReadOnly]


    def get(self, request,pk):
        try:
            movie = models.StreamPlatform.objects.get(pk=pk)
        except models.StreamPlatform.DoesNotExist:
            return Response({'error': 'Movie not found'},status=status.NOT_FOUND)

        serializer = serializers.StreamPlatformSerializer(movie)
        return Response(serializer.data)


    def put(self, requset,pk):
        movie = models.StreamPlatform.objects.get(pk=pk)
        serializer = serializers.StreamPlatformSerializer(movie,data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    def delete(self, requset,pk):
        movie= models.StreamPlatform.objects.get(pk=pk)
        movie.delete()








class WatchListAPIView(APIView):
    permissions=[permissions.IsAdminOrReadOnly]


    def get(self, request):
        movie = models.WatchList.objects.all()
        serializer = serializers.WatchListSerializer(movie,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.WatchListSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAPIView(APIView):
    permissions=[permissions.IsAdminOrReadOnly]
    def get(self, request,pk):
        try:
            movie = models.WatchList.objects.get(pk=pk)
        except models.WatchList.DoesNotExist:
            return Response({'error': 'Movie not found'},status=status.NOT_FOUND)

        serializer = serializers.WatchListSerializer(movie)
        return Response(serializer.data)


    def put(self, requset,pk):
        movie = models.WatchList.objects.get(pk=pk)
        serializer = serializers.WatchListSerializer(movie,data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    def delete(self, requset,pk):
        movie= models.Movie.objects.get(pk=pk)
        movie.delete()













#----PART-2--###
## Class Based View----------------------------------------------------------------

# class MovieListAPIView(APIView):

#     def get(self, request):
#         movie = models.Movie.objects.all()
#         serializer = serializers.MovieSerializer(movie,many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = serializers.MovieSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# class MovieDetailAPIView(APIView):
    
#     def get(self, request,pk):
#         try:
#             movie = models.Movie.objects.get(pk=pk)
#         except models.Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'},status=status.NOT_FOUND)

#         serializer = serializers.MovieSerializer(movie)
#         return Response(serializer.data)


#     def put(self, requset,pk):
#         movie = models.Movie.objects.get(pk=pk)
#         serializer = serializers.MovieSerializer(movie,data=requset.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         else:
#             return Response(serializer.errors)

#     def delete(self, requset,pk):
#         movie= models.Movie.objects.get(pk=pk)
#         movie.delete()


##----PART-1---###

# #------function based view----------------------------------------------------------------

# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method=='GET':
#         movies = models.Movie.objects.all()
#         serializer = serializers.MovieSerializer(movies,many = True)#many = True used to access all movies

#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer=serializers.MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status= status.HTTP_201_CREATED)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,pk):
#     #for reading GET request
#     if request.method == 'GET':

#         try:
#             movie = models.Movie.objects.get(pk=pk)
#         except models.Movie.DoesNotExist:
#             return Response({'Error': 'Movie not found'},status=status.HTTP_404_NOT_FOUND)
#         movie = models.Movie.objects.get(pk=pk)
#         serializer =serializers.MovieSerializer(movie)

#         return Response(serializer.data)
    
#     #updating PUT request
#     if request.method == 'PUT':
#         movie= models.Movie.objects.get(pk=pk)
#         serializer = serializers.MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         else:
#             return Response(serializer.errors)

#     #DELETE REQUEST
#     if request.method == 'DELETE':
#         movie= models.Movie.objects.get(pk=pk)
#         movie.delete()

#         #return is used to desplay what had happened.
#         return Response(status=status.HTTP_204_NO_CONTENT)


