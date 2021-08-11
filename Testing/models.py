from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Test.models import Test
from Task.models import Task, MultipleChoiceTestAnswer, MultipleChoiceTest
from django.db.models.signals import post_save
from JustTesting.utils.query import InheritanceManager
from django.contrib.sessions.backends.base import SessionBase


class TestingSession(models.Model):
    """
    Base class for test sesions.

    Attributes:
        test: Test for create TestingSession.
        begin: Date and time when testing was/should be beginning.
               It is time of create TestingSession by default.
        end: Data and time when testing was/should be over.
             It is time of create TestingSession + test.duration by default.
        result: None if test_session is not ended else 
                equal of testing result (in percents).
    """
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Тест",
        help_text="Оберіть тест",
    )
    begin = models.DateTimeField(
        null=False,
        blank=True,
        verbose_name="Початок",
        help_text="Початок тестування",
    )
    end = models.DateTimeField(
        null=False,
        blank=True,
        verbose_name="Завершення",
        help_text="Дата та час, коли тестування має бути завершено/було завершено",
    )
    tasks = models.ManyToManyField(
        Task,
        through="M2MTaskInTestingSession",
        verbose_name="Завдання",
        help_text="Завдання у сесії тестування",
    )
    result = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Результат, %",
        help_text="Результат тестування у відсотках",
    )
    objects = InheritanceManager()

    def save(self):
        if self._state.adding:
            self._set_begin_and_end_if_none()
        super().save()

    def _set_begin_and_end_if_none(self):
        if not self.begin:
            self.begin = timezone.now()
        if not self.end:
            self.end = self.begin + \
                timezone.timedelta(minutes=self.test.duration)

    def is_correct_user(self, request) -> bool:
        """
        check user or session
        """
        raise NotImplementedError("This function must be implemented by derivative class")


class M2MTaskInTestingSession(models.Model):
    """
    Links tasks and testing_session.

    Attributes:
        session: TestingSession.
        task: Task.
        is_completed: True if task is completed else False.
        order: Field for ordering tasks in testing_session (if equal ordering by pk).
        issue_datetime: date and time of issue of task. 
                        None if the task was not issued.
    """
    session = models.ForeignKey(
        TestingSession,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="task_set",
        verbose_name="Сесія",
        help_text="Сесія тестування",
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="session_set",
        verbose_name="Завдання",
        help_text="Завдання для сесії тестування",
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name="Вирішено",
        help_text="Чи було надано відповідь на це завдання?",
    )
    order = models.PositiveBigIntegerField(
        null=False,
        blank=True,
        default=0,
        verbose_name="Розташування завдання",
        help_text="Чим більше значення, тим пізніше це завдання буде знаходитись у списку завдань сесії",
    )
    issue_datetime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Видано",
        help_text="Дата та час видачі завдання",
    )

    class Meta:
        verbose_name = "Список питань в тесті"
        verbose_name_plural = "Списки питань в тесті"
        db_table = "Testing_task_Testingsession"
        ordering = ['order', 'id']

    def replace_to_end(self):
        """
        Make the order largest in this test_session
        """
        self.order = self.session.task_set.last().order + 1


class TestingSessionOfUnautorizedUser(TestingSession):
    information = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Інформація про користувача",
        help_text="Прізвище, ім'я, номер групи, тощо",
    )

    def __str__(self):
        return "%s (%s)" % (self.information, self.test)

    class Meta:
        verbose_name = "Сесія тестування неавторизованого користувача"
        verbose_name_plural = "Сесії тестувань неавторизованих користувачів"

    def save(self, session: SessionBase):
        super().save()
        session["test_session_id"] = self.id
        if session.get_expiry_date() < self.end:
            # 1 hours after end it is time for take result of testing
            # if user did not have time to finish testing on time.
            session.set_expiry(self.end + timezone.timedelta(hours=1))

    def is_correct_user(self, request) -> bool:
        return self.id == request.session.get("test_session_id")


class TestingSessionOfAutorizedUser(TestingSession):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Коричтувач",
        help_text="Користувач, що проходив цю сесію тестування",
    )

    def __str__(self):
        return "%s (%s)" % (self.user, self.test)

    class Meta:
        verbose_name = "Сесія тестування авторизованого користувача"
        verbose_name_plural = "Сесії тестувань авторизованих користувачів"

    def is_correct_user(self, request) -> bool:
        return self.user == request.user


def _create_task_set_for_test_session(sender, instance, created: bool, *args, **kwargs):
    """
    create set of M2MTaskInTestingSession for test_session when session created.
    """
    import random
    from django.forms import ValidationError
    from Test.models import M2MTaskListInTest

    if created:
        task_lists_in_test = M2MTaskListInTest.objects.filter(
            test=instance.test)
        for task_list_in_test in task_lists_in_test:
            try:
                task_list_in_test.clean()
            except ValidationError:
                instance.delete()
                raise

        for task_list_in_test in task_lists_in_test:
            tasks = list(task_list_in_test.task_list.task_set.all())
            for _ in range(task_list_in_test.task_count):
                index = random.randint(0, len(tasks)-1)
                M2MTaskInTestingSession(
                    session=instance, task=tasks[index]
                ).save()
                tasks.pop(index)


post_save.connect(
    _create_task_set_for_test_session,
    sender=TestingSessionOfAutorizedUser
)
post_save.connect(
    _create_task_set_for_test_session,
    sender=TestingSessionOfUnautorizedUser
)


class Solution(models.Model):
    """
    Base class for solutions in testing session.

    Attributes:
        task_in_testing_session: link to M2MTaskInTestingSession.
        datetime: Date and time of solution create.
        result: Result of solution in percents.
    """
    task_in_testing_session = models.OneToOneField(
        M2MTaskInTestingSession,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Завдання з сесії тестування",
        help_text="Завдання, для якого було отримано цей розв'язок",
    )
    datetime = models.DateTimeField(
        null=False,
        default=timezone.now,
        verbose_name="Дата та час",
        help_text="Дата та час отримання розв'язку завдання",
    )
    result = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        verbose_name="Результат, %",
        help_text="Результат розв'язку у відсотках",
    )
    objects = InheritanceManager()


class MultipleChoiceTestSolution(Solution):
    """
    Solution of MultipleChoiceTest.
    """
    task_model = MultipleChoiceTest
    selected_answers = models.ManyToManyField(
        MultipleChoiceTestAnswer,
        verbose_name="Відповіді",
        help_text="Обрані варіанти відповідей",
    )

    def save(self, commit: bool = True):
        if commit:
            self.result = self._calculate_result()
        super().save(commit)

    def _calculate_result(self) -> float:
        selected_options_weight = 0
        for option in self.selected_answers.all():
            if option.weight == 0:
                return 0
            selected_options_weight += option.weight

        sum_weight = 0
        for option in self.task_in_testing_session.task.multiplechoicetest.answer_set.all():
            sum_weight += option.weight

        if sum_weight > 0:
            return 100 * selected_options_weight/sum_weight
