from django.db import models


class TaskList(models.Model):
    name = models.CharField(
        max_length=250,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Найменування",
        help_text="Найменування списку завдань",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Список завдань"
        verbose_name_plural = "Списки завдань"
        ordering = ['name']


class Task(models.Model):
    task_list = models.ForeignKey(
        TaskList,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Список завдань",
        help_text="Оберіть список завдань",
    )


class MultiplyChoiceTest(Task):
    text = models.TextField(
        null=True,
        blank=True,
        default="",
        verbose_name="Завдання",
        help_text="Введіть текст завдання для тесту",
    )

    def __str__(self):
        return f"self.text[:50]..." if len(self.text) > 50 else self.text

    class Meta:
        verbose_name = "Тест з вибором кількох варіантів відповіді"
        verbose_name_plural = "Тести з вибором кількох варіантів відповіді"


class MultiplyChoiceTestAnswer(models.Model):
    test = models.ForeignKey(
        MultiplyChoiceTest,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Тест",
        help_text="Оберіть тест",
    )
    text = models.TextField(
        null=True,
        blank=True,
        default="",
        verbose_name="Відповідь",
        help_text="Варіант відповіді",
    )
    weight = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Вага",
        help_text="Чим більше число, тим більший відсоток дасть вибір цього варіанту. 0 - невірний варіант",
    )

    def __str__(self):
        return f"self.text[:50]..." if len(self.text) > 50 else self.text

    class Meta:
        verbose_name = "Варіант відповіді на тест з вибором кількох варіантів"
        verbose_name_plural = "Варіанти відповіді на тести з вибором кількох варіантів"
        default_related_name = "answer_set"
