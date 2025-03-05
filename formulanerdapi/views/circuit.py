from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from formulanerdapi.models import Circuit
from formulanerdapi.models import Nation
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

class CircuitView(ViewSet):
    """Level up circuit view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single circuit by id
          get circuits by nation
          get circuits by name
          get circuits by type (maybe - might ditch it - no circuit table)
          get circuits by user favorites


        Returns:
            Response -- JSON serialized circuit
        """
        circuit = Circuit.objects.get(pk=pk)
        serializer = CircuitSerializer(circuit)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all circuits

        Returns:
            Response -- JSON serialized list of circuits
        """
        nation = request.query_params.get('nation', None)

        circuits = Circuit.objects.all()

        if nation is not None:
            circuits = circuits.filter(nation=nation)

        serializer = CircuitSerializer(circuits, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized circuit instance or error message
        """
        try:
            nation_id = request.data["nation_id"]
            nation = Nation.objects.get(pk=nation_id)

            circuit = Circuit.objects.create(
            name=request.data["name"],
            nation=nation,  
            length=request.data["length"],
            circuit_type=request.data["circuit_type"],
            designer=request.data["designer"],
            year_built=request.data["year_built"],
            circuit_image_url=request.data["circuit_image_url"]
            )     

            serializer = CircuitSerializer(circuit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            # Handle missing fields
          return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
          return Response({"error": "circuit or related object not found."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
        # Catch-all for any other errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

    def update(self, request, pk):
        """Handle PUT requests for a circuit

        Returns:
            Response -- Empty body with 204 status code or error message
        """
        try:
            circuit = Circuit.objects.get(pk=pk)

            nation_id = request.data.get(pk=nation_id)
            if nation_id:
                try:
                    nation = Nation.objects.get("nation_id")
                    circuit.nation = nation
                except Nation.DoesNotExist:
                    return Response({"error": "Invalid nation_id, nation not found."}, status=status.HTTP_400_BAD_REQUEST)
                
            circuit.name = request.data.get["name", circuit.name]
            circuit.length=request.data["length", circuit.length]
            circuit.circuit_type=request.data["circuit_type", circuit.circuit_type]
            circuit.designer=request.data["designer", circuit.designer]
            circuit.year_built=request.data["year_built", circuit.year_built]
            circuit.circuit_image_url=request.data["circuit_image_url", circuit.circuit_image_url]
            circuit.save()

            serializer = CircuitSerializer(circuit)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except circuit.DoesNotExist:
            raise Http404("circuit not found")
        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        try:
            circuit = Circuit.objects.get(pk=pk)
            circuit.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Circuit.DoesNotExist:
            raise Http404("Circuit not found")

class CircuitSerializer(serializers.ModelSerializer):
    """JSON serializer for circuits
    """
    class Meta:
        model = Circuit
        depth =1
        fields = ('id', 'name', 'nation', 'length', 'circuit_type', 'designer', 'year_built', 'circuit_image_url')
