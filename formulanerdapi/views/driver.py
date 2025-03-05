from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
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
        driver = Driver.objects.get(pk=pk)
        serializer = DriverSerializer(driver)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all drivers

        Returns:
            Response -- JSON serialized list of drivers
        """
        drivers = Driver.objects.all()

        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized driver instance or error message
        """
        try:
            nation_id = request.data["nation_id"]
            current_constructor_id = request.data["current_constructor_id"]

            current_constructor = Constructor.objects.get(pk=current_constructor_id)
            nation = Nation.objects.get(pk=nation_id)

            driver = Driver.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            gender=request.data["gender"],
            nation=nation,  
            current_constructor=current_constructor,
            about=request.data["about"],
            driver_image_url=request.data["driver_image_url"]
            )     

            serializer = DriverSerializer(driver)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            # Handle missing fields
          return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
          return Response({"error": "driver or related object not found."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
        # Catch-all for any other errors
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
                
            driver.name = request.data.get("name", driver.name)
            driver.age=request.data("age", driver.age)
            driver.gender=request.data("gender", driver.gender)
            driver.nation=request.data("nation", driver.nation)
            driver.current_constructor=request.data("current_constructor", driver.current_constructor)
            driver.about=request.data("about", driver.about)
            driver.driver_image_url=request.data("driver_image_url", driver.driver_image_url)
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
