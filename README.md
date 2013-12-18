

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

