from rest_framework import serializers

from api.models import BotUsers, Programs, TrainingsForPrograms, UsersTrainingResults, WODs, UsersWodResults, Coaches


class BotUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUsers
        fields = '__all__'


class ProgramsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programs
        fields = '__all__'


class TrainingsForProgramsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingsForPrograms
        fields = '__all__'


class UsersTrainingResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersTrainingResults
        fields = '__all__'


class WODsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WODs
        fields = '__all__'


class UsersWodResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersWodResults
        fields = '__all__'


class CoachesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coaches
        fields = '__all__'
