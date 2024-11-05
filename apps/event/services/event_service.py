from django.core.exceptions import ObjectDoesNotExist
from apps.event.models.event import Event

class EventService:
    @staticmethod
    def get_event_by_id(event_id: int) -> Event:
        """
        Retrieves an Event instance by its ID, ensuring the event is active and enabled.

        Parameters:
        - event_id (int): The ID of the event to retrieve.

        Returns:
        Event: The Event instance matching the given ID, if it exists, is active, and enabled.
        """
        try:
            return Event.objects.select_related('event_type', 'semester').get(id=event_id, is_active=True, semester__status='active')
        except Event.DoesNotExist:
            raise ObjectDoesNotExist(f"Evento de ID: {event_id} no existe, está inactivo, o no tiene el estado Habilitado")
