from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from formulanerdapi.models import Driver
from formulanerdapi.models import User
from formulanerdapi.models import Nation
from formulanerdapi.models import Circuit
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

class UserView(ViewSet):
    """Formula Nerd user view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user
        """
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all users

        Returns:
            Response -- JSON serialized list of users
        """
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized user instance or error message
        """
        try:
            nation = None
            favorite_driver = None
            favorite_circuit = None

            if "nation_id" in request.data:
                nation = Nation.objects.get(pk=request.data["nation_id"])

            if "favorite_driver_id" in request.data:
                favorite_driver = Driver.objects.get(pk=request.data["favorite_driver_id"])

            if "favorite_circuit_id" in request.data:
                favorite_circuit = Circuit.objects.get(pk=request.data["favorite_circuit_id"])

            user = User.objects.create(
            uid=request.data["uid"],
            name=request.data["name"],
            nation=nation,
            favorite_driver=favorite_driver,
            favorite_circuit=favorite_circuit
            )     

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            # Handle missing fields
          return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        
        except Nation.DoesNotExist:
            return Response({"error": "Nation not found."}, status=status.HTTP_400_BAD_REQUEST)
        except Driver.DoesNotExist:
            return Response({"error": "Driver not found."}, status=status.HTTP_400_BAD_REQUEST)
        except Circuit.DoesNotExist:
            return Response({"error": "Circuit not found."}, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
        # Catch-all for any other errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

    def update(self, request, pk):
        """Handle PUT requests for a user

        Returns:
            Response -- Empty body with 204 status code or error message
        """
        try:
            user = User.objects.get(pk=pk)

            nation_id = request.data.get("nation_id")
            if nation_id:
                try:
                    nation = Nation.objects.get(pk=nation_id)
                    user.nation = nation
                except Nation.DoesNotExist:
                    return Response({"error": "Invalid nation_id, nation not found."}, status=status.HTTP_400_BAD_REQUEST)
                
            user.uid = request.data.get("uid", user.uid)
            user.name = request.data.get("name", user.name)
            user.nation=request.data.get("nation_id", user.nation)
            user.favorite_driver=request.data("favorite_driver_id", user.favorite_driver)
            user.favorite_circuit.data("favorite_circuit_id", user.favorite_circuit)
            user.save()

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise Http404("user not found")
        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users
    """
    class Meta:
        model = User
        depth = 2
        fields = ('id', 'uid', 'name', 'nation', 'favorite_driver', 'favorite_circuit')
