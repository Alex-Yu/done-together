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
