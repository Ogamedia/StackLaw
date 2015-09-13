from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from models import ReviewRequest

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder':'company@email.com'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    company_name = forms.CharField(label=('Company Name'), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'company_name', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.company_name = self.cleaned_data['company_name']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        
        if commit:
            user.is_active = False
            user.save()
    
        return user
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('duplicate email')


class ReviewRequestForm(forms.ModelForm):
        
    class Meta:
        model = ReviewRequest
        exclude = ()
        # fields = ('description', 'body')
        # fields = '__all__'
        
        