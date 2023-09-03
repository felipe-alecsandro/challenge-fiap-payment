# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payment.serializers.transactions import TransactionSerializer
from payment.use_cases.webhooks import ProcessWebhookUseCase

class TransactionWebhookView(APIView):
    serializer_class = TransactionSerializer

    def post(self, request):
        # Parse and validate the incoming webhook payload
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Execute the use case to process the webhook payload
            webhook_payload = serializer.validated_data
            use_case = ProcessWebhookUseCase()
            use_case.execute(webhook_payload)

            # Respond with a success message
            return Response({'message': 'Webhook processed successfully'}, status=status.HTTP_200_OK)
        else:
            # Respond with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
