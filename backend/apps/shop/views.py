from django.db import transaction
from rest_framework import filters, generics, permissions, status  # <--- Import filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, OrderItem, Product
from .serializers import CreateOrderSerializer, OrderSerializer, ProductSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]


# 2. Product Detail (Public)
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


# 3. Create Order (Authenticated Users Only)
class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic()
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        address = serializer.validated_data["shipping_address"]
        items_data = serializer.validated_data["items"]

        # Create Order
        order = Order.objects.create(user=request.user, shipping_address=address)
        total = 0

        for item in items_data:
            try:
                product = Product.objects.get(id=item["product_id"])
                qty = item["quantity"]

                if product.stock_quantity < qty:
                    raise Exception(f"Not enough stock for {product.name}")

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price_at_purchase=product.price,
                )

                product.stock_quantity -= qty
                product.save()

                total += product.price * qty
                # TODO: rediect to stripe or esewa to make the actual payment
                # TODO: create another endpoint to create actual order

            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=400)

            except Exception as e:
                return Response({"error": str(e)}, status=400)

        order.total_price = total
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


# 3. Order History (Authenticated Users Only)
class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")
