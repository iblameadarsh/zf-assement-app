from django.urls import path, include
from zfundsapp.views import AdvisorAddClientView, GetAdvisorClientsView, ProductsViewset, ListCreateOrderView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductsViewset, basename='products_crud_api')
urlpatterns = router.urls

urlpatterns = [
    path('add-client/', AdvisorAddClientView.as_view(), name='register_user'),
    path('get-clients/', GetAdvisorClientsView.as_view(), name='get_clients'),
    path('list-create-orders/', ListCreateOrderView.as_view(), name='get_or_create_orders')
    
]

urlpatterns += router.urls
