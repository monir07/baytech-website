from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)ss')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT,  related_name='updated_%(class)ss', 
                        null=True, blank=True)

    class Meta:
        abstract = True
        app_label = 'base'


class CustomQuerySetManager(models.QuerySet):
    def filter_by_query(self,query_dict):
        return self.filter(**query_dict)

class EconomicYearChoices(models.TextChoices):
    FIRST = '2020-2021', '2020-2021'
    SECOND = '2021-2022', '2021-2022'
    THIRD = '2022-2023', '2022-2023'
    FOURTH = '2023-2024', '2023-2024'
    FIFTH = '2024-2025', '2024-2025'
    SIXTH = '2025-2026', '2025-2026'
    SEVENTH = '2026-2027', '2026-2027'
    EIGHTH = '2027-2028', '2027-2028'
    NINTH = '2028-2029', '2028-2029'
    TENTH = '2029-2030', '2029-2030'

class UserTypeChoices(models.TextChoices):
    GENERAL = 'general', 'general'
    WOMEN = 'women', 'women'
    AGED_PERSON = 'aged_person', 'aged_person'
    WITH_DISABILITY = 'with_disability', 'with_disability'
    WITH_DISABLE_CHILD = 'with_disable_child', 'with_disable_child'
    FREEDOM_FIGHTER = 'freedom_fighter', 'freedom_fighter'