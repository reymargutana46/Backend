from tracemalloc import start
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from .forms import PropertyForm
from .models import Property, Reservation
from .serializers import PropertiesListSerializer, PropertyDetailSerializer, ReservationsListSerializer
from useraccount.models import User


def _get_request_user(request):
    """Resolve the authenticated user from JWT header or request."""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')

    if auth_header.startswith('Bearer '):
        token_str = auth_header.split('Bearer ')[1].strip()

        try:
            token = AccessToken(token_str)
            user_id = token.payload.get('user_id')

            if user_id:
                return User.objects.get(pk=user_id)
        except Exception:
            pass

    if getattr(request, 'user', None) and request.user.is_authenticated:
        return request.user

    return None


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    #
    #Auth

    user = _get_request_user(request)

    print('user', user)

    #
    #
    favorites = []
    properties = Property.objects.all()

    #
    #Filter

    favorites_param = request.GET.get('favorites')
    is_favorites_param = request.GET.get('is_favorites')
    favorites_filter = False

    truthy_values = {'1', 'true', 'yes'}

    if favorites_param is not None:
        favorites_filter = str(favorites_param).lower() in truthy_values
    elif is_favorites_param is not None:
        favorites_filter = str(is_favorites_param).lower() in truthy_values
    landlord_id = request.GET.get('landlord_id', '')

    if landlord_id:
        properties = properties.filter(landlord_id=landlord_id)
    
    if favorites_filter:
        if user:
            properties = properties.filter(favorited__in=[user]).distinct()
        else:
            properties = Property.objects.none()

    #
    #Favorites

    if user:
        for property in properties:
            if property.favorited.filter(pk=user.pk).exists():
                favorites.append(property.id)

    #
    serializer = PropertiesListSerializer(properties, many=True)

    return JsonResponse({
        'data': serializer.data,
        'favorites': favorites
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    property = Property.objects.get(pk=pk)

    serializer = PropertyDetailSerializer(property, many=False)

    return JsonResponse(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_reservations(request, pk):
    reservations = Property.reservations.all()

    serializer = ReservationsListSerializer(reservations, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST', 'FILES'])
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)

    if form.is_valid():
        property = form.save(commit=False)
        property.landlord = request.user
        property.save()

        return JsonResponse({'success': True})
    else:
        print('error', form.errors, form.non_field_errors)
        return JsonResponse({'error': form.errors.as_json()}, status=400)


@api_view(['POST'])
def book_property(request, pk):
    try:
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        number_of_nights = request.POST.get('number_of_nights', '')
        total_price = request.POST.get('total_price', '')
        guests = request.POST.get('guests', '')

        property = Property.objects.get(pk=pk)

        Reservation.objects.create(
            property=property,
            start_date=start_date,
            end_date=end_date,
            number_of_nights=number_of_nights,
            total_price=total_price,
            guests=guests,
            created_by=request.user
        )

        return JsonResponse({'success': True})
    except Exception as e:
        print('error', e)

        return JsonResponse({'success': False})


@api_view(['POST'])
def toggle_favorite(request, pk):
    user = _get_request_user(request)

    if not user:
        return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

    property = Property.objects.get(pk=pk)

    if property.favorited.filter(pk=user.pk).exists():
        property.favorited.remove(user)

        return JsonResponse({'is_favorite': False})
    else:
        property.favorited.add(user)

        return JsonResponse({'is_favorite': True})
