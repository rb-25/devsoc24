from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

from users.models import User
from community.models import Code, Comment, Like, Resource, Friend
from community.serializers import CodeSerializer, CommentSerializer,CodeDetailSerializer,CodeListSerializer,LeaderboardSerializer

#Friend views
class RequestFriend(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        user=request.user
        friend=get_object_or_404(get_user_model(), pk=pk)
        if user==friend:
            return Response({"detail":"You can't send friend request to yourself"}, status=HTTPStatus.BAD_REQUEST)
        if user.friends.filter(friend=friend).exists():
            return Response({"detail":"You are already friends"}, status=HTTPStatus.BAD_REQUEST)
        user.friends.create(friend=friend)
        return Response({"detail":"Friend request sent"}, status=HTTPStatus.OK)

class AcceptFriend(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        user=request.user
        friend=get_object_or_404(get_user_model(), pk=pk)
        if not user.friends.filter(friend=friend).exists():
            return Response({"detail":"You are not friends"}, status=HTTPStatus.BAD_REQUEST)
        user.friends.get(friend=friend).delete()
        user.friends.create(friend=friend)
        return Response({"detail":"Friend request accepted"}, status=HTTPStatus.OK)    

class CodeView(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.action == "list":
            return  CodeListSerializer
        return CodeDetailSerializer
    

#Code Views 
class UserCodeView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Code.objects.all()
    serializer_class=CodeSerializer
    def create(self,request):
        request.data['user']=request.user.id
        return super().create(request)
    def update(self,request,pk):
        code=Code.objects.get(pk=pk)
        if code.user != request.user:
            raise PermissionDenied("You can't update this code")
        return super().update(request,pk)
    def destroy(self,request,pk):
        code=Code.objects.get(pk=pk)
        if code.user != request.user:
            raise PermissionDenied("You can't delete this code")
        return super().destroy(request,pk)
    

#Comment Views
class CommentView(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        return CodeDetailSerializer

class UserCommentView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    def create(self,request):
        request.data['user']=request.user.id
        return super().create(request)
    def update(self,request,pk):
        comment=Comment.objects.get(pk=pk)
        if comment.user != request.user:
            raise PermissionDenied("You can't update this comment")
        return super().update(request,pk)
    def destroy(self,request,pk):
        comment=Comment.objects.get(pk=pk)
        if comment.user != request.user:
            raise PermissionDenied("You can't delete this comment")
        return super().destroy(request,pk)

#Like views
class LikeView(APIView): 
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        user=request.user
        code=get_object_or_404(Code, pk=pk)
        like=Like.objects.filter(user=user, code=code)
        if like.exists():
            like.delete()
            return Response({"detail":"Unliked"}, status=HTTPStatus.OK)
        else:
            Like.objects.create(user=user, code=code)
            return Response({"detail":"Liked"}, status=HTTPStatus.OK)
    def get(self,request):
        serializer = CodeSerializer(Code.objects.all(), many=True)
        return Response(serializer.data)

#Leaderboard views
class LeaderboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        users=User.objects.all.order_by('-wins')
        serializer= LeaderboardSerializer(users,many=True)
        return Response(serializer.data)
        