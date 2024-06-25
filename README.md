# ofd-backend

#### Install Requirements
~~~
python3.7 -m venv venv
~~~
~~~
source venv/bin/activate
~~~
~~~
sh scripts/install_requirements.sh
~~~

#### Important Commands
* Remove __pycache__ files from project
 ~~~ 
git rm --cached */__pycache__/
~~~

#### Important Links
~~~
https://erdplus.com/create-account
~~~
Draw polygon on map to get location boundry
~~~
http://apps.headwallphotonics.com/
~~~
~~~
https://geojson.io/#map=2/20.0/0.0 (recommended)
~~~
Install GDL on MAC OS
~~~
https://gist.github.com/kelvinn/f14f0fc24445a7994368f984c3e37724
~~~

#### Important Points
~~~
manage.py is development server
~~~

~~~
wsgi.py is production server
~~~

## Errors Solution
django.db.migrations.exceptions.CircularDependencyError
~~~
1. comment foreign keys from all models 
2. make migrations and migrate
3. uncomment foreign keys 
4. make migrations => set default value for foreign keys (e.g 1)
5. migrate updated migrations
~~~
