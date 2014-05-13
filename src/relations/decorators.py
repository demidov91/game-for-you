from relations.models import Team
from core.decorators import OwnerOnly

class team_owner_only(OwnerOnly):
    default_get_key = 'team_id'
    default_set_key = 'team'

    __name__ = 'team_owner_only'

    model_class = Team


