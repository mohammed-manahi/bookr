from django import forms
from django.core.exceptions import ValidationError


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    # the choices for ChoiceField should be tuple of tuples or it can be list of lists
    search_choices = (("title", "Title"), ("contributor", "Contributor"))
    search_in = forms.ChoiceField(required=False, choices=search_choices)


class OrderForm(forms.Form):

    # custom form validation using django exceptions
    def validate_email_domain(value):
        if value.split("@")[-1].lower() != "example.com":
            raise ValidationError("The email address must be on the domain example.com.")

    # custom clean method to retrieve email in loser case
    def clean_email(self):
        return self.cleaned_data['email'].lower()

    # custom cross-fields validation to send enter email to send confirmation and ensure total orders are less than 100
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["send_confirmation"] and not cleaned_data.get("email"):
            self.add_error("email", "Please enter an email address to receive the confirmation message.")
        elif cleaned_data.get("email") and not cleaned_data["send_confirmation"]:
            self.add_error("send_confirmation", "Please check this if you want to receive a confirmation email.")
        item_total = cleaned_data.get("magazine_count", 0) + cleaned_data.get("book_count", 0)
        if item_total > 100:
            self.add_error(None, "The total number of items must be 100 or less.")

    magazine_count = forms.IntegerField(min_value=0, max_value=80,
                                        widget=forms.NumberInput(attrs={"placeholder": "0"}))
    book_count = forms.IntegerField(min_value=0, max_value=50,
                                    widget=forms.NumberInput(attrs={"placeholder": "0"}))
    send_confirmation = forms.BooleanField(required=False)
    email = forms.EmailField(required=False, validators=[validate_email_domain],
                             widget=forms.EmailInput(attrs={"placeholder": "name@example.com"}))
