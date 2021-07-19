from django.db import models
from django.contrib.auth.models import User
from django.db.models.expressions import OrderBy
from Test.models import Test
from Task.models import Task
from django.db.models.signals import post_save


class TestSession(models.Model):
    """
    Base class for test sesions.

    Attributes:
        test: Test for create TestSession.
        begin: Date and time when testing was/should be beginning.
               It is time of create TestSession by default.
        end: Data and time when testing was/should be over.
             It is time of create TestSession + test.duration by default.
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
        through="M2MTaskInTestSession",
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

    def save(self):
        if self._state.adding:
            self._set_begin_and_end_if_none()
        super().save()

    def _set_begin_and_end_if_none(self):
        from django.utils import timezone

        if not self.begin:
            self.begin = timezone.now()
        if not self.end:
            self.end = self.begin + \
                timezone.timedelta(minutes=self.test.duration)


class M2MTaskInTestSession(models.Model):
    """
    Links tasks and test_session.

    Attributes:
        session: TestSession.
        task: Task.
        is_completed: True if task is completed else False.
        order: Field for ordering tasks in test_session (if equal ordering by pk).
    """
    session = models.ForeignKey(
        TestSession,
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

    class Meta:
        verbose_name = "Список питань в тесті"
        verbose_name_plural = "Списки питань в тесті"
        db_table = "Testing_task_Testsession"
        ordering = ['order', 'id']

    def replace_to_end(self):
        """
        Make the order largest in this test_session
        """
        self.order = self.session.task_set.last().order + 1


class TestSessionOfUnautorizedUser(TestSession):
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


class TestSessionOfAutorizedUser(TestSession):
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


def _create_task_set_for_test_session(sender, instance, created: bool, *args, **kwargs):
    """
    create set of M2MTaskInTestSession for test_session when session created.
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
                M2MTaskInTestSession(
                    session=instance, task=tasks[index]
                ).save()
                tasks.pop(index)


post_save.connect(
    _create_task_set_for_test_session,
    sender=TestSessionOfAutorizedUser
)
post_save.connect(
    _create_task_set_for_test_session,
    sender=TestSessionOfUnautorizedUser
)