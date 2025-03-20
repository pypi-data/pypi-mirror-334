from django_anchor_modeling import constants
from django_anchor_modeling.exceptions import SentinelUserDoesNotExist


def get_knot_choice_value(instance: object):
    """
    Given any instance of a model, return the knot choice value
    format is

    APP__CLASS
    """
    app_label = instance._meta.app_label
    class_name = instance.__class__.__name__

    return f"{app_label}__{class_name}"


# utils.py or a similar module
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

SENTINEL_NULL_USER_ID = getattr(
    settings, "SENTINEL_NULL_USER_ID", constants.SENTINEL_NULL_USER_ID
)


def get_sentinel_user():
    sentinel_user, _ = User.objects.get_or_create(pk=SENTINEL_NULL_USER_ID)
    return sentinel_user


def get_sentinel_user_id():
    if User.objects.filter(pk=SENTINEL_NULL_USER_ID).exists():
        return SENTINEL_NULL_USER_ID
    else:
        raise SentinelUserDoesNotExist()


class DynamicAttributeDescriptor:
    def __init__(self, field_name):
        self.field_name = field_name

    def __get__(self, instance, owner):
        if instance is None:
            return self  # Access through class, not instance

        try:
            attribute = getattr(instance, self.field_name)
            return attribute.value
        except AttributeError:
            return None  # Return None if the attribute doesn't exist
