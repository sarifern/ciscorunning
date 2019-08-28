# Cisco Running

Repo for Web APP Cisco Running

# Installation in MAC

0. Install VSCode and VSCode python plugin.

1. Clone the project.

2. Set up your git global config

``` 
git config --global user.name "<Your name>"     
git config --global user.email "<Your email>"
``` 

3. Edit your hostnames file and add the following

``` 
#in /etc/hosts
#add

127.0.0.1         www.lurifern.com
``` 

4. Install PostgreSQL 

``` 
brew install postgresql
``` 

4.1 Add the path out of 

``` 
which pg_config
``` 
to your PATH declaration in your shell profile (for example ~/.bash_profile)

``` 
export PATH=$PATH:/usr/local/bin/pg_config
``` 
5. Install Xcode tools

``` 
xcode-select --install
``` 

6. Create a virtual environment for Python 3.7.3.

``` 
python3.7 -m virtualenv env
``` 
7. install the packages

``` 
env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2
pip install -r requirements.txt
``` 

8. Please add the .secrets and local-settings.py files. Ask for them to the admins lurifern@cisco.com
Set .secrets at the parent folder, and local-settings.py under the ic_marathon_site folder

8.1 Execute

``` 
export $(grep -v '^#' .secrets | xargs)
``` 

9. Make the DB migrations

``` 
python manage.py migrate --settings=ic_marathon_site.local_settings
``` 

10. Create a superuser

``` 
python manage.py createsuperuser --settings=ic_marathon_site.local_settings
```  

# Running the project locally

In VSCode, you can use the debugging option, as the .vscode/launch.json has the right runserver arguments.
Manually, the command would be

``` 
python manage.py runsslserver --settings=ic_marathon_site.local_settings
``` 

# Heroku deployment

Make sure you have the Heroku CLI tool.

https://devcenter.heroku.com/articles/heroku-cli

Login to heroku with the HEROKU_ADMIN and HEROKU_PASSWORD variables

``` 
heroku login
``` 

To set environment variables, use the heroku config command

``` 
heroku config:set <variable name>=############ -a ciscorunning
``` 

Since the app is already configured in Heroku (ciscorunning), there is no further configuration.

Once the changes are committed and push to the repo, Heroku will automatically build the new app and deploy it.