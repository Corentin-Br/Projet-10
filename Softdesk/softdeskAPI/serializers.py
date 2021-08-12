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
        fields = ['email', 'first_name', 'last_name', 'password', 'issues_written_id', 'comments_written_id',
                  'contributors_id']

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class IssueSerializer(serializers.ModelSerializer):
    # comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())
    comments_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'priority', 'status', 'project_id', 'author_id', 'assignee_id',
                  'created_time', 'comments_id']


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user_id', 'project_id', 'permission', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    # contributors = serializers.PrimaryKeyRelatedField(many=True, queryset=Contributor.objects.all())
    # issues = serializers.PrimaryKeyRelatedField(many=True, queryset=Issue.objects.all())
    contributors_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    issues_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'contributors_id', 'issues_id']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['description', 'author_id', 'issue_id', 'created_time']
