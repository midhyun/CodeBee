from django import forms

class CounterTextInput(forms.TextInput):
    template_name = "widgets/counter_text.html"