from rest_framework.filters import BaseFilterBackend

class CustomSearchFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search = request.query_params.get('keySearch', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset