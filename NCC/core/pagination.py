from rest_framework import pagination
from rest_framework.response import Response

class SubmissionPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'
class LeaderboardPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'
    def get_paginated_response(self, data):
        response = Response(data)
        response['count'] = self.page.paginator.count
        response['next'] = self.get_next_link()
        response['previous'] = self.get_previous_link()
        return response