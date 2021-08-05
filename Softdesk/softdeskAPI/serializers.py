from rest_framework import serializers
from .models import MyUser, Issue, Project, Contributor, Comment


class MyUserSerializer(serializers.ModelSerializer):
    # issues_written = serializers.PrimaryKeyRelatedField(many=True, queryset=Issue.objects.all())
    # comments_written = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())
    # contributors = serializers.PrimaryKeyRelatedField(many=True, queryset=Contributor.objects.all())
    issues_written = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments_written = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    contributors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    password1 = serializers.CharField(label='Password', max_length=50, write_only=True)
    password2 = serializers.CharField(label='Password confirmation', max_length=50, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'issues_written', 'comments_written', 'contributors']

    def validate(self, data):
        if data['password1'] == data['password2']:
            return data
        raise serializers.ValidationError("passwords must be identical")

    def create(self, validated_data):
        validated_data["password"] = validated_data["password1"]
        del(validated_data['password1'])
        del (validated_data['password2'])
        return MyUser.objects.create_user(**validated_data)


class IssueSerializer(serializers.ModelSerializer):
    # comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'priority', 'status', 'project', 'author', 'assignee', 'created_time',
                  'comments']


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user', 'project', 'permission', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    # contributors = serializers.PrimaryKeyRelatedField(many=True, queryset=Contributor.objects.all())
    # issues = serializers.PrimaryKeyRelatedField(many=True, queryset=Issue.objects.all())
    contributors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    issues = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'contributors', 'issues']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['description', 'author', 'issue', 'created_time']