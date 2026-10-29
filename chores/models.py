from django.db import models


class Definition(models.Model):
    household = models.ForeignKey("households.Household", on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    child = models.ForeignKey("households.Child", on_delete=models.PROTECT)
    due_date = models.DateField()


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

    class Meta:
        constraints = [
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
