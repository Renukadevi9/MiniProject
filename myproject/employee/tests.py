from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Employee

class EmployeeSystemTests(TestCase):
    def setUp(self):
        # Create standard test user
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        
        # Create test employee
        self.employee = Employee.objects.create(
            emp_id='EMP001',
            first_name='Alice',
            last_name='Smith',
            email='alice@example.com',
            department='HR',
            designation='HR Manager'
        )

    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/login.html')

    def test_login_successful(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_failed(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/login.html')

    def test_dashboard_redirects_if_unauthenticated(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('dashboard'))

    def test_dashboard_renders_for_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/dashboard.html')
        self.assertContains(response, 'Alice Smith')
        self.assertContains(response, 'EMP001')

    def test_dashboard_search(self):
        self.client.login(username=self.username, password=self.password)
        # Search for active matches
        response = self.client.get(reverse('dashboard'), {'search': 'Alice'})
        self.assertContains(response, 'Alice Smith')
        
        # Search with non-matching string
        response = self.client.get(reverse('dashboard'), {'search': 'Bob'})
        self.assertNotContains(response, 'Alice Smith')
        self.assertContains(response, 'No Employees Found')

    def test_add_employee_view(self):
        self.client.login(username=self.username, password=self.password)
        # Verify page loads
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)
        
        # Add employee
        response = self.client.post(reverse('add'), {
            'emp_id': 'EMP002',
            'first_name': 'Bob',
            'last_name': 'Jones',
            'email': 'bob@example.com',
            'department': 'Engineering',
            'designation': 'Developer'
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(Employee.objects.filter(emp_id='EMP002').exists())

    def test_update_employee_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('update', kwargs={'pk': self.employee.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Update field
        response = self.client.post(reverse('update', kwargs={'pk': self.employee.pk}), {
            'emp_id': 'EMP001',
            'first_name': 'Alice',
            'last_name': 'Smith-Doe',
            'email': 'alice@example.com',
            'department': 'HR',
            'designation': 'Director'
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.last_name, 'Smith-Doe')
        self.assertEqual(self.employee.designation, 'Director')

    def test_delete_employee_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('delete', kwargs={'pk': self.employee.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Post confirmation to delete
        response = self.client.post(reverse('delete', kwargs={'pk': self.employee.pk}))
        self.assertRedirects(response, reverse('dashboard'))
        self.assertFalse(Employee.objects.filter(pk=self.employee.pk).exists())
