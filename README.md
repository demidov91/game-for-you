game-for-you
============

Web-tool for distributed command game organization.

Requires:
 * One of: python3.4 python3.3 python2.6
  * zc.buildout

Installation:
 * git clone **repo-url**
 * Add src/core/local_settings.py file. Add SECRET_KEY variable there, at least.
  * Create the database.
 * python bootstrap.py
 * chmod a+x test.sh
 * bin/buildout
 * Collect application static files.
  * uncomment **'django.contrib.staticfiles',** line in settings.py
  * bin/manage collectstatic
