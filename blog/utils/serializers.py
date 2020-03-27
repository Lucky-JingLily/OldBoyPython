from rest_framework import serializers

from blog import models


# class UserInfoSerializer(serializers.Serializer):
#     userType = serializers.IntegerField()
#     username = serializers.CharField()
#     password = serializers.CharField()
#     # gp = serializers.CharField(source="group.user_group_name")

class UserInfoSerializer(serializers.ModelSerializer):
    group = serializers.HyperlinkedIdentityField(view_name='gp', lookup_field='userGroup_id', lookup_url_kwarg='group')
    class Meta:
        model = models.UserInfo
        # fields = "__all__"
        fields = ['username', 'id', 'password', 'rls', "group"]

    '''
    下面是自定义序列化字段，序列化的属性值由方法来提供，
       方法的名字：固定为 get_属性名，
       方法的参数：self为序列化对象，row为序列化的model对象
       注意 : 建议自定义序列化字段名不要与model已有的属性名重名,否则会覆盖model已有字段的声明
       注意 : 自定义序列化字段要用SerializerMethodField()作为字段类型
    '''
    rls = serializers.SerializerMethodField()

    def get_rls(self, row):
        role_obj_list = row.roles.all()
        ret = []
        for item in role_obj_list:
            ret.append({'id': item.id, 'title': item.title})
        return ret
