from abc import ABC, abstractmethod
from django import forms


class ModelAndInlineFormsetContainer(ABC):
    """
    Abstract class for association 
    form of model and inline formset for this model.

    Attributes:
        model: Model for create ModelForm.
        fields: Fields of model for create ModelForm.
        inline_model: Model for create inline formset.
        inline_model_fields: Fields of model for create inline formset.
        inline_form: Form for create inline formset.
        formset: Formset.

    Implement class must realize classmethod get_queryset and specify values:
    model
    fields
    inline_model and inline_model_fields or/and inline_form
    optionally formset
    """
    model = None
    model_fields = None
    inline_model = None
    inline_model_fields = None
    inline_form = forms.ModelForm
    formset = forms.BaseInlineFormSet

    def __init__(self, **kwargs):
        f = forms.modelform_factory(
            model=self.model, fields=self.model_fields
        )
        self.form = f(**kwargs)

        instance_of_model = kwargs.get("instance")
        formset_factory = forms.inlineformset_factory(
            self.model,
            self.inline_model,
            form=self.inline_form,
            formset=self.formset,
            fields=self.inline_model_fields,
            extra=2 if instance_of_model is None else 1,
        )
        q = self.inline_model.objects.none() if instance_of_model is None else\
            self.__class__.get_queryset(instance_of_model)
        self.formset = formset_factory(
            queryset=q,
            **kwargs
        )

    @classmethod
    @abstractmethod
    def get_queryset(cls, instance):
        """
        Called if instance was be passed to constructor.
        :return: QuerySet of objects for create forms for inline formset.        
        """
        pass

    def is_valid(self):
        return self.form.is_valid() and self.formset.is_valid()

    def save(self, commit: bool = True):
        self.formset.instance = self.form.save(commit)
        self.formset.save(commit)
