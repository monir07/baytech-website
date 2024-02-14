from django.db.models import Q
from django.conf import settings
from base.helpers.func import find_common_groups

def query_filter(queryset, user, history, in_list=False):
    filter_dict = {
        "DGM_CNP": Q(tendercstsign__dgm_cnp_sign__isnull=False if history else True),
        "OIC_LIST": (Q(tendercstsign__dgm_cnp_sign__isnull=False, tendercstsign__related_oic_sign__isnull=False if history else True)),
       }   
        
    user_groups = [group.name for group in user.groups.all()]
    groups_name = ["DGM_CNP", "OIC_COMMERCIAL_L", "OIC_COMMERCIAL_F", "OIC_LIST", "RELATED_DGM", "GM_PRODUCTION", "GM_FINANCE", "GM_ADMIN", "MD"]
    user_access_groups = find_common_groups(user_groups, groups_name)
    
    if in_list:
        if user_access_groups and len(user_access_groups) > 0:
            query = Q()
            for group in user_access_groups:
                query = query | filter_dict.get(group)
            queryset = queryset.filter(query)
        else:
            queryset = queryset.none()
    else:
        queryset = queryset.none()
    return queryset