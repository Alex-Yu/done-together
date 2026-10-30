from django.conf import settings
from django.db import models


class Definition(models.Model):
    household = models.ForeignKey("households.Household", on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    child = models.ForeignKey("households.Child", on_delete=models.PROTECT)
    due_date = models.DateField(null=True)
    schedule = models.CharField(
        max_length=12,
        default="once",
        choices=[
            ("once", "One-off"),
            ("daily", "Daily"),
            ("weekdays", "Selected weekdays"),
        ],
    )
    weekdays = models.JSONField(default=list)
    eligible_from = models.DateField(null=True)
    version = models.PositiveBigIntegerField(default=1)


class Occurrence(models.Model):
    definition = models.ForeignKey(Definition, on_delete=models.SET_NULL, null=True)
    household = models.ForeignKey("households.Household", on_delete=models.PROTECT)
    child = models.ForeignKey("households.Child", on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    state = models.CharField(
        max_length=24,
        default="to_do",
        choices=[
            ("to_do", "To do"),
            ("awaiting_approval", "Awaiting approval"),
            ("completed", "Completed"),
        ],
    )
    version = models.PositiveBigIntegerField(default=1)
    completed_at = models.DateTimeField(null=True)
    submitted_at = models.DateTimeField(null=True)
    submitted_timezone = models.CharField(max_length=100, blank=True)
    submitted_late = models.BooleanField(null=True)
    return_note = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["definition"],
                condition=~models.Q(state="completed"),
                name="one_unfinished_per_definition",
            ),
            models.UniqueConstraint(
                fields=["definition", "due_date"], name="unique_definition_due_date"
            ),
            models.CheckConstraint(
                condition=models.Q(
                    state__in=["to_do", "awaiting_approval", "completed"]
                ),
                name="valid_occurrence_state",
            ),
        ]


class Approval(models.Model):
    occurrence = models.OneToOneField(Occurrence, on_delete=models.PROTECT)
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    approved_at = models.DateTimeField()
    # Each unique durable approval is exactly one star; no mutable counter.
