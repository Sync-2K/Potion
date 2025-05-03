from app.state.globals import input_handler


def set_all_attributes(value):
    """Set all attributes to a specific value."""

    attribute_inputs = input_handler.get_inputs("Attributes")
    for select in attribute_inputs.values():
        select.value = value


def set_all_badges(value):
    """Set all badges to a specific value."""

    badge_inputs = input_handler.get_inputs("Badges")
    for select in badge_inputs.values():
        select.value = value


def set_all_tendencies(value):
    """Set all tendencies to a specific value."""

    tendency_inputs = input_handler.get_inputs("Tendencies")
    for select in tendency_inputs.values():
        select.value = value


def set_all_hotzones(value):
    """Set all hotzones to a specific value."""

    hotzone_inputs = input_handler.get_inputs("Hotzones")
    for select in hotzone_inputs.values():
        select.value = value


def adjust_all_attributes(amount):
    """Adjust all attributes by a specific amount."""

    attribute_inputs = input_handler.get_inputs("Attributes")
    for select in attribute_inputs.values():
        current = select.value or 25
        new_value = max(25, min(110, current + amount))
        select.value = new_value


def adjust_all_badges(amount):
    """Adjust all badges by a specific amount."""

    badge_inputs = input_handler.get_inputs("Badges")
    for select in badge_inputs.values():
        current = select.value or 0
        new_value = max(0, min(5, current + amount))
        select.value = new_value


def adjust_all_tendencies(amount):
    """Adjust all tendencies by a specific amount."""

    tendency_inputs = input_handler.get_inputs("Tendencies")
    for select in tendency_inputs.values():
        current = select.value or 0
        new_value = max(0, min(100, current + amount))
        select.value = new_value


def adjust_all_hotzones(amount):
    """Adjust all hotzones by a specific amount."""

    hotzone_inputs = input_handler.get_inputs("Hotzones")
    for select in hotzone_inputs.values():
        current = select.value or 0
        new_value = max(0, min(2, current + amount))
        select.value = new_value
