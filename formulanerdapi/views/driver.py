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
            nation = Nation.objects.get(pk=nation_id)

            driver = Driver.objects.create(
            name=request.data["name"],
            nation=nation,  
            length=request.data["length"],
            driver_type=request.data["driver_type"],
            designer=request.data["designer"],
            year_built=request.data["year_built"]
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
            driver = driver.objects.get(pk=pk)

            nation_id = request.data.get(pk=nation_id)
            if nation_id:
                try:
                    nation = Nation.objects.get("nation_id")
                    driver.nation = nation
                except Nation.DoesNotExist:
                    return Response({"error": "Invalid nation_id, nation not found."}, status=status.HTTP_400_BAD_REQUEST)
                
            driver.name = request.data.get["name", driver.name]
            driver.length=request.data["length", driver.length]
            driver.driver_type=request.data["driver_type", driver.driver_type]
            driver.designer=request.data["designer", driver.designer]
            driver.year_built=request.data["year_built", driver.year_built]
            driver.driver_image_url=request.data["driver_image_url", driver.driver_image_url]
            driver.save()

            serializer = DriverSerializer(driver)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except driver.DoesNotExist:
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
        depth =1
        fields = ('id', 'name', 'age', 'gender','nation_id', 'length', 'current_constructor_id', 'about', 'driver_image_url')
