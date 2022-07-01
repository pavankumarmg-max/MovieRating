from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from watchlist_app.models import Review, WatchList,StreamPlatform

# Register your models here.
@admin.register(WatchList)
class WatchListAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=['id','title']
@admin.register(StreamPlatform)
class StreamPlatformAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=['id','name']

@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=['id','user_review']
# admin.site.register(WatchListAdmin,WatchList)
# admin.site.register(StreamPlatform)
# admin.site.register(Review)
# print('admin panel 8')