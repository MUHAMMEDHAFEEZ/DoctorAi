from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MyModel
from .serializers import MyModelSerializer
import openai

openai.api_key = ""

class MyAPIView(APIView):
    def get(self, request):
        data = MyModel.objects.all()
        serializer = MyModelSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_input = request.data.get('content', '')  # Assuming 'content' is the field where the user input is stored

        # Use OpenAI API to generate a response
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Are you your a real doctor who prescribes treatment and medication"},
                {"role": "user", "content": user_input},
            ]
        )
        api_response = completion['choices'][0]['message']['content'].strip()

        # Save the user input and API response to the database
        serializer = MyModelSerializer(data={'name': user_input, 'description': api_response})
        if serializer.is_valid():
            serializer.save()

            # Custom response for a successful POST request
            response_data = {
                'message': f"{api_response}",
                'message_discraption': f"User input: {user_input}. DoctorAI response: {api_response}",
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
