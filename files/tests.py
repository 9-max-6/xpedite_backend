# from django.test import TestCase

# # Create your tests here.
# from rest_framework.test import APITestCase, APIClient
# from rest_framework import status
# from django.urls import reverse
# from django.contrib.auth.models import User
# from .models import File

# class FileViewSetTests(APITestCase):

#     def setUp(self):
#         # Create a user for authentication
#         self.user = User.objects.create_user(username="testuser", password="testpass")
#         self.client = APIClient()

#         # Log in the user for authenticated requests
#         self.client.login(username="testuser", password="testpass")

#         # Create some file instances to use in tests
#         self.file1 = File.objects.create(
#             file_name="example.pdf",
#             file_type="PDF",
#             file_content=b"Dummy content",
#             user=self.user,
#         )

#         self.file2 = File.objects.create(
#             file_name="example2.pdf",
#             file_type="PDF",
#             file_content=b"Another dummy content",
#             user=self.user,
#         )

#     def test_list_files(self):
#         """Test listing all files (GET /files/)"""
#         url = reverse('file-list')  # Use reverse to get the URL for the list action
#         response = self.client.get(url)

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Check if the response contains the correct number of files
#         self.assertEqual(len(response.data), 2)

#     def test_retrieve_file(self):
#         """Test retrieving a single file (GET /files/{id}/)"""
#         url = reverse('file-detail', args=[self.file1.id])  # Use reverse to get the detail URL
#         response = self.client.get(url)

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Check if the returned file is the correct one
#         self.assertEqual(response.data['file_name'], self.file1.file_name)

#     def test_create_file(self):
#         """Test creating a new file (POST /files/)"""
#         url = reverse('file-list')
#         data = {
#             "file_name": "new_file.pdf",
#             "file_type": "PDF",
#             "file_content": b"New file content",
#             "user": self.user.id,
#         }
#         response = self.client.post(url, data, format='json')

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # Check if the file was created
#         self.assertEqual(response.data['file_name'], "new_file.pdf")

#     def test_unauthorized_access(self):
#         """Test unauthorized access to the file detail endpoint"""
#         self.client.logout()  # Log out the authenticated user

#         url = reverse('file-detail', args=[self.file1.id])
#         response = self.client.get(url)

#         # Check that unauthorized users receive a 401 Unauthorized status
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_update_file(self):
#         """Test updating a file (PUT /files/{id}/)"""
#         url = reverse('file-detail', args=[self.file1.id])
#         data = {
#             "file_name": "updated_example.pdf",
#             "file_type": "PDF",
#             "file_content": b"Updated content",
#             "user": self.user.id,
#         }
#         response = self.client.put(url, data, format='json')

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Check if the file was updated
#         self.file1.refresh_from_db()  # Refresh the file instance from the database
#         self.assertEqual(self.file1.file_name, "updated_example.pdf")

#     def test_delete_file(self):
#         """Test deleting a file (DELETE /files/{id}/)"""
#         url = reverse('file-detail', args=[self.file1.id])
#         response = self.client.delete(url)

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#         # Check if the file was deleted
#         self.assertFalse(File.objects.filter(id=self.file1.id).exists())
