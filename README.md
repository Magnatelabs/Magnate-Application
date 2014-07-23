
 
[ ![Codeship Status for Magnatelabs/Magnate-Application](https://www.codeship.io/projects/b5c76750-e9f2-0131-b97c-5a04e3162754/status)](https://www.codeship.io/projects/26265)

# Testing 

Be sure to run the tests with `python manage.py test`. They MUST PASS. Exception: if you are not connected to Internet, you get 2 failures in the merchant app in `billing.tests.AuthorizeNETAIMGatewayTestCase`. Also note that several external applications are excluded from testing. Specifically, in `app_magnate/settings.py` you will see

    TEST_RUNNER = 'django_test_exclude.runners.ExcludeTestSuiteRunner'
    TEST_EXCLUDE=[ "django.contrib", "zinnia", "account", "waitinglist", "brabeion" ]
    
I am not sure why some of Zinnia's tests fail. However, it has been working totally fine, and the quality of Zinnia's codebase is exceptional, so I am not too worried about it. `Account` and `waitinglist` fail all over the place. Those apps have been modified by monkey-patching and, it looks like, were not that good in the first place. In the future those apps should be eliminated from the project, or at least the latest versions should be added in `requirements.txt`, without including edited versions in the codebase. For `brabeion` all tests pass if you run them properly. However, then you need to include a different `settings.py`, and it just makes it inconvenient to run it with the other tests. For `django_contrib` --- again, I am not sure what's wrong with them, but I assume that django works just fine, so I don't need to be testing it.

# requirements.txt 
Some comments:
We are using Django 1.5. Something was deprected somewhere, so it doesn't work with Django 1.6; you would probably need to update one of the packages. 
`PIL` is used for displaying the picture on the profile. For some reason, `Pillow` is not enough for that; make sure you are installing `PIL` properly. To install PIL on a Mac, install Macports from http://www.macports.org/install.php, and then `sudo port install libpng`; `sudo port install jpeg`; `pip install PIL`. To install PIL on Ubuntu, read `http://obroll.com/install-python-pil-python-image-library-on-ubuntu-11-10-oneiric/`. Basically, `sudo pip uninstall PIL`,  `sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev`, `sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib`, `sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib`, `sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib`, `sudo pip install -U PIL`.


For `brabeion`, we are using a modified version in the github fork, as you can see. I haven't sent a pull request. 

# Directories. 
This is an explanation of what each directory in `app_magnate` is for.


## account
This is an external app from pinax. It adds user accounts. It should have been just properly listed in `requirements.txt`. However, for historical reasons, there were local modifications to this package, so it was just included into the codebase as a whole. TODO: fix it. 

## app_magnate
This is the project dir.
* Very important file: `app_magnate/static/js/receive_updates.js`. It includes javascript code that regularly polls the server for updates so that every time you are awarded a badge, you will see a messagebox, and then the badges will be updated with ajax. It also receives updates about new articles, but those are not used. The backend view is in `dashboard/views.py`, called `receive_updates_api`. (Note that in `pinax_theme_bootstrap/templates/theme_bootstrap/base.html` we are setting `$.ajaxSetup({ cache: false });`.) The way it works is by timestamp. It polls the server with the timestamp of the last update and receives whatever happened after that, if anything. I am not 100% if I implemented the logic 100% correctly: if the user uses the Back button, I think sometimes the same update can be shown multiple times. I wasn't able to reproduce it properly, though. I experimented with it a bit, but didn't have enough time to figure it out. The problem may have to do with the way I am storing `last_ts` (last timestamp for which the update was received); it is also in this `receive_updates.js`. Not sure what happens to javascript variables when you are using the Back button in the browser.

Now, it is not really necessary to poll the server regularly. You can just take the function `receive_updates` from the same file and call it after the user likes an entry (see `dashboard/templates/dashboard/dashboard_main.html`) or receives a star rating (see `social/templates/social_star_rating.html`; was not sure where best to put all this code...). Then, you can also call it on the donation success page in `app_magnate/templates/billing/authorize_net_success.html` (it should really be in `donations/templates/billing/`). I just thought polling might be useful for some future functionality.

* the hook for things to be executed on startup is in `app_magnate/startup.py`. 
* there are some legacy functions in `app_magnate/receivers.py` doing something with login/logout that I never even looked at. Not sure if they are used or not. 
* the star rating jquery plugin is in `app_magnate/static/fyneworks_star_rating`.


## billing
This is another external app called Merchant. It can be also found in PyPI. The released version had a few bugs and glitches, so we just included it and fixed the glitches in the codebase. I know should have just created a fork on github, like we did with brabeion... In fact, I have contributed a patch to the project, which was already merged, and proposed some other changes (passing more information with the signal on successful/unsuccessful transaction), which were already implemented by the maintainers of the project. TODO: take the newest version of this app from github and use it. It may be necessary to overload a couple of classes or functions to get it integrated properly, but the maintainers of the project say that this should be possible in this particular scenario. 

## companyinfo
This is a little custom django app responsible for things like "About us", "Newsletter signup", etc. 

## dashboard
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


## donations
This is also a very important app. It implements the functionality of making a donation. The user's billing address is saved with the donation amount for future reference; though, so far nothing is done with this information. 

Take a look at the model `Donation`:

    `class Donation (PrivatelyPublishedModelMixin, models.Model):`
    
The `PrivatelyPublishedModelMixin` automatically creates a private Zinnia entry for the user every time this user makes a donation (and a `Donation` model object is created). It also adds the `entry` field to the `Donation` model.

If you try to add a new donation, you are first asked for amount, then for your billing address, then finally for your credit card info. TODO: The flow is a terrible mess and should be fixed. If you look at the class `DonationBilling` in `donations/views.py`, you will see that it is a class-based view inherited from `FormView`. However, the flow of the application does not match the flow of a FormView, because we have a sequence of several forms that have to pass information, each to the next one. The last one will be submitted to Authorize.Net with direct post method, and it already has to have hash, fingerprint timestamp, etc., that it will send to Authorize.net, and in order to compute the hash we need the amount... you get the idea. Thus, it would be better to either use django's `FormWizard` or write a custom solution, perhaps relying entirely on function-based views. The URL structure is also a bit convoluted. We should either assign a different URL to each of the steps or, conversely, assign the same URL to all of them and, perhaps, pass the number of the step on each request. What happens right now is that `DonationBilling.post` explicitly calls the following view: `return donation_orderpay(request, entry)`. This makes things really complicated. For example, if the Authorize.Net transaction fails, we cannot really redirect users back to the final page where they were entering the credit card info. We could, that is, have a different URL pointing directly to the view `donations.views.donation_orderpay`, but then this function becomes used in two different ways --- directly as a function-based view and via a call from another class-based view --- and there are just too many possibilities for errors. 

The flow of Authorize.Net is as follows. The data from a user goes to Authorize.Net using the DPM (direct post method). Note that the customer's data never ever hits our servers. The user only gets the form from us, and then user's browser does a POST request directly to Authorize.Net. The request includes an `x_relay_url` (though it can also be configured in Authorize.Net's settings). After Authorize.Net verifies the fingerprint (hash and that the timestamp is not too old and not too much in the future), it does a POST request to the `x_relay_url` (while the user is waiting). Our server verifies another hash that the response came from Authorize.Net and then handles the result of a successful or failed transaction. Then our server responds to Authorize.Net with a redirect snippet that Authorize.Net then serves to the user to get him/her back to our website. This is handled by the `merchant` app (`billing/integrations/...`). On failure we are redirecting the user back to try to make the donation again (we changes the code directly in the `merchant` app); on success the user is shown a success page and can then go back to the dashboard. Note that we are passing `x_cust_id` to Authorize.Net, which it is passing back to use, so we can know, which user made the payment. 

## getstartedquestions
Not so sure if we are using it, but this is intended to be part of the Private Beta version. That is, when the registration is originally closed, the user are supposed to ask for a private invitation to register. (This is not to mention that we don't have any public registration functionality implemented). The users then fill an initial questionnaire, and I think that this is what this Django app is about.

## glue_zinnia
Here is where we do the magic to make Zinnia work with our app. In Zinnia entries can be `published`, `draft`, or `hidden`. Hidden entries are not really completely hidden as you can access them via a direct link, but we are changing it. We decide that in our app hidden Zinnia entries will be invisible to everyone except those explicitly listed as `authorized_users` for this particular entry. Then every time a user receives a messages such as "You have a new badge", a private Zinnia entry will be created for this user using the mixin from `dashboard/mixins.py`.

`glue_zinnia.models.EntryCheck` is our overloaded Zinnia `Entry` model. (Zinnia provides functionality for overloading its `Entry` model. Thus, in `settings.py` we are also setting `ZINNIA_ENTRY_BASE_MODEL='glue_zinnia.models.EntryCheck'`.) The code in `glue_zinnia/models.py` is what allows us to write things like `Entry.private.authorize_or_published(request.user)` to retrieve all entries that should be visible to a particular user. 

Now, in order to fully leverage the power of Zinnia, we did not just make a frame for it and include it as part of our template. We did the other way round. Zinnia is in the center of the dashboard, everything is structured around it. Thus the dashboard is really a customized Zinnia feed, not vice versa. This is very important to understand. You can go to any Zinnia page, such as e.g. `http://localhost:8000/blog/search/` (or whatever your url), and it will be displayed with the dashboard around it. There is a very important template `dashboard/templates/zinnia/base.html`, which simply says `{% extends "dashboard/dashboard_main.html" %}`. Since all Zinnia pages derive from this (now overloaded) `base.html`, now they all are derivated from `dashboard_main.html`. (Of course, in `settings.py`, in `INSTALLED_APPS`, `zinnia` is included after `dashboard`.)

This, however, introduces security issues. For example, if the users followed a direct link to a hidden entry, they were naturally able to view it because of how Zinnia works, even if it was not their entry. Thus, in `glue_zinnia/mixins.py` there is `HiddenEntryProtectionMixin`, solving this problem; `glue_zinnia/views.py` and `glue_zinnia/urls/entries.py` are using it.

THEORETICALLY SPEAKING, THERE MAY BE OTHER SIMILAR SECURITY ISSUES. Therefore, certain parts of Zinnia functionality can be disabled by editing `glue_zinnia/urls/__init__.py`. Just comment out the lines you don't want, such as `search`, `sitemap`, etc. 


## pinax_theme_bootstrap
This is really just a set of templates from pinax for starting a new django app. I am not sure if it should be included in the project or if it should be properly installed from `requirements.txt` with the templates overloaded. Anyway, for historical reasons it is here, included in the project. The most interesting file here is `pinax_theme_bootstrap/templates/theme_bootstrap/base.html`. This is where we include jQuery and most of the other javascript libraries and display a Magnate logo, among other things. Consider renaming this file into `dashboard/templates/theme_bootstrap/base.html` or `app_magnate/templates/theme_bootstrap/base.html`. Obivously, just make sure that the apps in `INSTALLED_APPS` in `settings.py` are in the right order: whatever is overloading goes first, whatever is overloaded goes second.

## siteErrors
A little django app for returning 404 and 500 errors and the "coming soon" page.

## social
This django app implements the functionality so users can "like" articles and give a star rating to the website. Check out `social/models.py` and perhaps `social/tests.py`. A particular user can like any particular (public) Zinnia entry. The `Like` model includes `count`, but it is really only `0` or `1`. The rating so far is for the entire website. It can be changed to include a generic foreign key to an arbitrary model; in this case you would probably use the `site.Site` object for rating the entire website. Also note that rating can be done only as often as specified by the variable `settings.MAGNATE_CAN_RATE_STAR_EVERY`. It can be equal to e.g. `hours=3`, `days=6`, etc. Whatever you can pass to `datetime.timedelta(...)`. The times in the database for both the ratings and the likes are probably UTC, if I am correct; at least, it should be so. (There is a unittest for the ratings making sure that the time when you can/cannot rate is counted properly). 

Also, `social/views.py` contains the views for handling ajax requests to like an entry and to give a star rating. Both of them return JSON. Because our "Likes" widget also shows the total number of likes, `ajax_like_entry` also returns the html that should be put in place of the current "Likes" widget so this count could be updated. `ajax_star_rating`, on the other hand, just returns a message to be displayed in place of the stars. In theory, the message "You have already voted in the recent past" should never be displayed because, if the user has recently voted, the stars should not be displayed in the first place. However, it may happen if the user uses the back button in the browser. (The user could also try to submit a rating directly by using some tool such as `curl`; however, this should not be possible because of CSRF protection. Both the likes and the star rating are protected by CSRF protection middleware included in `settings.py`.)

There are also two custom template tags in `social/templatetags/social_tags.py`: `like_entry_button` (which really should be called `render_like_entry_button`) and `render_star_rating`. The `like_entry_button` is used in `dashboard/templates/zinnia/_entry_detail.html`. In the file, `object` is `EntryCheck`, an overloaded Zinnia entry defined in `glue_zinnia/models.py`. `render_star_rating` is used in `dashboard/templates/dashboard/dashboard_main.html`. 

## spotlight
Legacy folder; will be removed.

## status_awards
This django app implements badges awarded to users. (Note that we are using an external app called `brabeion` that implements the core of the badges functionality). As soon as you import `status_awards`, `status_awards/__init__.py` gets executed and imports either `status_awards/magnate_badges.py` or `status_awards/test_badges.py`. Each of those file registers all the badge types to be used in production or in test, respectively. Note also the function `award_badge(event, user)` also defined in `status_awards.__init__.py`. It checks if this particular user should be awarded any badges on this event; events are strings. For now, our awarding mechanism is very conservative. We are not, for example, trying to award badges on server startup or on timer. Instead, we assume that at every moment all badges have been awarded correctly. When something happens (e.g. a user likes an entry) that may trigger an award, we check for awards for particular affected user(s), and only for those badges, which award may be triggered by a particular event that happened.  In the unlikely event that a server crashes while awarding a badge some badges may end up being unawarded until another qualifying event. Same may happen if some information in the SQL database was edited manually. Thus, consider at least adding a function trying to award all badges to all users on application startup (assuming that we won't have millions of users --- then it would make more sense to do such checks on user login or logout, or something like that). A hook for code to be executed on startup is in `app_magnate/startup.py`. 

I have edited the `brabeion` package by creating a fork on github. As you may notice in `requirements.txt`, this is where it is coming from. The change was to add the same functionality as in Zinnia: the ability to overload their `BadgeAward` with our custom model. This is exactly what we are doing in `status_awards/models.py`. One thing we are doing is also using the `PrivatelyPublishedModelMixin`, so there is a new Zinnia entry also created for each newly awarded badge. Another one is adding the concept of metabadges.

Metabages are awards given for other awards. They are not displayed as ordinary badges but as "statuses". For example, you may get badges for making donations, liking items, rating the website, and then you get promoted to a new status such as "Meme Magnate". Only one status (=metabadge) is displayed at all times: basically, the latest one. This allows us to create a nonlines hierarchy where users can "grow" in different directions. Some users can be "into" making donations :-), while others may be "into" liking things, much like in certain role-playing games you may be able to practice your sword skills and improve as a warrior or practice your healing skills and imporve as a cleric. The hierarchy of badges and metabadges is a completely arbitrary directed acyclic graph with badges as the leaves (out-degree zero) and metabadges as the inner vertices. 

You will see in `dashboard/templates/dashboard/__user_badges.html` that to display ordinary badges, we use `{{ badges | no_metabadges }}`. Also note the `magnate_status_badge` function in `dashboard/contexts.py`: it picks the latest metabadge to be displayed as user's status.

There is also a custom template tag in `status_awards/templatetags/status_awards_tags.py` called `render_badge(badge, size)`. Its job is to display the badge as a picture which is also a hyperlink to the page with more information about this particular badge. Right now it is a bit stupid because it is using the size for resizing the picture, which could arguably be better done with CSS. However, this design allows you to potentially use different files for badges of different sizes, which may be better (so we don't send a huge badge file over the network just to resize it to a small icon). This design should similarly allow you to send all badge icons as side-by-side sprites in one image file and then display them appropriately. 

If you want to change the structure of the badges, edit `status_awards/magnate_badges.py`. Before you start changing everything, make sure you understand the `brabeion` package well enough and, in particular, the distinction between `Badge`, representing the type of an award, and `BadgeAward`, a django model representing a particular award. BadgeAwards are stored in the database, whereas Badges are not. Also note that particular types of badges are identified by a pair `(slug, level)`, such as `('likes', 2)`. The levels are usually `0`-indexed; however the `brabeion` package has an inconsistency here. When you are implementing the function `award`, you have to add `1` to the level, and to return e.g. `BadgeAwarded(1)` to give a badge of level 1. Also you should always set `multiple = False`, as we have not considered awarding the same badge multiple times and, thus, have not tested this feature at all.  Lastly, if you are implementing your own Metabadge, you should always set `events` to the same thing, and they should always be defined after `requirements`. Namely, `events = ['badge_awarded_'+s for s in set(s for s_l in requirements for s in s_l.keys())]`. This means that this particular badge could be triggered by awards of badges that it depends on. (We do not have a general event `badge_awarded`, though, it could be easily added. This could be handy for checking badge awards on application startup). Note that metabadge awards are handled automatically in `status_awards/__init__.py`, in `on_badge_awarded`, so you do not need to call anything to recompute metabadges. You do need to call something to recompute ordinary badges, though. You can see in `social/views.py` the calls to `status_awards.award_badges`; this is where the work is done. If you decide to change the mechanism by which the badges are awarded by e.g. creating signals for things like "user liked an entry" and then registering a general badge awarder to listen to all those signals, be sure to change the unittests in `status_awards/tests.py`. 



## waitinglist
This is a pinax app for the "private beta" functionality. Users interested in the website before general registration is open are joining a "waiting list". Not sure how well it works, but it was used in the previous Magnate project that our codebase is based on.
