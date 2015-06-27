# gaefrx

This is very much work in progress.

Setup
-----

* Make sure that the environment variable `GOOGLE_APPENGINE` points to the SDK.
* The following environment variables should be defined in the file app/secrets.yaml. Use the file 'secrets.yaml.template' as starting point.

Tests
-----

Use the `test_runner` bash script.

Dev Server
----------

Use the bash script `dev_runner`.

Dependencies
------------

* Javascript tooling
  * Node.js
  * npm
  * gulp
  * bower
* Python 2.7+
* Nose


Uploading to Google AppEngine
-----------------------------

* cd gaefrx/app
* appcfg.py update app.yaml frontend/frontend.yaml api/api.yaml
* appcfg.py update_dispatch .
