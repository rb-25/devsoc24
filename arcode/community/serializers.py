from rest_framework import serializers
from community.models import Code, Comment, Like

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Code
        fields=['id','title','code','language','date','user']
        extra_kwargs = {
            'user' : {'read_only': True}
        }
    
    def create(self,validated_data):
        user=self.context['request'].user
        code=Code.objects.create(user=user,**validated_data)
        return code

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['id','code','user','content','date']
        extra_kwargs = {
            'user' : {'read_only': True}
        }
    
    def create(self,validated_data):
        user=self.context['request'].user
        comment=Comment.objects.create(user=user,**validated_data)
        return comment

class CodeListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model=Code
        exclude=['code']

class CodeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Code
        fields='__all__'
        
class LeaderboardSerializer(serializers.Serializer):
    user = serializers.StringRelatedField()
    wins = serializers.IntegerField()