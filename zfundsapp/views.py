# rest-framework imports

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, AuthenticationFailed, PermissionDenied
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework import viewsets

#inter-app imports
from authentication.models import User
from authentication.serializers import UserSerializer
from zfundsapp.serializers import AdvisorAddClientSerializer, ProductsSerializer, OrderSerializer
from zfundsapp.models import Products, Order
# from core.utils import IsAdmin

#third-party imports
import uuid, datetime, pytz

# Create your views here.


class AdvisorAddClientView(APIView):

    """
       URL: {{HOST}}/app/add-clients/
       METHOD: [POST]
       BODY: {
                "client_name": "c",
                "client_email": "c@gmail.com",
                "client_usergroup": "Ad",
                "client_phone_number": "8989890980"
            }
    """
    serializer_class = AdvisorAddClientSerializer

    def post(self, request, *args, **kwargs):
        
        token = self.request.META.get('HTTP_KEY')
        if not token:
            raise ParseError('Please pass authentication token to proceed!')
        
        user = User.objects.filter(token=token).last()
        
        if not user:
            raise AuthenticationFailed('Invalid token provided, user not found!')
        
        from core.utils import validate_token
        if not validate_token(user.valid_from):
            raise AuthenticationFailed('Token expired!')
        
        if user.usergroup != 'Advisor':
            raise PermissionDenied('Permission denied! Only Advisors can add users.')
        
        data = request.data
        client_name = data.get('name', None)
        client_mobile = data.get('phone_number', None)
        client_email = data.get('email', None)
        
        if client_name is None:
            raise ParseError('please enter client name to proceed!')
        if client_mobile is None:
            raise ParseError('please enter client mobile to proceed!')
        if client_email is None:
            raise ParseError('please enter client email to proceed')
         
        client_user = User(
            name=client_name,
            email=client_email,
            phone_number=client_mobile,
            advisor=user
        )
        client_user.set_password('psf@123') # default password which user may change later
        client_user.save()
        client_user.username = client_name.split()[0] + '-' + str(client_user.id)
        client_user.save()

        return Response({
            'name': f'{client_user.name}',
            'phon_number': f'{client_user.phone_number}',
            'email': f'{client_user.email}',
            'advisor': f'{client_user.advisor}'
        }, status=status.HTTP_201_CREATED)

        
class GetAdvisorClientsView(ListAPIView):
    """
        URL: {{HOST}}/app/get-clients/
        METHOD: [GET]
        HEADERS: {
                    "KEY": "TOKEN",
                }
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):

        token = self.request.META.get('HTTP_KEY')
        if not token:
            raise ParseError('Please pass authentication token to proceed!')
        
        user = User.objects.filter(token=token).last()
        
        if not user:
            raise AuthenticationFailed('Invalid token provided, user not found!')
        
        from core.utils import validate_token
        if not validate_token(user.valid_from):
            raise AuthenticationFailed('Token expired!')
        
        if user.usergroup != 'Advisor':
            raise PermissionDenied('Permission denied! Only Advisors can see users.')
        
        data = self.queryset.filter(advisor=user)
        
        return data
    

class ProductsViewset(viewsets.ModelViewSet):
    """ 
        URL: {{HOST}}/app/products/
        METHOD: [GET/PUT/POST/DELETE]
        HEADERS: {
                    "KEY": "TOKEN",
                }
        BODY: {
                "name": "Reliance",
                "category": "mutual_funds",
                "code": "RMFS",
                "price": "12000"
            }
    """

    
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    
    def create(self, request, *args, **kwargs):
        token = self.request.META.get('HTTP_KEY')
        if not token:
            raise ParseError('Please pass authentication token to proceed!')
        
        user = User.objects.filter(token=token).last()
        
        if not user:
            raise AuthenticationFailed('Invalid token provided, user not found!')
        
        from core.utils import validate_token
        if not validate_token(user.valid_from):
            raise AuthenticationFailed('Token expired!')
        
        if user.usergroup != 'Admin':
            raise PermissionDenied('Permission denied! Admin users only.')
        

        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        token = self.request.META.get('HTTP_KEY')
        if not token:
            raise ParseError('Please pass authentication token to proceed!')
        
        user = User.objects.filter(token=token).last()
        
        if not user:
            raise AuthenticationFailed('Invalid token provided, user not found!')
        
        from core.utils import validate_token
        if not validate_token(user.valid_from):
            raise AuthenticationFailed('Token expired!')
                
        if user.usergroup != 'Advisor':
            raise PermissionDenied('Permission denied! Admin users only.')
        return super().list(request, *args, **kwargs)


class ListCreateOrderView(ListCreateAPIView):

    """ 
        URL: {{HOST}}/app/list-create-orders/
        METHOD: [GET/POST]
        HEADERS: {
                    "KEY": "TOKEN",
                }
        BODY: {
                "products": [1, 2],
                "status": "Complete",
                "total_price": 12000,
                "client_mobile": 1010101011
            }
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):

        token = self.request.META.get('HTTP_KEY')
        if not token:
            raise ParseError('Please pass authentication token to proceed!')
        
        user = User.objects.filter(token=token).last()
        
        if not user:
            raise AuthenticationFailed('Invalid token provided, user not found!')
        
        from core.utils import validate_token
        if not validate_token(user.valid_from):
            raise AuthenticationFailed('Token expired!')

        serializer = self.serializer_class(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        order_obj = serializer.save()
        
        if user.usergroup == 'Advisor':
            client_mobile = request.data.pop('client_mobile')
            client = User.objects.filter(phone_number=client_mobile).last()
            if not client:
                raise ParseError('Client not found!')
            order_obj.buyer = user
            order_obj.user = client
            order_obj.save()

        elif user.usergroup == 'Consumer':
            order_obj.user = user
            order_obj.save()
        
        # assigning unique link to each client and product
        order_obj.link = f'/{order_obj.id}/{order_obj.user.name}/{uuid.uuid4()}'
        order_obj.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        


