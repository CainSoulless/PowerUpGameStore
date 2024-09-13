from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserRegistrationTest(TestCase):

    def test_register_new_user(self):
        # Datos simulados para el formulario de registro
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'full_name': 'Test users',
            'birthday': '1990-01-01',
            'password': '123456789A',
            'confirm_password': '123456789A'
        }

        # Simula un POST request a la vista de registro
        response = self.client.post(reverse('register'), data=user_data)

        # Verifica que el usuario fue creado correctamente
        self.assertEqual(response.status_code, 302)  # Verifica redirección después del registro
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Verifica que el usuario fue creado
