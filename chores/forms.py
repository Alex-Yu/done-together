from django import forms


class ChoreForm(forms.Form):
    title = forms.CharField(max_length=200, label="Chore title")
    child = forms.ModelChoiceField(
        queryset=None, label="Assigned child", empty_label="Choose a child"
    )
    due_date = forms.DateField(
        label="Due date",
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    version = forms.IntegerField(min_value=1, widget=forms.HiddenInput, required=False)

    def __init__(self, household, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["child"].queryset = household.children.order_by("pk")
        self.fields["child"].label_from_instance = lambda child: child.name


class RecurringForm(ChoreForm):
    due_date = None
    schedule = forms.ChoiceField(
        choices=[("daily", "Daily"), ("weekdays", "Selected weekdays")]
    )
    weekdays = forms.TypedMultipleChoiceField(
        choices=list(
            enumerate(
                [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ]
            )
        ),
        coerce=int,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def clean(self):
        data = super().clean()
        if data.get("schedule") == "weekdays" and not data.get("weekdays"):
            self.add_error("weekdays", "Choose at least one weekday.")
        if data.get("schedule") == "daily":
            data["weekdays"] = []
        return data


class SubmissionForm(forms.Form):
    version = forms.IntegerField(min_value=1, widget=forms.HiddenInput)
    pin = forms.CharField(
        label="Assigned child’s PIN",
        strip=False,
        required=False,
        widget=forms.PasswordInput(
            attrs={"inputmode": "numeric", "autocomplete": "off"}
        ),
    )
    browser_timezone = forms.CharField(
        label="Your computer timezone",
        max_length=100,
        help_text="Detected from this computer. If unavailable, choose its IANA timezone (for example Europe/Warsaw).",
    )

    def clean_browser_timezone(self):
        from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

        value = self.cleaned_data["browser_timezone"]
        try:
            ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError):
            raise forms.ValidationError("Enter a valid computer timezone.") from None
        return value


class ReviewForm(forms.Form):
    version = forms.IntegerField(min_value=1, widget=forms.HiddenInput)
    action = forms.ChoiceField(
        choices=[("approve", "Approve — award one star"), ("return", "Return to child")]
    )
    note = forms.CharField(
        label="Return explanation",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        max_length=4000,
    )

    def clean(self):
        data = super().clean()
        if data.get("action") == "return" and not data.get("note"):
            self.add_error(
                "note", "Explain what needs doing before returning this chore."
            )
        return data
