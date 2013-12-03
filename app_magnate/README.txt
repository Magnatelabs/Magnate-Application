
IF I WERE TO GO FORWARD WITH MY SOLUTION OF ENTRY vs. AUTHORIZED ENTRY then
write unit tests
be really sure that authorized entries do not show up as regular entries.

Admin is screwed...


alternatively, try to set get_queryset on the Entry to make it only return some entries by deafult?....well, the version with authorized_entry seems more reliable. But does django guarantee that if we subclass the same abstract model twice, we get independent tables?

Then make sure that dashboard actually displays my secred authorized entries but that they cannot be seen by e.g. a direct link...


0.SECURITY HOLE 
Can see private entries via direct link, e.g. http://localhost:8000/blog/2013/12/02/private-sergey/

What can be done?
- Add another check to the template, and not display if an item is hidden and we are not permitted to view it. Return 404.
(Change _entry_detail.html for a start and/or _entry_detail_base.html)
- Remove some URLs and write our own Handlers, not Zinnia's, for other Zinnia views.

- Add some Middleware?
Not just "login required" everything.


Also before of previous/next entry functionality.?!?!?!

1. Fix Likes. They are not thread safe. They are also not really working. We have lots of objects in SQL, but the logic is broken. Likes by different people do not add up.
2. Add rating the website. Also create a template tag in the social app. Also update it with Ajax.
3. Add badges. Look how it is done in Brabeion. We should have a BadgeType class that could be extended to particular badge types and decorated with @register_badge. Then every model Badge will have a certain type set. Also every Badge will have a user. For every badge type we will be able to check if a given user qualifies (e.g. if he has enough likes). We will also be able to check if a given user has been awarded a badge (even if he does not qualify any more) and if the user has received the award (meaning a Zinnia entry was created, for example). Use transactions when the user receives an award.

Each badge type also has a nae, e.g. PASSIONARY.

4. The panel displaying all user's badges should be smarter. Perhaps use also a template tag to display all the badges; then we can use badges to reload it once the user gets something new. Note that there may also be a new post in Zinnia, but it is trickier to reload it with Ajax.

Each badge picture could be a link to a Zinnia post about this badge, if it has been awarded to this user.

5. Some interesting badges:
- donation>0
- likes>2
- a badge for which you qualify with 1% probability (lucky streak)
- admin's favor: you never qualify, but admin may award it, and then you'll just receive it.
- certain number of comments

6. For each badge there is a picture. Where do we write the text for a Zinnia post notifying you about a new badge?..

7. Add login_required middleware.

8. Compute title Automatically from badges ("Meme Magnate")?

9. For the badge panel, display only K badges by default, and add a See All? What would See All do? Show/hide (toggle) other hidden badges?


10. POST to Zinnia on every donation and on every badge award!!!
