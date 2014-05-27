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

After site started:
 * Enable social authentication:
  * Create record with social application data for each provider at /admin/socialaccount/socialapp/
