from django.db import models
import uuid
from typing import List, Iterable
from JustTesting.utils.query import InheritanceManager


class KnowledgeField(models.Model):
    name = models.CharField(
        max_length=250,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Найменування",
        help_text="Найменування області знань",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Область знань"
        verbose_name_plural = "Області знань"
        ordering = ['name']


class TaskList(models.Model):
    """
    List of tasks. Tasks can be of defferent types.

    When creating a testing session, 
    tasks are randomly selected from the list of tasks.
    """
    knowledge_field = models.ForeignKey(
        KnowledgeField,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Область знань",
        help_text="Оберіть область знань",
    )
    name = models.CharField(
        max_length=250,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Найменування",
        help_text="Найменування списку завдань",
    )

    def __str__(self):
        prefix = f"({self.knowledge_field}) " if self.knowledge_field else ""
        return prefix + self.name

    class Meta:
        verbose_name = "Список завдань"
        verbose_name_plural = "Списки завдань"
        ordering = ['knowledge_field__name', 'name']


class Task(models.Model):
    """
    Base class for tasks.

    Task is not abstract class in order to be able 
    to take tasks of different types from the database, 
    regardless of their types. To do this, it is enough 
    to place tasks of different types in one task_list.
    """
    task_list = models.ForeignKey(
        TaskList,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Список завдань",
        help_text="Оберіть список завдань",
    )
    objects = InheritanceManager()


class MultipleChoiceTest(Task):
    """
    Task with multiple choice.

    Each answer option of MultipleChoiceTest has an attribute 'weight'.
    Weight is equal 0 if answer option is wrong.
    The result of task is 0 if one of the selected answer options is wrong option.
    Otherwise, the result is equal to the product of 100% and
    the sum of the weights of selected answer options, 
    divide by sum of the weights of all options for the task.
    """
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

    def clean(self):
        from django.forms import ValidationError
        from django.utils.translation import ugettext_lazy as _

        super().clean()
        if self.text == "":
            raise ValidationError({"text": _("Завдання має містити текст")})

    @staticmethod
    def clean_answer_set(answers: Iterable):
        """
        raise django.forms.ValidationError if 
        answers is incorrect collection of answers for MultipleChoiceTest.
        :param answers: Iterable[MultipleChoiceTestAnswer]
        """
        from django.forms import ValidationError
        from django.utils.translation import ugettext_lazy as _

        if len(answers) < 2:
            # task must be have 2 or more answer options.
            raise ValidationError(
                "Завдання має містити не менше 2 варіантів відповіді"
            )
        errors: List[ValidationError] = []
        sum_weight: int = 0
        for i in range(len(answers)):
            sum_weight += answers[i].weight
            for j in range(i):
                if answers[i].text == answers[j].text:
                    # all answer options must be different.
                    errors.append(ValidationError(
                        f"Завданя містить два однакових варіанти відповіді: {j+1} та {i+1}"
                    ))
        if sum_weight == 0:
            # task must be have 1 or more answer options with non zero weight.
            errors.append(ValidationError(
                "Завдання не містить варіантів відповіді, що позначені як вірні"
            ))
        if errors:
            raise ValidationError(errors)


class MultipleChoiceTestAnswer(models.Model):
    """
    Answer option to task with multiple choice.

    Id is uuid, because this type does not give users information 
    about the position of the answer option among others when creating a task. 
    (For example, with int, the user can understand that 
    the variant with the smallest number was the first) 
    This does not require any additional action when saving the task 
    to the database or transferring it to the user.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    test = models.ForeignKey(
        MultipleChoiceTest,
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

    def clean(self):
        from django.forms import ValidationError
        from django.utils.translation import ugettext_lazy as _

        super().clean()
        if self.text == "":
            raise ValidationError(
                {"text": _("Варіант відповіді має містити текст")}
            )
