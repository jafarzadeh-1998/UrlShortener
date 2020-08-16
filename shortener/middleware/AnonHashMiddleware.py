import uuid

class AnonHashMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        """
        If user is not authenticated (anonymous) we set session hashcode
        uuid4 hex
        """
        if not request.user.is_authenticated and \
                'hashcode' not in request.session:
            request.session['hashcode'] = uuid.uuid4().hex


    def __call__(self, request):
        response = self.get_response(request)        
        self.process_request(request)
        
        return response