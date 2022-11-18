from django import forms

class CounterTextArea(forms.Textarea):
    template_name = "widgets/counter_text.html"