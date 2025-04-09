import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from .scan_file import scan_file_for_sensitive_data
import os

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class FileScanView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if 'file' not in request.FILES:
            logger.warning("No file provided in request.")
            return JsonResponse({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']

        # Save the uploaded file to a temp location
        file_path = f'temp_{file.name}'

        try:
            with open(file_path, 'wb') as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)

            logger.info(f"File saved temporarily to {file_path}. Starting scan...")

            # Run the async DLP scan from sync context
            matches = async_to_sync(scan_file_for_sensitive_data)(file_path)

            # Clean up the temporary file after processing
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Temporary file {file_path} removed after processing.")

            if matches:
                return Response({'matches': matches}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No sensitive data found.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error while processing file {file.name}: {e}")
            # Ensure file cleanup even if an error occurs
            if os.path.exists(file_path):
                os.remove(file_path)
            return JsonResponse({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
