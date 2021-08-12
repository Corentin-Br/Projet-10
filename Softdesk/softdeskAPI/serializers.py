from rest_framework import serializers
from .models import MyUser, Issue, Project, Contributor, Comment


class MyUserSerializer(serializers.ModelSerializer):
    # issues_written = serializers.PrimaryKeyRelatedField(many=True, queryset=Issue.objects.all())
    # comments_written = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())
    # contributors = serializers.PrimaryKeyRelatedField(many=True, queryset=Contributor.objects.all())

    issues_written_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments_written_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    contributors_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'password', 'issues_written', 'comments_written',
                  'contributors']

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class IssueSerializer(serializers.ModelSerializer):
    # comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())
    comments_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'priority', 'status', 'project', 'author', 'assignee',
                  'created_time', 'comments']


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user_id', 'project_id', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    # contributors = serializers.PrimaryKeyRelatedField(many=True, queryset=Contributor.objects.all())
    # issues = serializers.PrimaryKeyRelatedField(many=True, queryset=Issue.objects.all())
    contributors_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    issues_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'contributors', 'issues']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['description', 'author', 'issue', 'created_time']
