from django import template

register = template.Library()


@register.filter
def value_from_model(model, field):
    return getattr(model, field)


@register.filter
def split(string, sep):
    return string.split(sep)


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()

@register.filter(name='has_group_in_permissions') 
def has_group_in_permissions(user):
    g_list = ['Hardware', 'Foreign', 'Steel', 'General', 'Electrical', 'Timber and Stationary', 'Foundry', 'Tools', 'Oil']
    if user.userinform.section == "Main Store":        
        if user.userinform.store_group_name:
            store_group_name_list = user.userinform.store_group_name.split(",")
            for item in store_group_name_list:
                if item in g_list:
                    return True
    return False

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 

# @register.filter(name='has_group_in_permissions') 
# def has_group_in_permissions(user):
#     g_list = ['Foreign', 'General']
#     if user.userinform.section == "Main Store":
#         if user.userinform.section.store_group_name:
#             store_group_name_list = user.userinform.section.store_group_name.split(",")
#             for item in store_group_name_list:
#                 if item in g_list:
#                     return True
#     return False

@register.filter 
def get_class(instance):
    return instance.__class__.__name__

@register.filter(name='capitalize_under')
def capitalize_under(value):
    value = value.replace('_', ' ')
    return value.title()



@register.simple_tag
def get_count(value, arg, operator):
    try:
        if operator == '*':
            return round(value * arg)
        elif operator == '-':
            return round(value - arg)
        elif operator == '+':
            return round(value + arg)
        elif operator == '/':
            return round(value / arg)
    except:
        return 0
    

@register.filter(name='get_params')
def get_params(request):
    params = request.GET.copy()
    print(params.getlist("status"))
    if params.get("page"):
        params.pop("page")
    param_string = ""
    for param in params.keys():
        items = params.getlist(param)
        for item in items:
            param_string += "{}={}&".format(param, item)
    return param_string[:-1]


@register.filter(name='get_dic_item') 
def get_dic_item(dictionary, key):
    return dictionary.get(key)

@register.filter 
def get_positive(value):
    return value if value >= 0 else 0.0
