from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from .models import Product
from .serializers import ProductSerializer
from .utils.csv_validator import validate_and_parse_csv
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser



@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, FileUploadParser])
def upload_csv(request):
    """
    POST /api/upload/
    Upload and validate CSV file, save valid products to DB
    """
    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    valid_rows, invalid_rows = validate_and_parse_csv(uploaded_file)

    for row in valid_rows:
        Product.objects.update_or_create(sku=row['sku'], defaults=row)

    return Response({
        'valid_count': len(valid_rows),
        'invalid_count': len(invalid_rows),
        'invalid_rows': invalid_rows[:10]  # preview first few invalid rows
    }, status=status.HTTP_200_OK)



@api_view(['GET'])
def list_products(request):
    """
    GET /api/products/?page=1&limit=10
    """
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    products = Product.objects.all().order_by('id')
    paginator = Paginator(products, limit)
    serializer = ProductSerializer(paginator.get_page(page), many=True)
    return Response({
        'page': page,
        'total': paginator.count,
        'pages': paginator.num_pages,
        'results': serializer.data
    })


@api_view(['GET'])
def search_products(request):
    """
    GET /api/products/search/?brand=StreamThreads&color=Red&minPrice=500&maxPrice=2000
    """
    queryset = Product.objects.all()

    brand = request.GET.get('brand')
    color = request.GET.get('color')
    min_price = request.GET.get('minPrice')
    max_price = request.GET.get('maxPrice')

    if brand:
        queryset = queryset.filter(brand__icontains=brand)
    if color:
        queryset = queryset.filter(color__icontains=color)
    if min_price:
        queryset = queryset.filter(price__gte=float(min_price))
    if max_price:
        queryset = queryset.filter(price__lte=float(max_price))

    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)
