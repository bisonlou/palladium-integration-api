from api.validators.validation_helper import ValidationHelpers


validate = ValidationHelpers()


def validate_user(data):
    """
    Function to check if user keys and key data is present
    Also checks if data is in required format
    Returns True on success otherwise False
    """
    keys = ["password", "first_name", "last_name", "email", "middle_name"]
    errors = validate.key_exists(data, keys)
    if errors:
        return errors

    errors = validate.is_of_type_string(data, keys)
    if errors:
        return errors

    errors = validate.key_value_not_empty(data, keys)
    if errors:
        return errors

    errors = validate.is_proper_email(data["email"])
    if errors:
        return errors

    errors = validate.is_proper_phone_number(data["phone_number"])
    if errors:
        return errors

    keys = ["first_name", "last_name", "middle_name"]
    errors = validate.is_proper_name(data, keys)
    if errors:
        return errors

    errors = validate.is_poper_password(data["password"])
    if errors:
        return errors
