from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm


class RoomForm (ModelForm):
    class Meta :
        model =Room
        fields='__all__'
    
        exclude=['host','participants']
class UserForm (ModelForm):
    class Meta:
        model=User
        fields=['avater','name','username','email','bio']