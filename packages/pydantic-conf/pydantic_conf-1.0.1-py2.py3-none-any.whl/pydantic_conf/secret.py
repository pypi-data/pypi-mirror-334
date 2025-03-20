from pathlib import Path
from typing import Annotated, Any

from pydantic import (
    SecretBytes,
    SecretStr,
    WrapValidator,
    ValidatorFunctionWrapHandler,
    ValidationInfo,
)


def validate_secret(
    value: Any,
    handler: ValidatorFunctionWrapHandler,
    info: ValidationInfo,
) -> Path:
    """Validate a secret path."""

    if value is None:
        value = info.field_name

    if not isinstance(value, str):
        raise ValueError("Secret must be a string")

    if not value.startswith("/run/secrets/"):
        value = f"/run/secrets/{value}"

    path = Path(value)

    if not path.exists():
        raise ValueError(f"Secret file {path} not found")

    if "SecretBytes" in str(handler):
        return handler(path.read_bytes())

    return handler(path.read_text())


ContainerSecretStr = Annotated[
    SecretStr,
    WrapValidator(validate_secret),
]

ContainerSecretBytes = Annotated[
    SecretBytes,
    WrapValidator(validate_secret),
]
