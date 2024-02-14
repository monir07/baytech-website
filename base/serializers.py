from django.contrib.auth import get_user_model
from rest_framework.serializers import SerializerMethodField, ModelSerializer
from base.models import BaseModel

User = get_user_model()



class UserLiteSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class ReadWriteSerializerMethodField(SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs["source"] = "*"
        self.read_only = False
        super(SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {f'{self.field_name}_id': data}


class BaseModelSerializer(ModelSerializer):
    created_by = ReadWriteSerializerMethodField()
    updated_by = ReadWriteSerializerMethodField(required=False)

    def get_created_by(self, obj):
        return UserLiteSerializer(instance=obj.created_by).data

    def get_updated_by(self, obj):
        if not obj.updated_by:
            return None
        return UserLiteSerializer(instance=obj.updated_by).data

    class Meta:
        model = BaseModel
        abstract = True
