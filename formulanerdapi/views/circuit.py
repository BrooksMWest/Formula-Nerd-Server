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

        try:
            circuit = Circuit.objects.get(pk=pk)
        except Circuit.DoesNotExist:
            return Response({"error": "Circuit not found"}, status=status.HTTP_404_NOT_FOUND)

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
            # Extract the nation_id from request data
            nation_id = request.data["nation_id"]
        
            # Try to fetch the nation using the provided nation_id
            try:
                nation = Nation.objects.get(pk=nation_id)
            except Nation.DoesNotExist:
                return Response({"error": "Nation not found."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the new circuit instance
            circuit = Circuit.objects.create(
                name=request.data["name"],
                nation=nation,  
                length=request.data["length"],
                circuit_type=request.data["circuit_type"],
                designer=request.data["designer"],
                year_built=request.data["year_built"],
                circuit_image_url=request.data["circuit_image_url"]
            )     

            # Serialize the circuit instance
            serializer = CircuitSerializer(circuit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            # Handle missing fields
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

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

            nation_id = request.data.get("nation_id")
            if nation_id:
                try:
                    nation = Nation.objects.get(id=nation_id)
                    circuit.nation = nation
                except Nation.DoesNotExist:
                    return Response({"error": "Invalid nation_id, nation not found."}, status=status.HTTP_400_BAD_REQUEST)

            # Update the circuit fields with the provided data or keep the existing value if not provided
            circuit.name = request.data.get("name", circuit.name)
            circuit.length = request.data.get("length", circuit.length)
            circuit.circuit_type = request.data.get("circuit_type", circuit.circuit_type)
            circuit.designer = request.data.get("designer", circuit.designer)
            circuit.year_built = request.data.get("year_built", circuit.year_built)
            circuit.circuit_image_url = request.data.get("circuit_image_url", circuit.circuit_image_url)

            # Save the updated circuit
            circuit.save()

            # Serialize the updated circuit data
            serializer = CircuitSerializer(circuit)
            return Response(serializer.data, status=status.HTTP_200_OK)  # Change to 200 OK

        except Circuit.DoesNotExist:
            return Response({"error": "Circuit not found"}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
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
