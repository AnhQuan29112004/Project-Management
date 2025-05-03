from rest_framework.filters import BaseFilterBackend

class CustomSearchFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        
        for key,value in request.query_params.items():
            if key and key not in ["page","pageSize"] and value:
                if key == "keySearch":
                    queryset = queryset.filter(name__icontains =value)
                else:
                    queryset = queryset.filter(researchField__name__icontains =value)
        
        return queryset