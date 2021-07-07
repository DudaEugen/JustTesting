from typing import Optional
from abc import ABC, abstractmethod
from django import forms


class ModelAndInlineFormsetContainer(ABC):
    model = None
    model_fields = ()
    formset_model = None
    formset_model_fields = ()
    formset = None
    formset_model_foreignkey_name = ""

    def __init__(self, **kwargs):
        f = forms.modelform_factory(
            model=self.model, fields=self.model_fields
        )
        self.form = f(**kwargs)

        instance_of_model = kwargs.get("instance")
        formset_factory = forms.inlineformset_factory(
            self.model,
            self.formset_model,
            formset=self.formset,
            fields=self.formset_model_fields,
            extra=2 if instance_of_model is None else 1,
        )
        q = self.formset_model.objects.none() if instance_of_model is None else\
            self.__class__.get_queryset(instance_of_model)
        self.formset = formset_factory(
            queryset=q,
            **kwargs
        )

    @classmethod
    @abstractmethod
    def get_queryset(cls, instance):
        pass

    def is_valid(self):
        return self.form.is_valid() and self.formset.is_valid()

    def save(self, commit: bool = True):
        self.formset.instance = self.form.save(commit)
        self.formset.save(commit)
