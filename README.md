game-for-you
============

Web-tool for distributed command game organization.

Requires:
 * python3.3
  * zc.buildout

Installation:
 * git clone **repo-url**
 * buildout init 
 * bin/buildout
 * Collect application static files.
  * uncomment **'django.contrib.staticfiles',** line in settings.py
  * bin/manage collectstatic
