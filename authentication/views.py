# rest-framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, AuthenticationFailed
from rest_framework import status

#inter-app imports
from authentication.models import User
from authentication.serializers import UserSerializer

#third-party imports
import uuid, datetime, pytz

# Create your views here.


class UserRegisterView(APIView):
    
    """
       URL: {{HOST}}/auth/register/
       METHOD: [POST]
       BODY: {
                "name": "c",
                "email": "c@gmail.com",
                "password": "psf@123",
                "otp": "123456",
                "usergroup": "Ad",
                "phone_number": "8989890980"
            }
    """

    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        otp = request.data.pop('otp', None)
        if not otp:
            raise ParseError('Please enter to otp to proceed!')
        if len(otp) != 6:
            raise ParseError('Invalid otp!')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class UserLoginView(APIView):

    """
       URL: {{HOST}}/auth/login/
       METHOD: [POST]
       BODY: {
                "phonenumber": "8989890980",
                "otp": "234512"
            }
    """

    
    def post(self, request, *args, **kwargs):
        data = request.data
        phonenumber = data.get('phonenumber', None)
        otp = data.get('otp', None)
        if not otp:
            raise ParseError('Please enter to otp to proceed!')
        
        '''
        Usually "Authentication Failed" exception is thrown when passwords dont match 
        but in this case we're using mock otp for a demonstration of authentication.
        ''' 
        
        if len(otp) != 6:
            raise AuthenticationFailed('Invalid otp, enter valid otp to proceed!')
        
        user = User.objects.filter(phone_number=phonenumber).last()
        if not user:
            raise AuthenticationFailed('User not found!')
        
        token = uuid.uuid4()
        user.token = token
        utc = pytz.UTC
        user.valid_from = utc.localize(datetime.datetime.now())
        user.save()
        
        return Response(
            {
                'message': 'success!',
                'token': token
            }
        )


class UserRetrieveView(APIView):
    
    """
       URL: {{HOST}}/auth/login/
       METHOD: [GET]
       HEADERS: {
                    "KEY": "TOKEN",
                }
    """
    
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):

        token = self.request.META.get('HTTP_KEY')
        if not token:
            raise ParseError('Please pass authentication token to proceed!')
        user = User.objects.filter(token=token).last()
        if not user:
            raise AuthenticationFailed('Invalid token provided, user not found!')
        
        from core.utils import validate_token
        if not validate_token(user.valid_from):
            raise AuthenticationFailed('Token expired!')
        serializer = self.serializer_class(user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


