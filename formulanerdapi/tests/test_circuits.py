from rest_framework.test import APITestCase
from rest_framework import status
from formulanerdapi.models import Circuit, Nation
from django.urls import reverse

class CircuitViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests"""
        cls.nation1 = Nation.objects.create(name="Germany", flag_image_url="https://example.com/germany.png")
        cls.nation2 = Nation.objects.create(name="Italy", flag_image_url="https://example.com/italy.png")

        cls.circuit1 = Circuit.objects.create(
            name="Hockenheimring",
            nation=cls.nation1,
            length=4.574,
            circuit_type="Permanent",
            designer="Hermann Tilke",
            year_built=1932,
            circuit_image_url="https://example.com/hockenheimring.png"
        )

        cls.circuit2 = Circuit.objects.create(
            name="Monza",
            nation=cls.nation2,
            length=5.793,
            circuit_type="Permanent",
            designer="Jovino di Giorgio",
            year_built=1922,
            circuit_image_url="https://example.com/monza.png"
        )

    def test_retrieve_circuit(self):
        """Test retrieving a single circuit"""
        response = self.client.get(f"/circuits/{self.circuit1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Hockenheimring")
    
    def test_list_circuits(self):
        """Test listing all circuits"""
        response = self.client.get("/circuits")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_circuits_by_nation(self):
        """Test listing circuits filtered by nation"""
        response = self.client.get(f"/circuits?nation={self.nation1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Hockenheimring")
    
    def test_create_circuit(self):
        """Test creating a new circuit"""
        data = {
            "name": "Silverstone",
            "nation_id": self.nation1.id,
            "length": 5.891,
            "circuit_type": "Permanent",
            "designer": "John Barnard",
            "year_built": 1948,
            "circuit_image_url": "https://example.com/silverstone.png"
        }
        response = self.client.post("/circuits", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Circuit.objects.count(), 3)
    
    def test_update_circuit(self):
        """Test updating an existing circuit"""
        data = {
            "name": "Updated Hockenheimring",
            "nation_id": self.nation1.id,
            "length": 4.600,
            "circuit_type": "Permanent",
            "designer": "Hermann Tilke",
            "year_built": 1932,
            "circuit_image_url": "https://example.com/updated_hockenheimring.png"
        }
        response = self.client.put(f"/circuits/{self.circuit1.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.circuit1.refresh_from_db()
        self.assertEqual(self.circuit1.name, "Updated Hockenheimring")
    
    def test_delete_circuit(self):
        """Test deleting a circuit"""
        response = self.client.delete(f"/circuits/{self.circuit2.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Circuit.objects.filter(id=self.circuit2.id).exists())
    
    def test_retrieve_nonexistent_circuit(self):
        """Test retrieving a circuit that does not exist"""
        response = self.client.get("/circuits/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Circuit not found"})
    
    def test_update_nonexistent_circuit(self):
        """Test updating a circuit that does not exist"""
        data = {
            "name": "Ghost Circuit",
            "nation_id": self.nation1.id,
            "length": 5.000,
            "circuit_type": "Permanent",
            "designer": "Unknown",
            "year_built": 2050,
            "circuit_image_url": "https://example.com/ghost_circuit.png"
        }
        response = self.client.put("/circuits/999", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_circuit(self):
        """Test deleting a circuit that does not exist"""
        response = self.client.delete("/circuits/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_circuit_with_missing_field(self):
        """Test creating a circuit with missing field"""
        data = {
            "name": "Bahrain International Circuit",
            "nation_id": self.nation2.id,
            "length": 5.412,
            "circuit_type": "Permanent",
            "designer": "Hermann Tilke",
            "year_built": 2004
        }
        response = self.client.post("/circuits", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Missing field: 'circuit_image_url'"})
    
    def test_create_circuit_with_invalid_nation(self):
        """Test creating a circuit with an invalid nation"""
        data = {
            "name": "Abu Dhabi Circuit",
            "nation_id": 999,
            "length": 5.281,
            "circuit_type": "Permanent",
            "designer": "Hermann Tilke",
            "year_built": 2009,
            "circuit_image_url": "https://example.com/abu_dhabi.png"
        }
        response = self.client.post("/circuits", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "circuit or related object not found."})
    
    def test_create_circuit_with_invalid_nation(self):
        """Test creating a circuit with an invalid nation"""
        data = {
            "name": "Abu Dhabi Circuit",
            "nation_id": 999,
            "length": 5.281,
            "circuit_type": "Permanent",
            "designer": "Hermann Tilke",
            "year_built": 2009,
            "circuit_image_url": "https://example.com/abu_dhabi.png"
        }
        response = self.client.post("/circuits", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Nation not found."})
