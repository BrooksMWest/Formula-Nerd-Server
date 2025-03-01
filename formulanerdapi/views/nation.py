from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from formulanerdapi.models import Nation
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

class NationView(ViewSet):
    """Formula Nerd Nation view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single nation

        Returns:
            Response -- JSON serialized nation
        """
        nation = Nation.objects.get(pk=pk)
        serializer = NationSerializer(nation)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all nations

        Returns:
            Response -- JSON serialized list of nations
        """
        nations = Nation.objects.all()

        serializer = NationSerializer(nations, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized author instance or error message
        """
        try:
            # Create the nation instance with validated data
            nation = Nation.objects.create(
            name=request.data["name"],
            flag_image_url=request.data["flag_image_url"],  # Ensure the key matches your frontend
            )     

            # Serialize and return the new book
            serializer = NationSerializer(nation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            # Handle missing fields
          return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
        # Handle foreign key errors or other object issues
          return Response({"error": "Nation or related object not found."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
        # Catch-all for any other errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

    def update(self, request, pk):
        """Handle PUT requests for a nation

        Returns:
            Response -- Empty body with 204 status code or error message
        """
        try:
            nation = Nation.objects.get(pk=pk)
            nation.name=request.data["name"]
            nation.flag_image_url=request.data["flag_image_url"]  
            nation.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Nation.DoesNotExist:
            raise Http404("Nation not found")
        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        try:
            nation = Nation.objects.get(pk=pk)
            nation.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Nation.DoesNotExist:
            raise Http404("Nation not found")


class NationSerializer(serializers.ModelSerializer):
    """JSON serializer for nations
    """
    class Meta:
        model = Nation
        depth =1
        fields = ('id', 'name', 'flag_image_url')
