from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from .models import *
from laysans_backend.settings import EMAIL_HOST_USER
from .serizllers import *
from django.shortcuts import get_object_or_404

class Mail(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = MailSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            email2="careers@laysans.com"
            email3="sivaraj.t2001@gmail.com"


            # Compose email content
            email_body = f"From: {name} <{email}>\n\n{message}"

            try:
                email_message = EmailMessage(
                    subject=subject,
                    body=email_body,
                    from_email=EMAIL_HOST_USER,  
                    to=[email2],
                    reply_to=[email] 
                )
                email_message.send(fail_silently=False)

                email_message1 = EmailMessage(
                    subject='Thank you For Contacting Us',
                    body='We Have Received Your Query',
                    from_email=EMAIL_HOST_USER,  
                    to=[email],
                    reply_to=[email] 
                )
                email_message1.send(fail_silently=False)

                return Response(
                    {"message": "Sent successfully!"},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"error": f"Failed to send email: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CareerMail(APIView):
    @csrf_exempt
    def post(self, request):
        # Include request.FILES in request.data
        request_data = request.data.copy()
        request_data.update(request.FILES)

        serializer = CareersMailSerializer(data=request_data)

        if serializer.is_valid():
            name = serializer.validated_data['name']
            jobname = serializer.validated_data['JobName']
            email = serializer.validated_data['email']
            resume = request.FILES.get('resume') 
            message=serializer.validated_data['message']
            email2="contact@laysans.com"
            email3="sivaraj.t2001@gmail.com"

            # Compose email content
            email_body = f"From: {jobname} <{email}>"

            try:
                # Email to Admin (with resume attachment)
                email_message = EmailMessage(
                    subject=f"Apply For {jobname}",
                    body=email_body,
                    from_email=EMAIL_HOST_USER,
                    to=[email2],  # Send to the admin
                    reply_to=[email]
                )

                if resume:
                    email_message.attach(resume.name, resume.read(), resume.content_type)

                email_message.send(fail_silently=False)

                # Thank You Email to Sender (without attachment)
                email_message1 = EmailMessage(
                    subject='Thank you for contacting us',
                    body='We have received your query and will get back to you soon.',
                    from_email=EMAIL_HOST_USER,
                    to=[email],
                    reply_to=[EMAIL_HOST_USER]
                )
                email_message1.send(fail_silently=False)

                return Response(
                    {"message": "Email and resume sent successfully!"},
                    status=status.HTTP_200_OK
                )

            except Exception as e:
                return Response(
                    {"error": f"Failed to send email: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientAPI(APIView):
    def get(self, request):
        clients = Client.objects.all()  # Retrieve all clients
        serializer = ClientSerializer(clients, many=True, context={'request': request})  # Pass request in context
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CareersAPI(APIView):
    def get(self, request, id=None):
        if id:
            career = get_object_or_404(Careers, id=id)  # Use get_object_or_404
            serializer = CareerSerializer(career, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            careers = Careers.objects.all()
            serializer = CareerSerializer(careers, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        



# Assuming get_response is defined elsewhere
def get_response(message):
    return f"Chatbot Response: {message}"  # Dummy response function

class ChatAIView(APIView):
    def post(self, request, *args, **kwargs):
        print("POST request received in ChatAIView")

        try:
            # Extracting message from request body
            body_data = request.data  
            msg2 = body_data.get('message', '')

            if not msg2:
                return Response({"error": "Message field is required"}, status=status.HTTP_400_BAD_REQUEST)

            print(f"User message: {msg2}")

            # Getting chatbot response
            response = get_response(msg2)
            return Response({"answer": response}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
