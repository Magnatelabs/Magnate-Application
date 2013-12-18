
** Testing **

Be sure to run the tests with `python manage.py test`. They MUST PASS. Exception: if you are not connected to Internet, you get 2 failures in the merchant app in `billing.tests.AuthorizeNETAIMGatewayTestCase`. Also note that several external applications are excluded from testing. Specifically, in `app_magnate/settings.py` you will see

    TEST_RUNNER = 'django_test_exclude.runners.ExcludeTestSuiteRunner'
    TEST_EXCLUDE=[ "django.contrib", "zinnia", "account", "waitinglist", "brabeion" ]
    
I am not sure why some of Zinnia's tests fail. However, it has been working totally fine, and the quality of Zinnia's codebase is exceptional, so I am not too worried about it. `Account` and `waitinglist` fail all over the place. Those apps have been modified by monkey-patching and, it looks like, were not that good in the first place. In the future those apps should be eliminated from the project, or at least the latest versions should be added in `requirements.txt`, without including edited versions in the codebase. For `brabeion` all tests pass if you run them properly. However, then you need to include a different `settings.py`, and it just makes it inconvenient to run it with the other tests. For `django_contrib` --- again, I am not sure what's wrong with them, but I assume that django works just fine, so I don't need to be testing it.


** Directories. **

This is an explanation of what each directory in `app_magnate` is for.

# account
This is an external app from pinax. It adds user accounts. It should have been just properly listed in `requirements.txt`. However, for historical reasons, there were local modifications to this package, so it was just included into the codebase as a whole. TODO: fix it. 

# billing
This is another external app called Merchant. It can be also found in PyPI. The released version had a few bugs and glitches, so we just included it and fixed the glitches in the codebase. I know should have just created a fork on github, like we did with brabeion... In fact, I have contributed a patch to the project, which was already merged, and proposed some other changes (passing more information with the signal on successful/unsuccessful transaction), which were already implemented by the maintainers of the project. TODO: take the newest version of this app from github and use it. It may be necessary to overload a couple of classes or functions to get it integrated properly, but the maintainers of the project say that this should be possible in this particular scenario. 

# companyinfo
This is a little custom django app responsible for things like "About us", "Newsletter signup", etc. 

# dashboard
This is a django app that is central to this web application. 
Important: this Magnate App is tightly integrated with the package Zinnia (django-blog-zinnia).
In the dashboard you can find the main class-based view:
    
    class DashboardView(zinnia.views.archives.EntryIndex):

This class-based view overloads the `get_queryset` function (check `dashboard/views.py`):
    return Entry.private.authorized_or_published(self.request.user)
    
Here `Entry` is a Zinnia blog entry. However, we took advantage of Zinnia's functionality allowing one to overload this Entry model. The relevant code is in the django app `glue_zinnia`. See the comments for `glue_zinnia` for more details. For now, just understand that there may be security issues here. We are implementing private messages to users (such as "You have a new donation!") as also blog entries and adding some extra functionality to NOT display other people's private entries. By default Zinnia only displays published messages, but it does not specifically attempt to hide non-published messages from being accessed in some other way.


The main template is `dashboard/templates/dashboard/dashboard_main.html`.
The essential part of this template is the place:
    <!-- Zinnia content -->
    {% block content %}
    {% endblock %}

Then, there is a very important template `dashboard/templates/zinnia/base.html`, which simply says `{% extends "dashboard/dashboard_main.html" %}`. This basically means that the dashboard is just a decorated ZInnia feed, not vice versa, as you may imagine. This allows us to leverage the full power of Zinnia, but also introduces some security issues. More details in `glue_zinnia`. 

Take a look at `dashboard/contexts.py`. Here you will find a custom context template processor allowing all pages to display information about badges, donations, etc. This is implemented as a context template processors because many of the site's pages are actually generated by Zinnia, and it is nontrivial to add this information in other ways. Again, read about `glue_zinnia` for more details.


Also take a look at `dashboard/mixins.py`. The `PrivatelyPublishedModelMixin` is used to automatically publish private Zinnia entries to the user's timeline every time there is a new donation, new badge, etc. Thus, there is no need to listen for signals or something like that: so long as your model includes the mixin, a message will be created. If you are creating a new model with this mixin, make sure to overload `create_entry_content` and the like. Especially make sure to overload `create_entry_slug` to return some unique slug prefix; otherwise things may not work.


# donations
This is also a very important app. It implements the functionality of making a donation. The user's billing address is saved with the donation amount for future reference; though, so far nothing is done with this information. 

Take a look at the model `Donation`:

    `class Donation (PrivatelyPublishedModelMixin, models.Model):`
    
The `PrivatelyPublishedModelMixin` automatically creates a private Zinnia entry for the user every time this user makes a donation (and a `Donation` model object is created). It also adds the `entry` field to the `Donation` model.

If you try to add a new donation, you are first asked for amount, then for your billing address, then finally for your credit card info. TODO: The flow is a terrible mess and should be fixed. If you look at the class `DonationBilling` in `donations/views.py`, you will see that it is a class-based view inherited from `FormView`. However, the flow of the application does not match the flow of a FormView, because we have a sequence of several forms that have to pass information, each to the next one. The last one will be submitted to Authorize.Net with direct post method, and it already has to have hash, fingerprint timestamp, etc., that it will send to Authorize.net, and in order to compute the hash we need the amount... you get the idea. Thus, it would be better to either use django's `FormWizard` or write a custom solution, perhaps relying entirely on function-based views. The URL structure is also a bit convoluted. We should either assign a different URL to each of the steps or, conversely, assign the same URL to all of them and, perhaps, pass the number of the step on each request. What happens right now is that `DonationBilling.post` explicitly calls the following view: `return donation_orderpay(request, entry)`. This makes things really complicated. For example, if the Authorize.Net transaction fails, we cannot really redirect users back to the final page where they were entering the credit card info. We could, that is, have a different URL pointing directly to the view `donations.views.donation_orderpay`, but then this function becomes used in two different ways --- directly as a function-based view and via a call from another class-based view --- and there are just too many possibilities for errors. 

The flow of Authorize.Net is as follows. The data from a user goes to Authorize.Net using the DPM (direct post method). Note that the customer's data never ever hits our servers. The user only gets the form from us, and then user's browser does a POST request directly to Authorize.Net. The request includes an `x_relay_url` (though it can also be configured in Authorize.Net's settings). After Authorize.Net verifies the fingerprint (hash and that the timestamp is not too old and not too much in the future), it does a POST request to the `x_relay_url` (while the user is waiting). Our server verifies another hash that the response came from Authorize.Net and then handles the result of a successful or failed transaction. Then our server responds to Authorize.Net with a redirect snippet that Authorize.Net then serves to the user to get him/her back to our website. This is handled by the `merchant` app (`billing/integrations/...`). On failure we are redirecting the user back to try to make the donation again (we changes the code directly in the `merchant` app); on success the user is shown a success page and can then go back to the dashboard. Note that we are passing `x_cust_id` to Authorize.Net, which it is passing back to use, so we can know, which user made the payment. 

# getstartedquestions
Not so sure if we are using it, but this is intended to be part of the Private Beta version. That is, when the registration is originally closed, the user are supposed to ask for a private invitation to register. (This is not to mention that we don't have any public registration functionality implemented). The users then fill an initial questionnaire, and I think that this is what this Django app is about.

# glue_zinnia
Here is where we do the magic to make Zinnia work with our app. In Zinnia entries can be `published`, `draft`, or `hidden`. Hidden entries are not really completely hidden as you can access them via a direct link, but we are changing it. We decide that in our app hidden Zinnia entries will be invisible to everyone except those explicitly listed as `authorized_users` for this particular entry. Then every time a user receives a messages such as "You have a new badge", a private Zinnia entry will be created for this user using the mixin from `dashboard/mixins.py`.

`glue_zinnia.models.EntryCheck` is our overloaded Zinnia `Entry` model. (Zinnia provides functionality for overloading its `Entry` model. Thus, in `settings.py` we are also setting `ZINNIA_ENTRY_BASE_MODEL='glue_zinnia.models.EntryCheck'`.) The code in `glue_zinnia/models.py` is what allows us to write things like `Entry.private.authorize_or_published(request.user)` to retrieve all entries that should be visible to a particular user. 

Now, in order to fully leverage the power of Zinnia, we did not just make a frame for it and include it as part of our template. We did the other way round. Zinnia is in the center of the dashboard, everything is structured around it. Thus the dashboard is really a customized Zinnia feed, not vice versa. This is very important to understand. You can go to any Zinnia page, such as e.g. `http://localhost:8000/blog/search/` (or whatever your url), and it will be displayed with the dashboard around it. There is a very important template `dashboard/templates/zinnia/base.html`, which simply says `{% extends "dashboard/dashboard_main.html" %}`. Since all Zinnia pages derive from this (now overloaded) `base.html`, now they all are derivated from `dashboard_main.html`. (Of course, in `settings.py`, in `INSTALLED_APPS`, `zinnia` is included after `dashboard`.)

This, however, introduces security issues. For example, if the users followed a direct link to a hidden entry, they were naturally able to view it because of how Zinnia works, even if it was not their entry. Thus, in `glue_zinnia/mixins.py` there is `HiddenEntryProtectionMixin`, solving this problem; `glue_zinnia/views.py` and `glue_zinnia/urls/entries.py` are using it.

THEORETICALLY SPEAKING, THERE MAY BE OTHER SIMILAR SECURITY ISSUES. Therefore, certain parts of Zinnia functionality can be disabled by editing `glue_zinnia/urls/__init__.py`. Just comment out the lines you don't want, such as `search`, `sitemap`, etc. 



