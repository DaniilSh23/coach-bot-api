from django.urls import path, include

from api.views import UserInfoView, UserTrainingProgramView, UserCurrentTraningView, UserTrainingResultsView, \
    CleanResultsView, ProgramsView, AssignProgram, RandomWodView, CoachViews, WodResultsView

urlpatterns = [
    path('user_info/', UserInfoView.as_view(), name='user_info'),
    path('training_program/', UserTrainingProgramView.as_view(), name='training_program'),
    path('current_training/', UserCurrentTraningView.as_view(), name='current_training'),
    path('training_result/', UserTrainingResultsView.as_view(), name='training_result'),
    path('clean_results/', CleanResultsView.as_view(), name='clean_results'),
    path('programs/', ProgramsView.as_view(), name='programs'),
    path('assign_program/', AssignProgram.as_view(), name='assign_program'),
    path('random_wod/', RandomWodView.as_view(), name='random_wod'),
    path('wod_results/', WodResultsView.as_view(), name='wod_results'),
    path('coach/', CoachViews.as_view(), name='coach'),
]
