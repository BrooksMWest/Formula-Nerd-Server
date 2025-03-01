from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from formulanerdapi.models import race
from formulanerdapi.models import Nation
from formulanerdapi.models import Race
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

class RaceView(ViewSet):
    """Formula Nerd race view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single race

        Returns:
            Response -- JSON serialized race
        """
        race = Race.objects.get(pk=pk)
        serializer = RaceSerializer(race)
        return Response(serializer.data)


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
            nation_id = request.data["nation_id"]
            nation = Nation.objects.get(pk=nation_id)

            race = race.objects.create(
            name=request.data["name"],
            nation=nation,  
            length=request.data["length"],
            race_type=request.data["race_type"],
            designer=request.data["designer"],
            year_built=request.data["year_built"]
            )     

            serializer = RaceSerializer(race)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            # Handle missing fields
          return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
          return Response({"error": "race or related object not found."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
        # Catch-all for any other errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

    def update(self, request, pk):
        """Handle PUT requests for a race

        Returns:
            Response -- Empty body with 204 status code or error message
        """
        try:
            race = race.objects.get(pk=pk)

            nation_id = request.data.get(pk=nation_id)
            if nation_id:
                try:
                    nation = Nation.objects.get("nation_id")
                    race.nation = nation
                except Nation.DoesNotExist:
                    return Response({"error": "Invalid nation_id, nation not found."}, status=status.HTTP_400_BAD_REQUEST)
                
            race.name = request.data.get["name", race.name]
            race.length=request.data["length", race.length]
            race.race_type=request.data["race_type", race.race_type]
            race.designer=request.data["designer", race.designer]
            race.year_built=request.data["year_built", race.year_built]
            race.race_image_url=request.data["race_image_url", race.race_image_url]
            race.save()

            serializer = RaceSerializer(race)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except race.DoesNotExist:
            raise Http404("race not found")
        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        try:
            race = race.objects.get(pk=pk)
            race.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except race.DoesNotExist:
            raise Http404("race not found")

class RaceSerializer(serializers.ModelSerializer):
    """JSON serializer for races
    """
    class Meta:
        model = race
        depth =1
        fields = ('id', 'name', 'nation_id', 'length', 'race_type', 'designer', 'year_built', 'race_image_url')
