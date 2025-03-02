from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from formulanerdapi.models import DriverConstructorHistory
from formulanerdapi.models import Driver
from formulanerdapi.models import Constructor
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

class DriverConstructorHistoryView(ViewSet):
    """ driverConstructorHistory view"""

    def retrieve(self, request, pk):
        """Handle GET requests for drivers that have driven for a constructor


        Returns:
            Response -- JSON serialized driverConstructorHistory

        """
        driverConstructorHistory = DriverConstructorHistory.objects.get(pk=pk)
        serializer = DriverConstructorHistorySerializer(driverConstructorHistory)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all driver constructor histories

        Returns:
            Response -- JSON serialized list of circuits
        """
        driverConstructorHistories = DriverConstructorHistory.objects.all()

        serializer = DriverConstructorHistorySerializer(driverConstructorHistories, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations"""
        try:
            driver = Driver.objects.get(pk=request.data["driver_id"])
            constructor = Constructor.objects.get(pk=request.data["constructor_id"])

            driver_constructor_history = DriverConstructorHistory.objects.create(
                driver=driver,
                constructor=constructor,
                start_year=request.data.get("start_year"),
                end_year=request.data.get("end_year")
            )

            serializer = DriverConstructorHistorySerializer(driver_constructor_history)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Driver.DoesNotExist:
            return Response({"error": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)
        except Constructor.DoesNotExist:
            return Response({"error": "Constructor not found"}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk):
        """Handle PUT requests for a driverConstructorHistory"""

        try:
            driver_constructor_history = DriverConstructorHistory.objects.get(pk=pk)

            # Retrieve related objects to avoid ForeignKey constraint issues
            driver = Driver.objects.get(pk=request.data["driver_id"])
            constructor = Constructor.objects.get(pk=request.data["constructor_id"])

            driver_constructor_history.driver = driver
            driver_constructor_history.constructor = constructor
            driver_constructor_history.start_year = request.data.get("start_year", driver_constructor_history.start_year)
            driver_constructor_history.end_year = request.data.get("end_year", driver_constructor_history.end_year)

            driver_constructor_history.save()

            serializer = DriverConstructorHistorySerializer(driver_constructor_history)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Driver.DoesNotExist:
            return Response({"error": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)
        except Constructor.DoesNotExist:
            return Response({"error": "Constructor not found"}, status=status.HTTP_404_NOT_FOUND)
        except DriverConstructorHistory.DoesNotExist:
            return Response({"error": "DriverConstructorHistory not found"}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        try:
            driverConstructorHistory = DriverConstructorHistory.objects.get(pk=pk)
            driverConstructorHistory.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except DriverConstructorHistory.DoesNotExist:
            return Response({"error": "DriverConstructorHistory not found"}, status=status.HTTP_404_NOT_FOUND)


class DriverConstructorHistorySerializer(serializers.ModelSerializer):
    """JSON serializer for driver constructor history"""

    driver_id = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all())
    constructor_id = serializers.PrimaryKeyRelatedField(queryset=Constructor.objects.all())

    class Meta:
        model = DriverConstructorHistory
        depth =1
        fields = ('id', 'driver_id', 'constructor_id', 'start_year', 'end_year')
