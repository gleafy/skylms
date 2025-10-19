from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer, UserCreateSerializer
from .services import create_stripe_product, create_stripe_price, create_stripe_session

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        payment = serializer.save()
        
        product_name = payment.course.title if payment.course else payment.lesson.title
        product_id = create_stripe_product(product_name)
        price_id = create_stripe_price(product_id, payment.amount)
        session_id, session_url = create_stripe_session(price_id)
        
        payment.stripe_product_id = product_id
        payment.stripe_price_id = price_id
        payment.stripe_session_id = session_id
        payment.payment_url = session_url
        payment.save()
        
        return Response({"payment_url": session_url}, status=status.HTTP_201_CREATED)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        payment = serializer.save()
        
        if payment.course:
            product_name = payment.course.title
        elif payment.lesson:
            product_name = payment.lesson.title
        else:
            return Response({"error": "Must specify course or lesson"}, status=status.HTTP_400_BAD_REQUEST)
        
        product_id = create_stripe_product(product_name)
        price_id = create_stripe_price(product_id, payment.amount)
        session_id, session_url = create_stripe_session(price_id)
        
        payment.stripe_product_id = product_id
        payment.stripe_price_id = price_id
        payment.stripe_session_id = session_id
        payment.payment_url = session_url
        payment.save()
        
        return Response({"payment_url": session_url}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        payment = self.get_object()
        return Response({"status": payment.status})