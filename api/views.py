import datetime
import random

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import BotUsers, UsersTrainingResults, TrainingsForPrograms, Programs, WODs, UsersWodResults, Coaches
from api.serializers import UsersTrainingResultsSerializer, UsersWodResultsSerializer, ProgramsSerializer, \
    BotUsersSerializer


class UserInfoView(APIView):
    '''Представление общей информации о пользователе,
    а также о текущей программе тренировок пользователя'''

    def get(self, request, format=None):
        user_tlg_id = request.query_params.get('user_tlg_id')
        if user_tlg_id:
            user_object = BotUsers.objects.filter(user_tlg_id=user_tlg_id)
            result_object = user_object.values_list(
                'user_tlg_id',
                'user_tlg_name',
                'last_training_date',
                'program__title',
                'program__numbers_of_trainings',
                'training__training_number',
            )
            return Response(result_object, status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = BotUsersSerializer(data=request.data)
        if serializer.is_valid():
            user_tlg_id = serializer.data.get('user_tlg_id')
            BotUsers.objects.update_or_create(user_tlg_id=user_tlg_id,
                                              defaults={
                                                  'user_tlg_id': user_tlg_id,
                                                  'user_tlg_name': serializer.data.get('user_tlg_name')
                                              })
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)


class UserTrainingProgramView(APIView):
    '''Представление информации о программе тренировок пользователя'''

    def get(self, request, format=None):
        user_tlg_id = request.query_params.get('user_tlg_id')
        if user_tlg_id:
            program_object = BotUsers.objects.filter(user_tlg_id=user_tlg_id).select_related('program')
            result_object = program_object.values_list(
                'program__title',
                'program__description',
                'program__goal',
                'program__numbers_of_trainings',
                'program__workout_duration',
                'program__recommended_number_of_trainings',
                'training__training_number',
                'training__id',
                'program__id',
            )
            return Response(result_object, status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)


class UserCurrentTraningView(APIView):
    '''Представление информации о текущей тренировке пользователя'''

    def get(self, request, format=None):
        user_tlg_id = request.query_params.get('user_tlg_id')
        if user_tlg_id:
            training_object = BotUsers.objects.filter(user_tlg_id=user_tlg_id).select_related('training')
            result_object = training_object.values_list(
                'training__id',
                'program__title',
                'training__training_number',
                'training__training_description',
            )
            return Response(result_object, status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)


class UserTrainingResultsView(APIView):
    '''Представление для результатов тренировок пользователя'''

    def get(self, request, format=None):
        user_tlg_id = request.query_params.get('user_tlg_id')
        training_id = request.query_params.get('id')
        if not training_id:
            # если есть user_tlg_id, то получаем список всех результатов тренировок
            user_results = UsersTrainingResults.objects.filter(user__user_tlg_id=user_tlg_id).select_related('user')
            results_objects = UsersTrainingResultsSerializer(user_results, many=True)
        elif training_id:
            # если есть training_id, то получаем конкретный результат тренировки
            results_objects = UsersTrainingResults.objects.get(pk=training_id)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)
        return Response(results_objects.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UsersTrainingResultsSerializer(data=request.data)
        if serializer.is_valid():
            training = TrainingsForPrograms.objects.get(pk=serializer.data.get('training'))
            user = BotUsers.objects.get(pk=serializer.data.get('user'))
            UsersTrainingResults.objects.create(
                training=training,
                date=datetime.date.today(),
                result=serializer.data.get('result'),
                user=user,
            )
            user_training_number = user.training.training_number
            next_training = TrainingsForPrograms.objects.get(training_number=user_training_number + 1)
            user.training = next_training
            user.save()
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)


class CleanResultsView(APIView):
    '''Очистка всех результатов тренировок пользователя
    и удаление связи FK программы тренировок'''

    def get(self, request, format=None):
        user_tlg_id = request.query_params.get('user_tlg_id')
        if user_tlg_id:
            user_object = BotUsers.objects.get(user_tlg_id=user_tlg_id)
            # удаляем результаты тренировок пользователя
            UsersTrainingResults.objects.filter(user=user_object).delete()
            # очищаем поля программы и тренировки
            user_object.program = None
            user_object.training = None
            user_object.save()
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)


class ProgramsView(APIView):
    '''Представление списка программ или деталей программы тренировок'''

    def get(self, request, format=None):
        program_id = request.query_params.get('program_id')
        try:
            if program_id:
                print('HEREEEE....')
                program_object = Programs.objects.get(pk=program_id)
                result_object = ProgramsSerializer(program_object, many=False)
            else:
                print('HEREEEE....2')
                programs_lst = Programs.objects.all()
                result_object = ProgramsSerializer(programs_lst, many=True)
            return Response(result_object.data, status.HTTP_200_OK)
        except Exception:
            return Response(status.HTTP_400_BAD_REQUEST)


class AssignProgram(APIView):
    '''Назначить программу тренировок и первую тренировку пользователю'''

    def get(self, request, format=None):
        program_id = request.query_params.get('program_id')
        user_tlg_id = request.query_params.get('user_tlg_id')
        if user_tlg_id and program_id:
            user_obj = BotUsers.objects.get(user_tlg_id=user_tlg_id)
            program = Programs.objects.get(pk=program_id)
            user_obj.program = program
            first_training = TrainingsForPrograms.objects.filter(program=program).get(training_number=1)
            user_obj.training = first_training
            user_obj.save()
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)


class RandomWodView(APIView):
    '''Получение случайного WOD из списка'''

    def get(self, request, format=None):
        number_objects = len(WODs.objects.all())
        random_id = random.randint(1, number_objects)
        random_wod = WODs.objects.filter(pk=random_id).values_list(
            'id',
            'title',
            'modality',
            'description',
        )
        return Response(random_wod, status.HTTP_200_OK)


class WodResultsView(APIView):
    '''Представление для результатов выполнения WOD'''

    def get(self, request, format=None):
        last_results = UsersWodResults.objects.all()[:5].values_list(
            'wod__title',
            'user__user_tlg_name',
            'result',
            'date',
        )
        return Response(last_results, status.HTTP_200_OK)

    # {"wod": 1, "user": 1, "result": "7 мин. 56 сек."}

    def post(self, request, format=None):
        print(f'WE ARE HERE...\n{request.data}')
        serializer = UsersWodResultsSerializer(data=request.data)
        if serializer.is_valid():
            print('WE ARE HERE...5')
            wod_instance = WODs.objects.get(pk=serializer.data.get('wod'))
            user_instance = BotUsers.objects.get(pk=serializer.data.get('user'))
            new_result = UsersWodResults(
            wod=wod_instance,
            user=user_instance,
            result=serializer.data.get('result'),
            )
            new_result.save()
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)


class CoachViews(APIView):
    '''Представление для модели тренеров'''

    def get(self, request, format=None):
        coach_id = request.query_params.get('coach_id')
        if coach_id:
            coach_obj = Coaches.objects.filter(pk=coach_id).values_list(
                'id',
                'tlg_photo_id',
                'coach_tlg_id',
                'name',
                'age',
                'location',
                'about_coach',
                'contacts',
            )
        else:
            coach_obj = Coaches.objects.all().values_list(
                'id',
                'name',
            )
        return Response(coach_obj, status.HTTP_200_OK)







