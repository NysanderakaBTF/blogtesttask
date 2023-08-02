from django import forms
from users.models import User

class UserForm(forms.ModelForm):
    """
    A Django form used for user signup/registration.

    This form is based on the User model and provides fields for the user's name, email, and password.
    The password field is rendered as a password input for security.

    Usage:
    - When rendering a signup form in a Django template, create an instance of this form and pass it as context.
    - To validate and process the user's input, instantiate this form with the request.POST data in the view.

    """

    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
