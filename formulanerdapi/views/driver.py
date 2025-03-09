from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import serializers, status
from formulanerdapi.models import Driver
from formulanerdapi.models import Constructor
from formulanerdapi.models import Nation
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

class DriverView(ViewSet):
    """Formula Nerd driver view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single driver

        Returns:
            Response -- JSON serialized driver
        """
        try:
            driver = Driver.objects.get(pk=pk)
        except Driver.DoesNotExist:
            return Response({"error": "Driver not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DriverSerializer(driver)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all drivers

        Returns:
            Response -- JSON serialized list of drivers
        """
        nation = request.query_params.get('nation', None)

        drivers = Driver.objects.all()

        if nation is not None:
            drivers = drivers.filter(nation=nation)

        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized driver instance or error message
        """
        required_fields = [
            "name", "age", "gender", "nation_id", "current_constructor_id", "about", "driver_image_url"
        ]
    
        # Check for missing required fields
        for field in required_fields:
            if field not in request.data:
                return Response({"error": f"Missing field: {field}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve nation and constructor, handle cases where they are not found
            nation_id = request.data["nation_id"]
            current_constructor_id = request.data["current_constructor_id"]

            current_constructor = Constructor.objects.get(pk=current_constructor_id)
            nation = Nation.objects.get(pk=nation_id)

            # Create driver instance
            driver = Driver.objects.create(
                name=request.data["name"],
                age=request.data["age"],
                gender=request.data["gender"],
                nation=nation,  
                current_constructor=current_constructor,
                about=request.data["about"],
                driver_image_url=request.data["driver_image_url"]
            )     

            # Serialize the driver instance and return the response
            serializer = DriverSerializer(driver)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Nation.DoesNotExist:
            return Response({"error": "Nation not found."}, status=status.HTTP_400_BAD_REQUEST)

        except Constructor.DoesNotExist:
            return Response({"error": "Constructor not found."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
           # Catch all other errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk):
        """Handle PUT requests for a driver

        Returns:
            Response -- Empty body with 204 status code or error message
        """
        try:
            driver = Driver.objects.get(pk=pk)

            nation_id = request.data.get("nation_id")
            if nation_id:
                try:
                    nation = Nation.objects.get(pk=nation_id)
                    driver.nation = nation
                except Nation.DoesNotExist:
                    return Response({"error": "Invalid nation_id, nation not found."}, status=status.HTTP_400_BAD_REQUEST)
                
            current_constructor_id = request.data.get("current_constructor_id")
            if current_constructor_id:
                try:
                    current_constructor = Constructor.objects.get(pk=current_constructor_id)
                    driver.current_constructor = current_constructor
                except Constructor.DoesNotExist:
                    return Response({"error": "Invalid current_constructor_id, constructor not found."}, status=status.HTTP_400_BAD_REQUEST)
                
            driver.name = request.data.get("name", driver.name)
            driver.age=request.data.get("age", driver.age)
            driver.gender=request.data.get("gender", driver.gender)
            driver.nation=request.data.get("nation", driver.nation)
            driver.about=request.data.get("about", driver.about)
            driver.driver_image_url=request.data.get("driver_image_url", driver.driver_image_url)
            driver.save()

            serializer = DriverSerializer(driver)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except Driver.DoesNotExist:
            raise Http404("driver not found")
        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        try:
            driver = Driver.objects.get(pk=pk)
            driver.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Driver.DoesNotExist:
            raise Http404("driver not found")

class DriverSerializer(serializers.ModelSerializer):
    """JSON serializer for drivers
    """
    class Meta:
        model = Driver
        fields = ('id', 'name', 'age', 'gender','nation', 'current_constructor', 'about', 'driver_image_url')
        depth = 3
