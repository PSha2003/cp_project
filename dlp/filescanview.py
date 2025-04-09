from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from .scan_file import scan_file_for_sensitive_data

class FileScanView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']

        # Save the uploaded file to a temp location
        file_path = f'temp_{file.name}'
        with open(file_path, 'wb') as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)

        # Run the async DLP scan from sync context
        matches = async_to_sync(scan_file_for_sensitive_data)(file_path)

        if matches:
            return Response({'matches': matches}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No sensitive data found.'}, status=status.HTTP_200_OK)

