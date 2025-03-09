from rest_framework.test import APITestCase
from rest_framework import status
from formulanerdapi.models import Constructor, Nation
from django.urls import reverse

class ConstructorViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests"""
        cls.nation1 = Nation.objects.create(name="Germany", flag_image_url="https://example.com/germany.png")
        cls.nation2 = Nation.objects.create(name="Italy", flag_image_url="https://example.com/italy.png")
        
        cls.constructor1 = Constructor.objects.create(
            name="Mercedes",
            location="Stuttgart, Germany",
            nation=cls.nation1,
            is_engine_manufacturer=True,
            about="Leading F1 team",
            constructor_image_url="https://example.com/mercedes.png"
        )
        
        cls.constructor2 = Constructor.objects.create(
            name="Ferrari",
            location="Maranello, Italy",
            nation=cls.nation2,
            is_engine_manufacturer=False,
            about="Iconic F1 team",
            constructor_image_url="https://example.com/ferrari.png"
        )

    def test_retrieve_constructor(self):
        """Test retrieving a single constructor"""
        response = self.client.get(f"/constructors/{self.constructor1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Mercedes")
    
    def test_list_constructors(self):
        """Test listing all constructors"""
        response = self.client.get("/constructors")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_list_constructors_by_nation(self):
        """Test listing constructors filtered by nation"""
        response = self.client.get("/constructors?nation=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Mercedes")
    
    def test_create_constructor(self):
        """Test creating a new constructor"""
        data = {
            "name": "Red Bull",
            "location": "Milton Keynes, UK",
            "nation_id": self.nation1.id,
            "is_engine_manufacturer": False,
            "about": "Top F1 team",
            "constructor_image_url": "https://example.com/red_bull.png"
        }
        response = self.client.post("/constructors", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Constructor.objects.count(), 3)
    
    def test_update_constructor(self):
        """Test updating an existing constructor"""
        data = {
            "name": "Updated Mercedes",
            "location": "Updated Location",
            "nation_id": self.nation2.id,
            "is_engine_manufacturer": True,
            "about": "Updated team info",
            "constructor_image_url": "https://example.com/updated_mercedes.png"
        }
        response = self.client.put(f"/constructors/{self.constructor1.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.constructor1.refresh_from_db()
        self.assertEqual(self.constructor1.name, "Updated Mercedes")
    
    def test_delete_constructor(self):
        """Test deleting a constructor"""
        response = self.client.delete(f"/constructors/{self.constructor2.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Constructor.objects.filter(id=self.constructor2.id).exists())
    
    def test_retrieve_nonexistent_constructor(self):
        """Test retrieving a constructor that does not exist"""
        response = self.client.get("/constructors/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Constructor not found"})
    
    def test_update_nonexistent_constructor(self):
        """Test updating a constructor that does not exist"""
        data = {
            "name": "Ghost Constructor",
            "location": "Ghost Location",
            "nation_id": self.nation1.id,
            "is_engine_manufacturer": True,
            "about": "Ghost constructor",
            "constructor_image_url": "https://example.com/ghost_constructor.png"
        }
        response = self.client.put("/constructors/999", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_constructor(self):
        """Test deleting a constructor that does not exist"""
        response = self.client.delete("/constructors/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_constructor_with_missing_field(self):
        """Test creating a constructor with missing field"""
        data = {
            "name": "Alfa Romeo",
            "location": "Hinwil, Switzerland",
            "nation_id": self.nation2.id,
            "is_engine_manufacturer": False,
            "about": "F1 team"
        }
        response = self.client.post("/constructors", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Missing field: 'constructor_image_url'"})
    
    def test_create_constructor_with_invalid_nation(self):
        """Test creating a constructor with an invalid nation"""
        data = {
            "name": "Aston Martin",
            "location": "Silverstone, UK",
            "nation_id": 999,
            "is_engine_manufacturer": False,
            "about": "F1 team",
            "constructor_image_url": "https://example.com/aston_martin.png"
        }
        response = self.client.post("/constructors", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Nation not found."})
