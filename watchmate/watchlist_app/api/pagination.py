from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

class WatchListoffPagination(LimitOffsetPagination):
    # page_size = 10
    # page_size_query_param = 'page_size'
    # max_page_size = 10
    default_limit=10
    max_limit =10
    limit_query_param='limit'
    offset_query_param = 'start'

class WatchListCursorPagination(CursorPagination):
    page_size=10
