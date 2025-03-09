from rest_framework.test import APITestCase
from rest_framework import status
from formulanerdapi.models import DriverConstructorHistory, Driver, Constructor, Nation
from django.urls import reverse

class DriverConstructorHistoryViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests"""
        cls.nation1 = Nation.objects.create(name="Germany", flag_image_url="https://example.com/germany.png")
        cls.nation2 = Nation.objects.create(name="Italy", flag_image_url="https://example.com/italy.png")
        cls.nation3 = Nation.objects.create(name="France", flag_image_url="https://example.com/france.png")

        cls.constructor1 = Constructor.objects.create(name="Mercedes", nation=cls.nation1)
        cls.constructor2 = Constructor.objects.create(name="Ferrari", nation=cls.nation2)
        cls.constructor3 = Constructor.objects.create(name="Renault", nation=cls.nation3)

        cls.driver1 = Driver.objects.create(name="Lewis Hamilton", nation=cls.nation2, current_constructor=cls.constructor2)
        cls.driver2 = Driver.objects.create(name="Sebastian Vettel", nation=cls.nation1,current_constructor=cls.constructor1 )
        cls.driver3 = Driver.objects.create(name="Pierre Gasly", nation=cls.nation3,current_constructor=cls.constructor3 )

        cls.history1 = DriverConstructorHistory.objects.create(
            driver=cls.driver1,
            constructor=cls.constructor1,
            start_year=1995,
            end_year=1997
          )
        cls.history2 = DriverConstructorHistory.objects.create(
            driver=cls.driver2,
            constructor=cls.constructor2,
            start_year=2001,
            end_year=2005
          )

        
    def test_retrieve_driver_constructor_history(self):
        """Test retrieving a single driver constructor history"""
        response = self.client.get(f"/driverconstructorhistories/{self.history1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["driver"]["name"], "Lewis Hamilton")
        self.assertEqual(response.data["constructor"]["name"], "Mercedes")

    def test_list_driver_constructor_histories(self):
        """Test listing all driver constructor histories"""
        response = self.client.get("/driverconstructorhistories")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_driver_constructor_histories_filtered_by_driver(self):
        """Test listing driver constructor histories filtered by driver"""
        response = self.client.get(f"/driverconstructorhistories?driver={self.driver1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["driver"]["name"], "Lewis Hamilton")

    def test_list_driver_constructor_histories_filtered_by_constructor(self):
        """Test listing driver constructor histories filtered by constructor"""
        response = self.client.get(f"/driverconstructorhistories?constructor={self.constructor1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["constructor"]["name"], "Mercedes")

    def test_create_driver_constructor_history(self):
        """Test creating a new driver constructor history"""
        data = {
            "driver_id": self.driver1.id,
            "constructor_id": self.constructor2.id,
            "start_year": 2021,
            "end_year": 2022
        }
        response = self.client.post("/driverconstructorhistories", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DriverConstructorHistory.objects.count(), 3)

    def test_create_driver_constructor_history_with_missing_field(self):
        """Test creating a driver constructor history with missing field"""
        data = {
            "driver_id": self.driver1.id,
            "constructor_id": self.constructor2.id,
            "start_year": 2021
        }
        response = self.client.post("/driverconstructorhistories", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Missing field: 'end_year'"})

    def test_create_driver_constructor_history_with_invalid_driver(self):
        """Test creating a driver constructor history with an invalid driver"""
        data = {
            "driver_id": 999,  # Invalid driver ID
            "constructor_id": self.constructor1.id,
            "start_year": 2021,
            "end_year": 2022
        }
        response = self.client.post("/driverconstructorhistories", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Driver not found"})

    def test_create_driver_constructor_history_with_invalid_constructor(self):
        """Test creating a driver constructor history with an invalid constructor"""
        data = {
            "driver_id": self.driver1.id,
            "constructor_id": 999,  # Invalid constructor ID
            "start_year": 2021,
            "end_year": 2022
        }
        response = self.client.post("/driverconstructorhistories", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Constructor not found"})

    def test_update_driver_constructor_history(self):
        """Test updating an existing driver constructor history"""
        data = {
            "driver_id": self.driver2.id,
            "constructor_id": self.constructor2.id,
            "start_year": 2016,
            "end_year": 2021
        }
        response = self.client.put(f"/driverconstructorhistories/{self.history1.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.history1.refresh_from_db()
        self.assertEqual(self.history1.start_year, 2016)

    def test_update_nonexistent_driver_constructor_history(self):
        """Test updating a driver constructor history that does not exist"""
        data = {
            "driver_id": self.driver1.id,
            "constructor_id": self.constructor1.id,
            "start_year": 2022,
            "end_year": 2023
        }
        response = self.client.put("/driverconstructorhistories/999", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "DriverConstructorHistory not found"})

    def test_delete_driver_constructor_history(self):
        """Test deleting a driver constructor history"""
        response = self.client.delete(f"/driverconstructorhistories/{self.history2.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DriverConstructorHistory.objects.filter(id=self.history2.id).exists())

    def test_delete_nonexistent_driver_constructor_history(self):
        """Test deleting a driver constructor history that does not exist"""
        response = self.client.delete("/driverconstructorhistories/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "DriverConstructorHistory not found"})
