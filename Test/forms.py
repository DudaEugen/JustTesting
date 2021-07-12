from django import forms
from .models import M2MTaskListInTest, Test
from JustTesting.utils.formsets import ModelAndInlineFormsetContainer


class TestWithTaskListForm(ModelAndInlineFormsetContainer):
    model = Test
    model_fields = (
        "name",
        "duration",
        "is_allowed",
        "is_allow_for_unautorized_users",
    )
    inline_model = M2MTaskListInTest
    inline_model_fields = "__all__"

    @classmethod
    def get_queryset(cls, instance):
        return instance.m2mtasklistintest_set.all()
