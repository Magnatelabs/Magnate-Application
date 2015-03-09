from django import forms

ACCT_TYPE_CHOICES = (('CHECKING', 'Checking',), ('BUSINESSCHECKING', 'Business Checking',), ('SAVINGS', 'Savings',), )
CARD_TYPE_CHOICES = (('MASTERCARD', 'Mastercard',), ('VISA', 'Visa',), ('AMERICANEXP', 'American Express',), )

class AuthorizeNetForm(forms.Form):
    x_card_type = forms.ChoiceField(widget=forms.Select, choices=CARD_TYPE_CHOICES, label="")

    x_address = forms.CharField(widget=forms.HiddenInput(), max_length=60, label="Address")
    x_city = forms.CharField(widget=forms.HiddenInput(), max_length=40, label="City")
    x_state = forms.CharField(widget=forms.HiddenInput(), max_length=40, label="State")
    x_country = forms.CharField(widget=forms.HiddenInput(), max_length=60, label="Country")

    x_amount = forms.CharField(label="Amount (in USD)", widget=forms.HiddenInput())

    x_login = forms.CharField(widget=forms.HiddenInput(), required=False)
    x_fp_sequence = forms.CharField(widget=forms.HiddenInput(), required=False)
    x_fp_timestamp = forms.CharField(widget=forms.HiddenInput())
    x_fp_hash = forms.CharField(widget=forms.HiddenInput())
    x_type = forms.CharField(widget=forms.HiddenInput())
    
    x_cust_id = forms.CharField(widget=forms.HiddenInput(), required=True)
    x_extra_data = forms.CharField(widget=forms.HiddenInput(), required=True)    
    x_relay_url = forms.CharField(widget=forms.HiddenInput(), required=True)
    x_relay_response = forms.CharField(initial="TRUE", widget=forms.HiddenInput())
    x_payment_method = forms.CharField(widget=forms.HiddenInput())

class AuthorizeNetDPMForm(AuthorizeNetForm):
    x_card_num = forms.CharField(max_length=16, label="Credit Card #")
    x_exp_date = forms.CharField(max_length=5, label="Exp Date (mm/yy)")
    x_card_code = forms.CharField(max_length=4, label="CVV")

    x_first_name = forms.CharField(max_length=50, label="First Name")
    x_last_name = forms.CharField(max_length=50, label="Last Name")

    x_zip = forms.CharField(max_length=20, label="Zip")


class AuthorizeNetDPMFormCheck(AuthorizeNetForm):
    x_bank_aba_code = forms.CharField(label="ABA Code#", max_length=9, min_length=9) 
    x_bank_acct_num = forms.CharField(max_length=16, label="Account Num#")
    x_bank_acct_type = forms.ChoiceField(widget=forms.Select, choices=ACCT_TYPE_CHOICES, label="Account type")
    x_bank_name = forms.CharField(max_length=16, label="Bank Name")
    x_bank_acct_name = forms.CharField(max_length=16, label="Bank Account Name")
    x_echeck_type = forms.CharField(widget=forms.HiddenInput(), max_length=16, initial="WEB")
    x_recurring_billing = forms.CharField(widget=forms.HiddenInput(), max_length=16, initial="NO")
    x_delim_data = forms.CharField(widget=forms.HiddenInput(), initial="TRUE") 
 


