from django.db import models
from django.db.models.aggregates import Min
from Task.models import TaskList
from django.core.validators import MinValueValidator


class Test(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Найменування",
        help_text="Найменування тесту",
    )
    task_lists = models.ManyToManyField(
        TaskList,
        through="M2MTaskListInTest",
        verbose_name="Списки завдань",
        help_text="Списки, завдання з яких використовуються у тесті",
    )
    duration = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name="Тривалість, хв",
        help_text="Максимально дозволена тривалість тестування у хвилинах",
    )
    is_allowed = models.BooleanField(
        default=True,
        verbose_name="Відкрито",
        help_text="Дозволити проходження тесту",
    )
    is_allow_for_unautorized_users = models.BooleanField(
        default=False,
        verbose_name="Неавторизовані користувачі",
        help_text="Чи дозволено проходження цього тесту для неавторизованих користувачів?",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тести"
        ordering = ['name']


class M2MTaskListInTest(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Тест",
        help_text="Оберіть тест",
        db_column="test_id",
    )
    task_list = models.ForeignKey(
        TaskList,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name="Список питань",
        help_text="Оберіть список питань",
        db_column="tasklist_id",
    )
    task_count = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        null=False,
        blank=False,
        verbose_name="Кількість завдань",
        help_text="Скільки завдань із вказано списку використовувати у обраному тесті",
    )

    def __str__(self):
        return "%s-%s" % (self.test, self.task_list)

    class Meta:
        verbose_name = "Список питань в тесті"
        verbose_name_plural = "Списки питань в тесті"
        db_table = "Test_tasklist_Test"
        unique_together = [["test", "task_list"]]
