from django.contrib.auth import authenticate
from django.http  import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import User
from .serializers import UserDetailSerializer
<<<<<<< HEAD
from property.serializers import ReservationsListSerializer
=======
>>>>>>> 45aaddc (Book property and Land lord page dynamic - Gutana, Reymar C.)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def landlord_detail(request, pk):
    user = User.objects.get(pk=pk)

    serializer = UserDetailSerializer(user, many=False)

<<<<<<< HEAD
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def reservation_list(request):
    reservations = request.user.reservations.all()

    print('user', request.user)
    print(reservations)
    
    serializer = ReservationsListSerializer(reservations, many=True)
=======
>>>>>>> 45aaddc (Book property and Land lord page dynamic - Gutana, Reymar C.)
    return JsonResponse(serializer.data, safe=False)