# from django.shortcuts import render
# from django.http import JsonResponse
# from watchlist_app.models import Movie


# # Create your views here.
# # Movie model
# def movielist(request):
#     movies=Movie.objects.all()
#     data = {
#         'movies':list(movies.values())
#     }
        
#     return JsonResponse(data)

# #detailed 
# def movie_details(request,pk):
#     movie =Movie.objects.get(pk=pk)
#     data ={
#         'name': movie.name,
#         'description': movie.description,
#         'active': movie.active
#     }
    
#     return JsonResponse(data)

