class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Chỉ truy cập content sau khi render
        if hasattr(response, 'render') and callable(response.render):
            response.render()
        # Bây giờ có thể truy cập response.content an toàn
        return response