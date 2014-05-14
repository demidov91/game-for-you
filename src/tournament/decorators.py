from tournament.models import Tournament, Competition
from core.decorators import OwnerOnly

class tournament_owner_only(OwnerOnly):
    default_get_key = 'tournament_id'
    default_set_key = 'tournament'

    __name__ = 'tournament_owner_only'

    model_class = Tournament


class competition_owner_only(OwnerOnly):
    default_get_key = 'competition_id'
    default_set_key = 'competition'

    __name__ = 'competition_owner_only'

    model_class = Competition

    def get_instance_owner(self, instance):
        return instance.owners