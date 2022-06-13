from django.contrib import admin

# Register your models here.
from api.models import BotUsers, Programs, TrainingsForPrograms, UsersTrainingResults, WODs, UsersWodResults, Coaches


class BotUsersAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user_tlg_id',
        'user_tlg_name',
        'program',
        'training',
        'last_training_date',
    ]
    list_display_links = [
        'user_tlg_id',
        'user_tlg_name',
        'program',
        'training',
        'last_training_date',
    ]
    # list_editable = [
    #     'user_tlg_id',
    #     'user_tlg_name',
    #     'program',
    #     'training',
    #     'last_training_date',
    # ]


class ProgramsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'description',
        'goal',
        'numbers_of_trainings',
        'workout_duration',
        'recommended_number_of_trainings',
    ]
    list_display_links = [
        'id',
        'title',
        'description',
        'goal',
        'numbers_of_trainings',
        'workout_duration',
        'recommended_number_of_trainings',
    ]


class TrainingsForProgramsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'program',
        'training_number',
        'training_description',
    ]
    list_display_links = [
        'id',
        'program',
        'training_number',
        'training_description',
    ]


class UsersTrainingResultsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'training',
        'date',
        'result',
        'user',
    ]
    list_display_links = [
        'id',
        'training',
        'date',
        'result',
    ]


class WodAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'modality',
        'description',
    ]
    list_display_links = [
        'id',
        'title',
        'modality',
        'description',
    ]


class UsersWodResultsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'wod',
        'user',
        'result',
    ]
    list_display_links = [
        'id',
        'wod',
        'user',
        'result',
    ]


class CoachesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'tlg_photo_id',
        'coach_tlg_id',
        'name',
        'age',
        'location',
        'about_coach',
        'contacts',
    ]
    list_display_links = [
        'id',
        'tlg_photo_id',
        'coach_tlg_id',
        'name',
        'age',
        'location',
        'about_coach',
        'contacts',
    ]


admin.site.register(BotUsers, BotUsersAdmin)
admin.site.register(Programs, ProgramsAdmin)
admin.site.register(TrainingsForPrograms, TrainingsForProgramsAdmin)
admin.site.register(UsersTrainingResults, UsersTrainingResultsAdmin)
admin.site.register(WODs, WodAdmin)
admin.site.register(UsersWodResults, UsersWodResultsAdmin)
admin.site.register(Coaches, CoachesAdmin)
