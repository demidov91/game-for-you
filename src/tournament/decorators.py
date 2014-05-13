from tournament.models import Tournament
from core.decorators import OwnerOnly

class tournament_owner_only(OwnerOnly):
    default_get_key = 'tournament_id'
    default_set_key = 'tournament'

    __name__ = 'tournament_owner_only'

    model_class = Tournament