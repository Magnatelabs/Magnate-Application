# This command does a quick check if the payment gateway interface works
# Right now it only works with Authorize.net, and even this is half-baked

from django.core.management.base import NoArgsCommand, CommandError
from billing.integration import get_integration
import datetime
import time
import urllib
import urllib2

# Sample data for a test transaction
entry = {
    'first_name': 'Martha',
    'last_name': 'Graham',
    'zip': 98017,
    'address': '1300 East 62nd st. 2nd floor',
    'city': 'New York',
    'country': 'USA',
    'card_num': '4007000000027', # Visa test card for Authorize.net
    'exp_date': '01/28', # expires in 2028
    'relay_url': 'http://magnate-prod.herokuapp.com/donations/authorize_net/authorize_net-notify-handler/',
}

class Command(NoArgsCommand):
    help = "Test the payment gateway"
    def handle_noargs(self, **options):
        print "Testing the payment gateway"
        print "Half-baked test: no sensible relay_url is supplied"
        print "So should show an error, but mention that the transaction has been approved"

        int_obj = get_integration("authorize_net_dpm")
        fields = {'x_amount': time.time() % 86400 , # fairly unique amount so we do not worry about duplicate transactions 
                  'x_fp_sequence': datetime.datetime.now().strftime('%Y%m%d%H%M%S'), # any identifier for the transaction
                  'x_fp_timestamp': str(int(time.time())), # the timestamp when x_fp_sequence was generated
                  'x_recurring_bill': 'F',
                  'x_relay_url': entry['relay_url'],
                  'x_cust_id': 'test',
                  'x_first_name': entry['first_name'],
                  'x_last_name': entry['last_name'],
                  'x_zip': entry['zip'],
                  'x_address': entry['address'],
                  'x_city': entry['city'],
                  'x_country': entry['country'],

                  'x_card_num': entry['card_num'],
                  'x_exp_date': entry['exp_date'],
              }
        int_obj.add_fields(fields)
        form = int_obj.generate_form()
        # now just POST the form
                  
        # or should we use x.html_name instead of x.name?
        query_dict = {x.name:x.value() for x in form}
        query_dict = {k:query_dict[k] for k in query_dict if query_dict[k] is not None}
        query_str = urllib.urlencode(query_dict)
        print 'Issuing POST request...'
        print query_str
        result = urllib2.urlopen(int_obj.service_url, query_str)

        print "\nYou should see a redirect snippet on success:\n"
        # need result.getcode()==200
        lines=result.readlines()
        print lines, "\n"

        is_snippet=False
        transaction_approved=False
        for l in lines:
            if 'script' in l.lower(): # Javascript expected to redirect the user's browser on success or failure, indicating that Authorize.Net was able to receive a response from our website. So it successfully reported this (sample, fake) transaction to us.
                is_snippet=True
            if 'approved' in l.lower():
                transaction_approved = True
                

        if not is_snippet:
            raise CommandError('Payment gateway failed to communicate the transaction to the website. API flow failure. The gateway should return a snippet to redirect the user to a success/failure page')

        if not transaction_approved:
            raise CommandError('Transaction failed, even though the payment gateway successfully communicated this fact to the website.')

        print "\nOK, Success"