from rest_framework.response import Response
from rest_framework.views import APIView


class UserView(APIView):
    def get(self, request):
        return Response({'message': 'Response from UserView GET method'})

    def post(self, request):
        pass

    def put(self, request, id):
        pass

    def delete(self, request, id):
        pass

    def patch(self, request, id):
        pass
