from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
class VendorProductResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class CustomerProductResultsSetPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_page_number(self, request, paginator):
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number == '0':
            # Mark that a special response should be returned
            self.custom_zero_page_requested = True
            # Return a valid page number so pagination doesn't break internally
            return 1 
        self.custom_zero_page_requested = False
        return super().get_page_number(request, paginator)

    def get_paginated_response(self, data):
        # Check if special response is requested
        if self.custom_zero_page_requested:
            # return Response({"1": 1})
            return Response(data)
        return super().get_paginated_response(data)
        