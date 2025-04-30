from allauth.account.forms import SignupForm
from django import forms
from apps.user_profile.models.user_profile import UserProfile
from apps.user_profile.models.squadron import Squadron
import pytz

class CustomSignupForm(SignupForm):
    squadron = forms.ModelChoiceField(
        queryset=Squadron.objects.all(),
        required=False,
        label="Squadron"
    )
    timezone = forms.ChoiceField(
        choices=[(tz, tz) for tz in pytz.common_timezones],
        initial='UTC',
        label="Timezone"
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        max_length=500,
        required=False,
        label="Bio"
    )

    def save(self, request):
        user = super().save(request)
        user_profile = user.profile
        user_profile.squadron = self.cleaned_data['squadron']
        user_profile.timezone = self.cleaned_data['timezone']
        user_profile.bio = self.cleaned_data['bio']
        user_profile.save()
        return user