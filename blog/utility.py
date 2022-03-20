from django.db.models.base import ModelStateFieldsCacheDescriptor


class Visability_State:
    pending = 'pending'
    under_review = 'under review'
    approved = 'approved'
    hidden = 'hidden'