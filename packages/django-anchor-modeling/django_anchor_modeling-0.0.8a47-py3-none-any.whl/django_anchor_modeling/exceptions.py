from django.core.exceptions import (
    ImproperlyConfigured,
    ObjectDoesNotExist,
    PermissionDenied,
)
from icontract import ViolationError


class UndeletableModelError(PermissionDenied):
    pass


class SentinelDoesNotExist(ObjectDoesNotExist):
    """
    Base exception for when an expected sentinel record is missing.
    """

    pass


from django.conf import settings

from django_anchor_modeling import constants

# Assuming settings.SENTINEL_NULL_USER_ID is set, or fallback to a default value from constants
SENTINEL_NULL_USER_ID = getattr(
    settings, "SENTINEL_NULL_USER_ID", constants.SENTINEL_NULL_USER_ID
)


class SentinelUserDoesNotExist(SentinelDoesNotExist):
    """
    Raised when the sentinel user is missing. Includes the sentinel user ID
    in the error message and instructions on how to create it.
    """

    def __init__(self, *args, **kwargs):
        message = (
            f"Sentinel user does not exist. Expected sentinel user ID is '{SENTINEL_NULL_USER_ID}'. "
            "Create it by running:\n\n"
            "from django.contrib.auth import get_user_model\n"
            "UserModel = get_user_model()\n"
            f"UserModel.objects.get_or_create(pk={SENTINEL_NULL_USER_ID})\n"
        )
        super().__init__(message, *args, **kwargs)


class CustomTransactionExceptionWithCode(ImproperlyConfigured):
    code = None

    def __init__(self, message, *args, **kwargs):
        if self.code is not None:
            message = f"[{self.code}] {message}"
        super().__init__(message, *args, **kwargs)


class ActiveModelClassMustBeTransactionBackedError(CustomTransactionExceptionWithCode):
    code = "TE001"


class CannotReuseExistingTransactionError(CustomTransactionExceptionWithCode):
    code = "TE002"


class MissingTransactionInModelError(CustomTransactionExceptionWithCode):
    code = "TE003"


class SentinelTransactionCannotBeUsedError(CustomTransactionExceptionWithCode):
    code = "TE004"


class SentinelUserMissingInDatabaseError(CustomTransactionExceptionWithCode):
    code = "TE004"


class CustomTransactionBackedExceptionWithCode(PermissionDenied):
    code = None

    def __init__(self, message, *args, **kwargs):
        if self.code is not None:
            message = f"[{self.code}] {message}"
        super().__init__(message, *args, **kwargs)


class NotAnAnchorError(CustomTransactionBackedExceptionWithCode):
    code = "TBE001"


# Custom exception class for a specific type of contract violation
class TransactionTypeError(ViolationError):
    """
    use this exception to indicate that a transaction is not Transation type
    and inside an icontract require clause

    Example:
    >>> @require(
    >>>  lambda transaction=None: transaction is None or isinstance(transaction, Transaction),
    >>>  description="'transaction' in kwargs must be an instance of 'Transaction'.",
    >>>  error=TransactionTypeError  # Use your custom exception here
    >>> )
    >>> def save_project_fas(
    >>>   *,
    >>>   project: Union[Project, int],
    >>>   fas: Union[Fas, int],
    >>>   transaction: Union[Transaction, None] = None,
    >>>   **kwargs
    >>> ):
    """

    pass
