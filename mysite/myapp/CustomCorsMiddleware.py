class CustomCorsMiddleware:
    def __init__(self, get_response):
        print('lo tio')
        self.get_response = get_response

    def __call__(self, request):
        # preflight OPTIONS handling
        print('hola')
        if request.method == 'OPTIONS':
            response = HttpResponse(status=200)
            # Allow the origin in the request
            response["Access-Control-Allow-Origin"] = request.META.get('HTTP_ORIGIN', '*')
            # Allow the request method in the preflight request
            response["Access-Control-Allow-Methods"] = request.META.get('HTTP_ACCESS_CONTROL_REQUEST_METHOD', 'POST, OPTIONS')
            # Allow the headers in the preflight request
            response["Access-Control-Allow-Headers"] = request.META.get('HTTP_ACCESS_CONTROL_REQUEST_HEADERS', 'content-type')
            return response
        else:
            response = self.get_response(request)
            response["Access-Control-Allow-Origin"] = "*"
            return response