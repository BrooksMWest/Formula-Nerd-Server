from rest_framework.test import APITestCase
from rest_framework import status
from formulanerdapi.models import Nation

class NationViewTests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests"""
        cls.nation1 = Nation.objects.create(name="Germany", flag_image_url="https://example.com/germany.png")
        cls.nation2 = Nation.objects.create(name="Italy", flag_image_url="https://example.com/italy.png")
    
    def test_retrieve_nation(self):
        """Test retrieving a single nation"""
        response = self.client.get(f"/nations/{self.nation1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Germany")
    
    def test_list_nations(self):
        """Test listing all nations"""
        response = self.client.get("/nations")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_create_nation(self):
        """Test creating a new nation"""
        data = {"name": "France", "flag_image_url": "https://example.com/france.png"}
        response = self.client.post("/nations", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Nation.objects.count(), 3)
    
    def test_update_nation(self):
        """Test updating an existing nation"""
        data = {"name": "Updated Germany", "flag_image_url": "https://example.com/updated_germany.png"}
        response = self.client.put(f"/nations/{self.nation1.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.nation1.refresh_from_db()
        self.assertEqual(self.nation1.name, "Updated Germany")
    
    def test_delete_nation(self):
        """Test deleting a nation"""
        response = self.client.delete(f"/nations/{self.nation2.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Nation.objects.filter(id=self.nation2.id).exists())
    
    def test_retrieve_nonexistent_nation(self):
        """Test retrieving a nation that does not exist"""
        response = self.client.get("/nations/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_nonexistent_nation(self):
        """Test updating a nation that does not exist"""
        data = {"name": "Ghost Nation", "flag_image_url": "https://example.com/ghost.png"}
        response = self.client.put("/nations/999", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_nation(self):
        """Test deleting a nation that does not exist"""
        response = self.client.delete("/nations/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
