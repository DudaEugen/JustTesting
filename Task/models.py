from django.db import models
from typing import Optional


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
        verbose_name = "Завдання з вибором кількох варіантів відповіді"
        verbose_name_plural = "Завдання з вибором кількох варіантів відповіді"

    @staticmethod
    def find_errors_in_answer_list(answers: list) -> Optional[str]:
        if len(answers) < 2:
            return "Завдання має містити не менше 2 варіантів відповіді"
        sum_weight: int = 0
        for i in range(len(answers)):
            sum_weight += answers[i].weight
            for j in range(i):
                if answers[i].text == answers[j].text:
                    return f"Завданя містить два однакових варіанти відповіді: {i+1} та {j+1}"
        if sum_weight == 0:
            return "Завдання не містить варіантів відповіді, що позначені як вірні"


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
        null=False,
        blank=False,
        verbose_name="Вага",
        help_text="Чим більше число, тим більший відсоток дасть вибір цього варіанту. 0 - невірний варіант",
    )

    def __str__(self):
        return f"self.text[:50]..." if len(self.text) > 50 else self.text

    class Meta:
        verbose_name = "Варіант відповіді на тест з вибором кількох варіантів"
        verbose_name_plural = "Варіанти відповіді на тести з вибором кількох варіантів"
        default_related_name = "answer_set"
