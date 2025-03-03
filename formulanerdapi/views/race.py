from django.http import HttpResponseServerError, Http404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from formulanerdapi.models import Nation, Race, Driver, Circuit
from django.core.exceptions import ObjectDoesNotExist

class RaceView(ViewSet):
    """Formula Nerd race view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single race

        Returns:
            Response -- JSON serialized race
        """
        try:
            race = Race.objects.get(pk=pk)
            serializer = RaceSerializer(race)
            return Response(serializer.data)
        except Race.DoesNotExist:
            raise Http404("Race not found")

    def list(self, request):
        """Handle GET requests to get all races

        Returns:
            Response -- JSON serialized list of races
        """
        races = Race.objects.all()
        serializer = RaceSerializer(races, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized race instance or error message
        """
        try:
            nation = Nation.objects.get(pk=request.data["nation_id"])
            circuit = Circuit.objects.get(pk=request.data["circuit_id"])
            winner_driver = Driver.objects.get(pk=request.data["winner_driver_id"])
            p2_driver = Driver.objects.get(pk=request.data["p2_driver_id"])
            p3_driver = Driver.objects.get(pk=request.data["p3_driver_id"])

            race = Race.objects.create(
                name=request.data["name"],
                circuit=circuit,
                date=request.data["date"],
                nation=nation,
                distance=request.data["distance"],
                laps=request.data["laps"],
                winner_driver=winner_driver,
                p2_driver=p2_driver,
                p3_driver=p3_driver
            )     

            serializer = RaceSerializer(race)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Nation.DoesNotExist:
            return Response({"error": "Nation not found."}, status=status.HTTP_400_BAD_REQUEST)
        except Circuit.DoesNotExist:
            return Response({"error": "Circuit not found."}, status=status.HTTP_400_BAD_REQUEST)
        except Driver.DoesNotExist:
            return Response({"error": "Driver not found."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        """Handle PUT requests for a race

        Returns:
            Response -- Updated race instance or error message
        """
        try:
            race = Race.objects.get(pk=pk)

            if "nation_id" in request.data:
                try:
                    nation = Nation.objects.get(pk=request.data["nation_id"])
                    race.nation = nation
                except Nation.DoesNotExist:
                    return Response({"error": "Invalid nation_id, nation not found."}, status=status.HTTP_400_BAD_REQUEST)

            if "circuit_id" in request.data:
                try:
                    circuit = Circuit.objects.get(pk=request.data["circuit_id"])
                    race.circuit = circuit
                except Circuit.DoesNotExist:
                    return Response({"error": "Invalid circuit_id, circuit not found."}, status=status.HTTP_400_BAD_REQUEST)

            if "winner_driver_id" in request.data:
                try:
                    winner_driver = Driver.objects.get(pk=request.data["winner_driver_id"])
                    race.winner_driver = winner_driver
                except Driver.DoesNotExist:
                    return Response({"error": "Invalid winner_driver_id, driver not found."}, status=status.HTTP_400_BAD_REQUEST)

            if "p2_driver_id" in request.data:
                try:
                    p2_driver = Driver.objects.get(pk=request.data["p2_driver_id"])
                    race.p2_driver = p2_driver
                except Driver.DoesNotExist:
                    return Response({"error": "Invalid p2_driver_id, driver not found."}, status=status.HTTP_400_BAD_REQUEST)

            if "p3_driver_id" in request.data:
                try:
                    p3_driver = Driver.objects.get(pk=request.data["p3_driver_id"])
                    race.p3_driver = p3_driver
                except Driver.DoesNotExist:
                    return Response({"error": "Invalid p3_driver_id, driver not found."}, status=status.HTTP_400_BAD_REQUEST)

            race.name = request.data.get("name", race.name)
            race.date = request.data.get("date", race.date)
            race.distance = request.data.get("distance", race.distance)
            race.laps = request.data.get("laps", race.laps)

            race.save()
            serializer = RaceSerializer(race)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Race.DoesNotExist:
            raise Http404("Race not found")
        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        """Handle DELETE requests for a race"""
        try:
            race = Race.objects.get(pk=pk)
            race.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Race.DoesNotExist:
            raise Http404("Race not found")

class RaceSerializer(serializers.ModelSerializer):
    """JSON serializer for races"""
    class Meta:
        model = Race
        depth = 3
        fields = ('id', 'name', 'circuit', 'date', 'nation', 'distance', 'laps', 'winner_driver', 'p2_driver', 'p3_driver')
