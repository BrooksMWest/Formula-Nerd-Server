from rest_framework.test import APITestCase
from rest_framework import status
from formulanerdapi.models import User, Nation, Driver, Circuit, Constructor
from django.urls import reverse

class UserViewTests(APITestCase):

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

        cls.circuit1 = Circuit.objects.create(name="Circuit de Spa", nation=cls.nation1)
        cls.circuit2 = Circuit.objects.create(name="Monza", nation=cls.nation2)

        cls.user1 = User.objects.create(
            uid="user_001",
            name="John Doe",
            nation=cls.nation1,
            favorite_driver=cls.driver1,
            favorite_circuit=cls.circuit1
        )
        cls.user2 = User.objects.create(
            uid="user_002",
            name="Jane Doe",
            nation=cls.nation2,
            favorite_driver=cls.driver2,
            favorite_circuit=cls.circuit2
        )

    def test_retrieve_user(self):
        """Test retrieving a single user"""
        response = self.client.get(f"/users/{self.user1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "John Doe")
    
    def test_list_users(self):
        """Test listing all users"""
        response = self.client.get("/users")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_create_user(self):
        """Test creating a new user"""
        data = {
            "uid": "user_003",
            "name": "Mark Smith",
            "nation_id": self.nation1.id,
            "favorite_driver_id": self.driver2.id,
            "favorite_circuit_id": self.circuit2.id
        }
        response = self.client.post("/users", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_create_user_with_missing_field(self):
        """Test creating a user with missing field"""
        data = {
            "uid": "user_004",
            "name": "Alice Cooper",
            "nation_id": self.nation2.id,
            "favorite_driver_id": self.driver1.id
        }
        response = self.client.post("/users", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Missing field: 'favorite_circuit_id'"})
    
    def test_create_user_with_invalid_nation(self):
        """Test creating a user with an invalid nation"""
        data = {
            "uid": "user_005",
            "name": "Chris Rock",
            "nation_id": 999,
            "favorite_driver_id": self.driver1.id,
            "favorite_circuit_id": self.circuit1.id
        }
        response = self.client.post("/users", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Nation not found."})
    
    def test_create_user_with_invalid_driver(self):
        """Test creating a user with an invalid driver"""
        data = {
            "uid": "user_006",
            "name": "David Tennant",
            "nation_id": self.nation1.id,
            "favorite_driver_id": 999,
            "favorite_circuit_id": self.circuit2.id
        }
        response = self.client.post("/users", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Driver not found."})
    
    def test_create_user_with_invalid_circuit(self):
        """Test creating a user with an invalid circuit"""
        data = {
            "uid": "user_007",
            "name": "Emma Watson",
            "nation_id": self.nation1.id,
            "favorite_driver_id": self.driver2.id,
            "favorite_circuit_id": 999
        }
        response = self.client.post("/users", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Circuit not found."})
    
    def test_update_user(self):
        """Test updating an existing user"""
        data = {
            "name": "Updated Name",
            "favorite_driver_id": self.driver1.id,
            "favorite_circuit_id": self.circuit2.id
        }
        response = self.client.put(f"/users/{self.user1.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.name, "Updated Name")
    
    def test_update_user_with_invalid_driver(self):
        """Test updating a user with an invalid driver"""
        data = {
            "favorite_driver_id": 999
        }
        response = self.client.put(f"/users/{self.user1.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Invalid favorite_driver_id, driver not found."})
    
    def test_update_user_with_invalid_circuit(self):
        """Test updating a user with an invalid circuit"""
        data = {
            "favorite_circuit_id": 999
        }
        response = self.client.put(f"/users/{self.user1.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Invalid favorite_circuit_id, circuit not found."})
    
    def test_delete_user(self):
        """Test deleting a user"""
        response = self.client.delete(f"/users/{self.user1.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())
    
    def test_retrieve_nonexistent_user(self):
        """Test retrieving a user that does not exist"""
        response = self.client.get("/users/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "User not found."})
    
    def test_update_nonexistent_user(self):
        """Test updating a user that does not exist"""
        data = {
            "name": "Ghost User",
            "favorite_driver_id": self.driver2.id,
            "favorite_circuit_id": self.circuit1.id
        }
        response = self.client.put("/users/999", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_user(self):
        """Test deleting a user that does not exist"""
        response = self.client.delete("/users/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
