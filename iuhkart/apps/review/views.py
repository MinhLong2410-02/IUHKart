from apps.review.serializers import ReviewSerializer, Review, CustomerReviewSerializer
from rest_framework import generics, permissions
from apps.review.pagination import ReviewPagination
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiParameter
# Create your views here.

@extend_schema(
    summary="Get a product's reviews from customer.",
    description="This endpoint allows the authenticated vendor to retrieve a paginated list of their products.",
    parameters=[
        OpenApiParameter(
            name='page',
            type=int,
            location=OpenApiParameter.QUERY,
            description='The page number.',
        ),
        OpenApiParameter(
            name='page_size',
            type=int,
            location=OpenApiParameter.QUERY,
            description='Number of products per page. Default is 10.',
        ),
    ]
)
class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product=product_id)


    
class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = CustomerReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)