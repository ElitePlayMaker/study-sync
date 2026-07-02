"""Class management service — CRUD and slot creation."""

from datetime import datetime

from study_sync.models import class_session as class_model


def create_class_with_slot(title, description, lecturer_id, category, location,
                           duration_minutes, start_time, end_time, max_capacity):
    """Create a class and its first time slot in one flow."""
    if start_time >= end_time:
        return False, "End time must be after start time."

    class_id = class_model.create_class(
        title, description, lecturer_id, category, location, duration_minutes
    )
    class_model.create_slot(class_id, start_time, end_time, max_capacity)
    return True, class_id


def add_slot(class_id, start_time, end_time, max_capacity, lecturer_id=None):
    """Add a time slot to an existing class."""
    class_item = class_model.get_class(class_id)
    if not class_item:
        return False, "Class not found."
    if lecturer_id and class_item["lecturer_id"] != lecturer_id:
        return False, "You can only manage your own classes."
    if start_time >= end_time:
        return False, "End time must be after start time."

    class_model.create_slot(class_id, start_time, end_time, max_capacity)
    return True, "Time slot added."


def search_classes(search=None, category=None):
    """Search and filter available classes."""
    return class_model.list_classes(search=search, category=category)


def calendar_data(start=None, end=None, lecturer_id=None):
    """Format events for calendar UI."""
    events = class_model.calendar_events(start, end, lecturer_id)
    formatted = []
    for event in events:
        remaining = event["max_capacity"] - event["booked_count"]
        formatted.append({
            "id": event["slot_id"],
            "title": event["title"],
            "start": event["start_time"].isoformat(),
            "end": event["end_time"].isoformat(),
            "extendedProps": {
                "class_id": event["class_id"],
                "lecturer": event["lecturer_name"],
                "category": event["category"],
                "location": event["location"],
                "spots_left": max(remaining, 0),
                "status": event["status"],
            },
        })
    return formatted
