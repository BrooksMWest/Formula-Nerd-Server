from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from formulanerdapi.models import Nation
from formulanerdapi.models import Constructor
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
class ConstructorView(ViewSet):
    """Formula Nerd constructor view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single constructor

        Returns:
            Response -- JSON serialized constructor
        """
        try:
            constructor = Constructor.objects.get(pk=pk)
        except Constructor.DoesNotExist:
            return Response({"error": "Constructor not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConstructorSerializer(constructor)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all constructors

        Returns:
            Response -- JSON serialized list of constructors
        """
        nation = request.query_params.get('nation', None)

        constructors = Constructor.objects.all()

        if nation is not None:
            constructors = constructors.filter(nation=nation)

        serializer = ConstructorSerializer(constructors, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized constructor instance or error message
        """
        try:
            # Extract the nation_id from request data
            nation_id = request.data["nation_id"]
        
            # Try to fetch the nation using the provided nation_id
            try:
                nation = Nation.objects.get(pk=nation_id)
            except Nation.DoesNotExist:
                return Response({"error": "Nation not found."}, status=status.HTTP_400_BAD_REQUEST)


            nation_id = request.data["nation_id"]
            nation = Nation.objects.get(pk=nation_id)

            constructor = Constructor.objects.create(
            name=request.data["name"],
            location=request.data["location"],
            nation=nation,  
            is_engine_manufacturer=request.data["is_engine_manufacturer"],
            about=request.data["about"],
            constructor_image_url=request.data["constructor_image_url"]
            )     

            serializer = ConstructorSerializer(constructor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            # Handle missing fields
          return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
          return Response({"error": "constructor or related object not found."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
        # Catch-all for any other errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

    def update(self, request, pk):
        """Handle PUT requests for a constructor

        Returns:
            Response -- Empty body with 204 status code or error message
        """
        try:
            constructor = Constructor.objects.get(pk=pk)

            nation_id = request.data.get("nation_id")
            if nation_id:
                try:
                    nation = Nation.objects.get(pk=nation_id)
                    constructor.nation = nation
                except Nation.DoesNotExist:
                    return Response({"error": "Invalid nation_id, nation not found."}, status=status.HTTP_400_BAD_REQUEST)
                
            constructor.name = request.data.get("name", constructor.name)
            constructor.location = request.data.get("location", constructor.location)
            is_engine_manufacturer = request.data.get("is_engine_manufacturer")
            if is_engine_manufacturer is not None:
                constructor.is_engine_manufacturer = is_engine_manufacturer in ("true", "True", True)
            
            constructor.about = request.data.get("about", constructor.about)
            constructor.constructor_image_url = request.data.get("constructor_image_url", constructor.constructor_image_url)
            constructor.save()

            serializer = ConstructorSerializer(constructor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Constructor.DoesNotExist:
            raise Http404("constructor not found")
        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        try:
            constructor = Constructor.objects.get(pk=pk)
            constructor.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Constructor.DoesNotExist:
            return Response({"error": "Constructor not found"}, status=status.HTTP_404_NOT_FOUND)

class ConstructorSerializer(serializers.ModelSerializer):
    """JSON serializer for constructors
    """
    class Meta:
        model = Constructor
        depth =2
        fields = ('id', 'name', 'location', 'nation', 'is_engine_manufacturer', 'about','constructor_image_url')
