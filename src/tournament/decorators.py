from tournament.models import Tournament, Competition, Participation
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

class can_modify_participation(OwnerOnly):
    default_get_key = 'participation_id'
    default_set_key = 'participation'

    __name__ = 'can_modify_participation'

    model_class = Participation

    def get_instance_owner(self, instance):
        return instance.competition.owners