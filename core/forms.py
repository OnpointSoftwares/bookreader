from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

class DateInput(forms.DateInput):
    input_type = 'date'

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
        # Add placeholders and labels
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        self.fields['email'].widget.attrs['placeholder'] = 'Your email address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Create a password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        
        # Add help text
        self.fields['email'].required = True
        self.fields['email'].help_text = 'Required. Enter a valid email address.'


class ProfileForm(forms.ModelForm):
    """Form for updating user profile information."""
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Add placeholders and help text
        self.fields['bio'].widget.attrs['placeholder'] = 'Tell us about yourself...'
        # Custom labels
        self.fields['profile_picture'].label = 'Profile Picture'
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['phone_number'].label = 'Phone Number'
        self.fields['facebook_profile'].label = 'Facebook Profile URL'
        self.fields['twitter_profile'].label = 'Twitter Profile URL'
        self.fields['instagram_profile'].label = 'Instagram Profile URL'
        self.fields['email_notifications'].label = 'Receive email notifications'


class UserForm(forms.ModelForm):
    """
    Form for updating basic user information (first name, last name, email).
    This is typically used alongside ProfileForm.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Make email required
        self.fields['email'].required = True
        self.fields['email'].help_text = 'Required. Enter a valid email address.'
        
        # Add placeholders
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email address'