from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label="")
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = ''
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'submit'))