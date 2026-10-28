from zoneinfo import available_timezones

from django import forms


class HouseholdForm(forms.Form):
    timezone = forms.ChoiceField(
        label="Scheduling timezone",
        choices=[(zone, zone) for zone in sorted(available_timezones())],
        initial="UTC",
    )


class InvitationForm(forms.Form):
    email = forms.EmailField(
        label="Second parent’s email",
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
