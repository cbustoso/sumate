from django import forms
from . import errors

class AccountActionForm(forms.Form):
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )
    send_email = forms.BooleanField(
        required=False,
    )
    @property
    def email_subject_template(self):
        return 'email/account/notification_subject.txt'
    @property
    def email_body_template(self):
        raise NotImplementedError()
    def form_action(self, account, user):
        raise NotImplementedError()
    def save(self, account, user):
        try:
            account, action = self.form_action(account, user)
        except errors.Error as e:
            error_message = str(e)
            self.add_error(None, error_message)
            raise
        return account, action