from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone as django_timezone


class Household(models.Model):
    timezone = models.CharField(max_length=64)
    created_at = models.DateTimeField(default=django_timezone.now)
    revision = models.PositiveBigIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.pk:
            original = type(self).objects.only("timezone").get(pk=self.pk)
            if original.timezone != self.timezone:
                raise ValidationError("The household timezone cannot be changed.")
        return super().save(*args, **kwargs)


class Membership(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="household_membership",
    )
    household = models.ForeignKey(
        Household, on_delete=models.PROTECT, related_name="memberships"
    )
    slot = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(default=django_timezone.now)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(slot__in=[1, 2]), name="membership_slot_one_or_two"
            ),
            models.UniqueConstraint(
                fields=["household", "slot"], name="unique_household_parent_slot"
            ),
        ]


class Invitation(models.Model):
    household = models.ForeignKey(
        Household, on_delete=models.PROTECT, related_name="invitations"
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    email = models.EmailField()
    token_hash = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(default=django_timezone.now)
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(null=True, blank=True)
    superseded_at = models.DateTimeField(null=True, blank=True)

    @property
    def available(self):
        return (
            self.consumed_at is None
            and self.superseded_at is None
            and django_timezone.now() < self.expires_at
        )


class ParentCredential(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    pin_hash = models.CharField(max_length=256, default="")
    version = models.PositiveBigIntegerField(default=0)


class Child(models.Model):
    household = models.ForeignKey(
        Household, on_delete=models.PROTECT, related_name="children"
    )
    name = models.TextField()
    pin_hash = models.CharField(max_length=256)


class BoardAuthority(models.Model):
    session_hash = models.CharField(max_length=64, unique=True)
    household = models.ForeignKey(Household, on_delete=models.PROTECT)
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    credential_version = models.PositiveBigIntegerField()
    last_activity = models.DateTimeField()
