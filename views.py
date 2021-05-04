from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from application.movie.serializers import UserRegistrationSerializer
from rest_framework.generics import RetrieveAPIView
from application.movie.serializers import UserLoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from application.movie.profile.models import UserProfile
from django.shortcuts import render
from .models import Movie

class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            }

        return Response(response, status=status_code)

class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

class UserProfileView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'username': user_profile.username,
                    'password': user_profile.password,
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)

# Create your views here.
def movies(request):
	movies = Movie.objects.all() #queryset containing all movies we just created
	return render(request=request, template_name="", context={'movies':movies})

def add_to_cart(request,book_id):
        if request.user.is_authenticated():
            try:
                book = Book.objects.get(pk=book_id)
            except ObjectDoesNotExist:
                pass
            else :
                try:
                    cart = Cart.objects.get(user = request.user, active = True)
                except ObjectDoesNotExist:
                    cart = Cart.objects.create(user = request.user)
                    cart.save()
                    cart.add_to_cart(book_id)
                    return redirect('cart')
                else:
                    return redirect('index')


def remove_from_cart(request, book_id):
    if request.user.is_authenticated():
        try:
            book = Book.objects.get(pk = book_id)
        except ObjectDoesNotExist:
            pass
        else:
            cart = Cart.objects.get(user = request.user, active = True)
            cart.remove_from_cart(book_id)
        return redirect('cart')
    else:
        return redirect('index')
