from django.db import models

C = models.CharField(verbose_name='Имя пользователя в телеграме', max_length=100, blank=True, null=True)


class BotUsers(models.Model):
    '''Пользователи бота'''

    user_tlg_id = models.CharField(verbose_name='ID телеграма пользователя', max_length=50, db_index=True)
    user_tlg_name = models.CharField(verbose_name='Имя пользователя в телеграме', max_length=100)
    program = models.ForeignKey(verbose_name='Программа', to='Programs', on_delete=models.CASCADE, blank=True, null=True)
    training = models.ForeignKey(verbose_name='Тренировка', to='TrainingsForPrograms', on_delete=models.CASCADE, blank=True, null=True)
    last_training_date = models.DateField(verbose_name='Дата крайней тренировки', blank=True, null=True)

    class Meta:
        ordering = ['id']
        db_table = 'Пользователи'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.user_tlg_id


class Programs(models.Model):
    '''Программы тренировок'''

    title = models.CharField(verbose_name='Название программы', max_length=100)
    description = models.TextField(verbose_name='Описание программы', max_length=5000)
    goal = models.CharField(verbose_name='Цель программы', max_length=1000)
    numbers_of_trainings = models.IntegerField(verbose_name='Количество тренировок')
    workout_duration = models.CharField(verbose_name='Продолжительность тренировки', max_length=100)
    recommended_number_of_trainings = models.CharField(verbose_name='Рекомендуемое количество тренировок в неделю', max_length=20)

    class Meta:
        ordering = ['title']
        db_table = 'Программы тренировок'
        verbose_name = 'Программа тренировок'
        verbose_name_plural = 'Программы тренировок'

    def __str__(self):
        return self.title


class TrainingsForPrograms(models.Model):
    '''Тренировки для программ'''

    program = models.ForeignKey(to=Programs, on_delete=models.CASCADE, verbose_name='Программа')
    training_number = models.IntegerField(verbose_name='Номер тренировки')
    training_description = models.TextField(verbose_name='Описание тренировки', max_length=5000)

    class Meta:
        ordering = ['program']
        db_table = 'Тренировки для программ'
        verbose_name = 'Тренировка для программы'
        verbose_name_plural = 'Тренировки для программ'

    def __str__(self):
        return str(self.training_number)


class UsersTrainingResults(models.Model):
    '''Результаты тренировок пользователей'''

    training = models.ForeignKey(to=TrainingsForPrograms, on_delete=models.CASCADE, verbose_name='Тренировка')
    date = models.DateField(verbose_name='Дата', auto_now_add=True)
    result = models.TextField(verbose_name='Результат', max_length=2000)
    user = models.ForeignKey(to=BotUsers, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)

    class Meta:
        ordering = ['-date']
        db_table = 'Результаты тренировок пользователей'
        verbose_name = 'Резульат тренировки пользователя'
        verbose_name_plural = 'Результаты тренировок пользователей'

    def __str__(self):
        return self.result


class WODs(models.Model):
    '''WOD - workout of the day (кроссфит аббревиатура, какой-либо тренировочный комплекс)'''

    title = models.CharField(verbose_name='Название WOD', max_length=200)
    modality = models.CharField(verbose_name='Модальность', max_length=5)
    description = models.TextField(verbose_name='Описание комплекса', max_length=4000)

    class Meta:
        ordering = ['modality']
        verbose_name = 'WOD'
        verbose_name_plural = 'WODs'

    def __str__(self):
        return self.title


class UsersWodResults(models.Model):
    '''Пользовательские результаты WOD'''

    wod = models.ForeignKey(to=WODs, on_delete=models.CASCADE, verbose_name='WOD (комплекс)')
    user = models.ForeignKey(to=BotUsers, on_delete=models.CASCADE, verbose_name='Пользователь')
    result = models.CharField(verbose_name='Результат', max_length=1000)
    date = models.DateField(verbose_name='Дата выполнения', auto_now_add=True)

    class Meta:
        ordering = ['-date']
        db_table = 'Результаты WOD пользователей'
        verbose_name = 'Результат WOD пользователя'
        verbose_name_plural = 'Результаты WOD пользователей'

    def __str__(self):
        return self.result


class Coaches(models.Model):
    '''Тренеры'''

    tlg_photo_id = models.CharField(max_length=300, verbose_name='ID фото из телеграма', blank=True, null=True)
    coach_tlg_id = models.CharField(max_length=100, verbose_name='ID телеграма тренера')
    name = models.CharField(max_length=50, verbose_name='Имя тренера')
    age = models.IntegerField(verbose_name='Возраст тренера')
    location = models.CharField(verbose_name='Локация(город)', max_length=100)
    about_coach = models.TextField(verbose_name='О тренере', max_length=4000)
    contacts = models.TextField(verbose_name='Контакты тренера', max_length=4000)

    class Meta:
        ordering = ['id']
        db_table = 'Тренеры'
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'

    def __str__(self):
        return self.name
