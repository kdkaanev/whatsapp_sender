from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
import io
from .models import Contact
from .serializers import ContactSerializer


class ContactImportView(views.APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        
        if not file:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                return Response(
                    {'error': 'Unsupported file format. Use CSV or Excel.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            required_columns = ['name', 'phone_number']
            if not all(col in df.columns for col in required_columns):
                return Response(
                    {'error': f'File must contain columns: {", ".join(required_columns)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            created_contacts = []
            errors = []

            for idx, row in df.iterrows():
                try:
                    contact_data = {
                        'name': str(row['name']).strip(),
                        'phone_number': str(row['phone_number']).strip(),
                        'email': str(row.get('email', '')).strip() if 'email' in df.columns else ''
                    }

                    if not contact_data['name'] or not contact_data['phone_number']:
                        errors.append(f"Row {idx + 2}: Missing name or phone number")
                        continue

                    contact = Contact.objects.create(
                        user=request.user,
                        **contact_data
                    )
                    created_contacts.append(ContactSerializer(contact).data)

                except Exception as e:
                    errors.append(f"Row {idx + 2}: {str(e)}")

            return Response({
                'message': f'{len(created_contacts)} contacts imported successfully',
                'created': len(created_contacts),
                'errors': errors if errors else None,
                'contacts': created_contacts
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': f'Error processing file: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
