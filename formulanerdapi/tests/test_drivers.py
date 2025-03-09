from rest_framework.test import APITestCase
from rest_framework import status
from formulanerdapi.models import Driver, Constructor, Nation
from django.urls import reverse

class DriverViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests"""
        cls.nation1 = Nation.objects.create(name="Germany", flag_image_url="https://example.com/germany.png")
        cls.nation2 = Nation.objects.create(name="Italy", flag_image_url="https://example.com/italy.png")
        
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

    def test_retrieve_driver(self):
        """Test retrieving a single driver"""
        response = self.client.get(f"/drivers/{self.driver1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Lewis Hamilton")
    
    def test_list_drivers(self):
        """Test listing all drivers"""
        response = self.client.get("/drivers")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_list_drivers_by_nation(self):
        """Test listing drivers filtered by nation"""
        response = self.client.get("/drivers?nation=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Lewis Hamilton")
    
    def test_create_driver(self):
        """Test creating a new driver"""
        data = {
            "name": "Charles Leclerc",
            "age": 23,
            "gender": "Male",
            "nation_id": self.nation2.id,
            "current_constructor_id": self.constructor2.id,
            "about": "Young Ferrari driver",
            "driver_image_url": "https://example.com/leclerc.png"
        }
        response = self.client.post("/drivers", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 3)
    
    def test_update_driver(self):
        """Test updating an existing driver"""
        data = {
            "name": "Updated Hamilton",
            "age": 37,
            "gender": "Male",
            "nation_id": self.nation1.id,
            "current_constructor_id": self.constructor1.id,
            "about": "Updated driver info",
            "driver_image_url": "https://example.com/updated_hamilton.png"
        }
        response = self.client.put(f"/drivers/{self.driver1.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.driver1.refresh_from_db()
        self.assertEqual(self.driver1.name, "Updated Hamilton")
    
    def test_delete_driver(self):
        """Test deleting a driver"""
        response = self.client.delete(f"/drivers/{self.driver2.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Driver.objects.filter(id=self.driver2.id).exists())
    
    def test_retrieve_nonexistent_driver(self):
        """Test retrieving a driver that does not exist"""
        response = self.client.get("/drivers/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Driver not Found"})
    
    def test_update_nonexistent_driver(self):
        """Test updating a driver that does not exist"""
        data = {
            "name": "Ghost Driver",
            "age": 25,
            "gender": "Male",
            "nation_id": self.nation1.id,
            "current_constructor_id": self.constructor1.id,
            "about": "Ghost driver",
            "driver_image_url": "https://example.com/ghost_driver.png"
        }
        response = self.client.put("/drivers/999", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_driver(self):
        """Test deleting a driver that does not exist"""
        response = self.client.delete("/drivers/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_driver_with_missing_field(self):
        """Test creating a driver with missing field"""
        data = {
            "name": "Max Verstappen",
            "age": 24,
            "gender": "Male",
            "nation_id": self.nation1.id,
            "current_constructor_id": self.constructor1.id,
            "about": "Red Bull driver"
        }
        response = self.client.post("/drivers", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Missing field: 'driver_image_url'"})
    
    def test_create_driver_with_invalid_nation(self):
        """Test creating a driver with an invalid nation"""
        data = {
            "name": "Lando Norris",
            "age": 21,
            "gender": "Male",
            "nation_id": 999,
            "current_constructor_id": self.constructor1.id,
            "about": "McLaren driver",
            "driver_image_url": "https://example.com/norris.png"
        }
        response = self.client.post("/drivers", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Nation not found."})
    
    def test_create_driver_with_invalid_constructor(self):
        """Test creating a driver with an invalid constructor"""
        data = {
            "name": "Daniel Ricciardo",
            "age": 31,
            "gender": "Male",
            "nation_id": self.nation1.id,
            "current_constructor_id": 999,
            "about": "Driver",
            "driver_image_url": "https://example.com/ricciardo.png"
        }
        response = self.client.post("/drivers", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Constructor not found."})
