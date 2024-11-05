from typing import List
from django.db import transaction

from apps.account.models import User
from apps.event.services.event_service import EventService
from apps.event.models import Event
from apps.attendance.models import Attendance

class AttendanceService:
    @staticmethod
    def get_attendee_ids_for_event(event: Event) -> List[int]:
        """
        Retrieves a list of user IDs who have already registered as attendees for a given event.

        Parameters:
        - event (Event): The event instance to query for attendee IDs.

        Returns:
        List[int]: A list of user IDs who are attendees of the specified event.
        """
        return Attendance.objects.filter(event=event).values_list('attendee__id', flat=True)

    @staticmethod
    def register_attendees(attendees: List[User], event_id: int) -> List[Attendance]:
        """
        Registers each user in the provided list as an attendee for the specified event if they have not already been registered.
        Updates the user's points based on the event's point value. Returns an empty list if the event does not exist.

        Parameters:
        - attendees (List[User]): Users to register as attendees.
        - event_id (int): ID of the event for registration.

        Returns:
        List[Attendance]: Newly created Attendance records for newly registered users.
        """
        try:
            event = EventService.get_event_by_id(event_id)
        except Event.DoesNotExist:
            return []

        attendee_ids = set(AttendanceService.get_attendee_ids_for_event(event))

        new_attendances, users_to_update = [], []

        for user in attendees:
            if user.id not in attendee_ids:
                new_attendances.append(Attendance(attendee=user, event=event, points=event.event_type.points))
                user.points += event.event_type.points
                users_to_update.append(user)

        if new_attendances:
            with transaction.atomic():
                Attendance.objects.bulk_create(new_attendances)
                User.objects.bulk_update(users_to_update, ['points'])

        return new_attendances
