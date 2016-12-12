from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination

class SquadsterPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        if len(data) == 0:
            return Response({
                'next': None,
                'previous': None,
                'count': 0,
                'data': []
            })

        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })
