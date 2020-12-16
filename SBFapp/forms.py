from django import forms
from django.contrib.auth.models import User
from .models import  *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('major', 'year', 'max_group_size')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_title','post_content','post_type')
        widgets={'post_type':forms.RadioSelect()}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user','text')

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('event_name', 'event_description', 'event_date', 'event_start_time', 'event_end_time', 'days')
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'event_start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'event_end_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }
    days = forms.ModelMultipleChoiceField(queryset=Recurrence.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('group_name','group_descr', 'private')
