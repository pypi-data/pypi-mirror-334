import unittest

from digitalai.release.integration.release_api_client import ReleaseAPIClient


class TestReleaseAPIClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the API client before running tests."""
        cls.client = ReleaseAPIClient("http://localhost:5516", "admin", "admin")
        cls.global_variable_id = None  # Store ID at the class level

    @classmethod
    def tearDownClass(cls):
        """Close the API client session after all tests."""
        cls.client.close()

    def test_01_create_global_variable(self):
        """Test creating a new global variable."""
        global_variable = {
            "id": None,
            "key": "global.testVar",
            "type": "xlrelease.StringVariable",
            "requiresValue": "false",
            "showOnReleaseStart": "false",
            "value": "test value"
        }
        response = self.client.post("/api/v1/config/Configuration/variables/global", json=global_variable)
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")

        # Store ID in class attribute
        TestReleaseAPIClient.global_variable_id = response.json().get("id")
        print(f"Created global variable ID: {TestReleaseAPIClient.global_variable_id}")

    def test_02_update_global_variable(self):
        """Test updating an existing global variable."""
        if not TestReleaseAPIClient.global_variable_id:
            self.skipTest("Global variable ID is not set. Run test_01_create_global_variable first.")

        updated_variable = {
            "id": TestReleaseAPIClient.global_variable_id,
            "key": "global.testVar",
            "type": "xlrelease.StringVariable",
            "requiresValue": "false",
            "showOnReleaseStart": "false",
            "value": "updated test value"
        }

        response = self.client.put(f"/api/v1/config/{TestReleaseAPIClient.global_variable_id}", json=updated_variable)
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")
        print("Global variable updated successfully.")

    def test_03_get_global_variable(self):
        """Test retrieving the global variable."""
        if not TestReleaseAPIClient.global_variable_id:
            self.skipTest("Global variable ID is not set. Run test_01_create_global_variable first.")

        response = self.client.get(f"/api/v1/config/{TestReleaseAPIClient.global_variable_id}")
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")
        print(f"Retrieved global variable: {response.json()}")

    def test_04_delete_global_variable(self):
        """Test deleting the global variable."""
        if not TestReleaseAPIClient.global_variable_id:
            self.skipTest("Global variable ID is not set. Run test_01_create_global_variable first.")

        response = self.client.delete(f"/api/v1/config/{TestReleaseAPIClient.global_variable_id}")
        self.assertEqual(response.status_code, 204, f"Unexpected status code: {response.status_code}")
        print("Global variable deleted successfully.")

if __name__ == "__main__":
    unittest.main()
