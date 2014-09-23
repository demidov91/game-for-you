game-for-you
============

Web-tool for distributed command game organization.

Requires:
 * One of: python3.4 python3.3 python2.6
  * zc.buildout (?)
  * libpq-dev
  * python3-dev (python-dev)
 * build-essential (make, g++)
 * pillow debian dependences
  * sudo apt-get install libtiff4-dev libjpeg8-dev zlib1g-dev \
      libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk 
 * less compiler (node.js + less)

Installation:
 * git clone **repo-url**
 * Add src/core/local_settings.py file. Add SECRET_KEY variable there, at least.
  * Create the database.
 * python bootstrap.py
 * chmod a+x test.sh
 * bin/buildout
 * Create link to the less compiler
  * chmod u+x ~/.npm/less/x.x.x/package/bin/lessc          (maybe, a+x)
  * ln -s ~/.npm/less/x.x.x/package/bin/lessc ./lessc
 * Collect application static files.
  * bin/manage collectstatic
  * ln -s ../../app_static/facebook/ src/core/media/
  * ln -s ../../app_static/admin/ src/core/media/

Running site:
 * django development server
  * bin/manage runserver --nostatic  (use --nostatic param to avoid 404 error on path clashes)

 * nginx
  * *sudo cp deployment/nginx-site /etc/nginx/sites-available/nginx-file-for-site*
  * Replace server_name, error_log, proxy_pass, root with paths and urls.
  * *sudo ln -s ../sites-available/nginx-file-for-site /etc/nginx/sites-enabled/nginx-file-for-site*
  * *sudo cp deployment/proxy_params /etc/nginx/proxy_params*
  * Restart nginx.

 * apache2
  * install apache2-(prefork|threaded)-dev
  * install or build python with option --enable-shared if you haven't done it yet
  * install or build mod_wsgi for selected python version
   * run /sbin/ldconfig if libpython...so... is not found
  * Here is complete instruction of how to fix UnicodeError on file upload. http://itekblog.com/ascii-codec-cant-encode-characters-in-position/
    It was enough to add export LANG='be_BY.UTF-8', LC_ALL *the same* in /etc/apache2/envvars

After site started:
 * Enable social authentication:
  * Create record with social application data for each provider at /admin/socialaccount/socialapp/
