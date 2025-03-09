from rest_framework.test import APITestCase
from rest_framework import status
from formulanerdapi.models import Race, Nation, Circuit, Driver, Constructor
from django.urls import reverse

class RaceViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests"""
        cls.nation1 = Nation.objects.create(name="Germany", flag_image_url="https://example.com/germany.png")
        cls.nation2 = Nation.objects.create(name="Italy", flag_image_url="https://example.com/italy.png")
        
        cls.circuit1 = Circuit.objects.create(name="Circuit de Spa", nation=cls.nation1)
        cls.circuit2 = Circuit.objects.create(name="Monza", nation=cls.nation2)

        cls.constructor1 = Constructor.objects.create(name="Mercedes", nation=cls.nation1)
        cls.constructor2 = Constructor.objects.create(name="Ferrari", nation=cls.nation2)
        
        cls.driver1 = Driver.objects.create(
            name="Lewis Hamilton",
            age=36,
            gender="Male",
            nation=cls.nation1,
            current_constructor=cls.constructor1,
            about="Famous Formula 1 driver",
            driver_image_url="https://example.com/hamilton.png"
        )
        cls.driver2 = Driver.objects.create(
            name="Sebastian Vettel",
            age=34,
            gender="Male",
            nation=cls.nation2,
            current_constructor=cls.constructor2,
            about="Former Formula 1 driver",
            driver_image_url="https://example.com/vettel.png"
        )
        
        cls.race1 = Race.objects.create(
            name="Belgian Grand Prix",
            circuit=cls.circuit1,
            date="2025-08-30",
            nation=cls.nation1,
            distance=308.052,
            laps=44,
            winner_driver=cls.driver1,
            p2_driver=cls.driver2,
            p3_driver=cls.driver1
        )
        
        cls.race2 = Race.objects.create(
            name="Italian Grand Prix",
            circuit=cls.circuit2,
            date="2025-09-06",
            nation=cls.nation2,
            distance=306.720,
            laps=53,
            winner_driver=cls.driver2,
            p2_driver=cls.driver1,
            p3_driver=cls.driver2
        )

    def test_retrieve_race(self):
        """Test retrieving a single race"""
        response = self.client.get(f"/races/{self.race1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Belgian Grand Prix")
    
    def test_list_races(self):
        """Test listing all races"""
        response = self.client.get("/races")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_list_races_by_nation(self):
        """Test listing races filtered by nation"""
        response = self.client.get("/races?nation=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Belgian Grand Prix")
    
    def test_create_race(self):
        """Test creating a new race"""
        data = {
            "name": "French Grand Prix",
            "date": "2025-06-28",
            "nation_id": self.nation1.id,
            "circuit_id": self.circuit1.id,
            "distance": 309.690,
            "laps": 53,
            "winner_driver_id": self.driver1.id,
            "p2_driver_id": self.driver2.id,
            "p3_driver_id": self.driver1.id
        }
        response = self.client.post("/races", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Race.objects.count(), 3)
    
    def test_update_race(self):
        """Test updating an existing race"""
        data = {
            "name": "Updated Italian Grand Prix",
            "date": "2025-09-13",
            "distance": 310.010,
            "laps": 53
        }
        response = self.client.put(f"/races/{self.race2.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.race2.refresh_from_db()
        self.assertEqual(self.race2.name, "Updated Italian Grand Prix")
    
    def test_delete_race(self):
        """Test deleting a race"""
        response = self.client.delete(f"/races/{self.race1.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Race.objects.filter(id=self.race1.id).exists())
    
    def test_retrieve_nonexistent_race(self):
        """Test retrieving a race that does not exist"""
        response = self.client.get("/races/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Race not Found"})
    
    def test_update_nonexistent_race(self):
        """Test updating a race that does not exist"""
        data = {
            "name": "Ghost Race",
            "date": "2025-10-12",
            "nation_id": self.nation2.id,
            "circuit_id": self.circuit2.id,
            "distance": 305.000,
            "laps": 53
        }
        response = self.client.put("/races/999", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_race(self):
        """Test deleting a race that does not exist"""
        response = self.client.delete("/races/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_race_with_missing_field(self):
        """Test creating a race with missing field"""
        data = {
            "name": "Spanish Grand Prix",
            "date": "2025-05-10",
            "nation_id": self.nation2.id,
            "circuit_id": self.circuit2.id,
            "distance": 307.104,
            "laps": 66
        }
        response = self.client.post("/races", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Missing field: 'winner_driver_id'"})
    
    def test_create_race_with_invalid_nation(self):
        """Test creating a race with an invalid nation"""
        data = {
            "name": "Dutch Grand Prix",
            "date": "2025-07-25",
            "nation_id": 999,
            "circuit_id": self.circuit1.id,
            "distance": 305.000,
            "laps": 72,
            "winner_driver_id": self.driver1.id,
            "p2_driver_id": self.driver2.id,
            "p3_driver_id": self.driver1.id
        }
        response = self.client.post("/races", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Nation not found."})
    
    def test_create_race_with_invalid_circuit(self):
        """Test creating a race with an invalid circuit"""
        data = {
            "name": "Canadian Grand Prix",
            "date": "2025-06-14",
            "nation_id": self.nation1.id,
            "circuit_id": 999,
            "distance": 305.000,
            "laps": 70,
            "winner_driver_id": self.driver1.id,
            "p2_driver_id": self.driver2.id,
            "p3_driver_id": self.driver1.id
        }
        response = self.client.post("/races", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Circuit not found."})
    
    def test_create_race_with_invalid_driver(self):
        """Test creating a race with an invalid driver"""
        data = {
            "name": "Austrian Grand Prix",
            "date": "2025-07-04",
            "nation_id": self.nation1.id,
            "circuit_id": self.circuit1.id,
            "distance": 305.000,
            "laps": 71,
            "winner_driver_id": 999,
            "p2_driver_id": self.driver2.id,
            "p3_driver_id": self.driver1.id
        }
        response = self.client.post("/races", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Driver not found."})
