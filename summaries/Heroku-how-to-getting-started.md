
# How Heroku works + Getting started on Heroku with Python

## How Heroku works
[source](https://devcenter.heroku.com/articles/how-heroku-works)

### Defining an application
- Applications consist of your source code, a description of any dependencies and a [Procfile](https://devcenter.heroku.com/articles/procfile) (mechanism for declaring what commands are run by your applications dynos on Heroku platform).
- Dependency mechanisms vary according to language: in Ruby you use a `Gemfile`, in Python a `requirements.txt`, in Node.js a `package.json`, in Java a `pom.xml` etc.
- Each line of a Procfile declares a [process type](https://devcenter.heroku.com/articles/process-model) - a named command that can be executed against your built application.

### Deploying applications
- Heroku platform uses Git as the primary means for deploying applications.
- When you create an application on Heroku, it associates a new Git remote named `heroku`. To deploy the code, you just use `$ git push heroku master`.
- Other means to deploy: Github integration, Dropbox sync, Heroku API.

### Building applications
- Build mechanism: retrieve the specified dependencies and create any necessary assets.
- [Buildpacks](https://devcenter.heroku.com/articles/buildpacks) lie behind the slug compilation process. Buildpacks take your application, its dependencies, and the language runtime, and produce slugs.
- The source code of your application, together with the fetched dependencies and output of the build phase such as generated assets or compiled code, as well as the language and framework, are assembled into a [slug](https://devcenter.heroku.com/articles/slug-compiler).
- A slug is a bundle of your source, fetched dependencies, the language runtime, and compiled/generated output of the build system - ready for execution.

### Running applications on dynos
- [Dynos](https://devcenter.heroku.com/articles/dynos) are isolated, virtualized Unix containers, that provide the environment required to run an application.
- Heroku executes applications by running a command you specified in the Procfile, on a dyno that's been preloaded with your prepared slug.
- When you deploy a new version of your application, all the currently executing dynos are killed, and new ones are started to replace them.

### Config vars
- An application configuration is everything that is likely to vary between environments (staging, production, developer environments etc) - credentials, for example.
- The configuration for an application is stored in [config vars](https://devcenter.heroku.com/articles/config-vars).
- Config vars contain customizable data that can be changed independently of your source code.
- At runtime, all of the config vars are exposed as environment variables.

### Releases
- Every time you deploy a new version of an application, a new slug is created and release is generated.
- Heroku contains a store of the previous releases.
- [Releases](https://devcenter.heroku.com/articles/releases) are an append-only ledger of slugs, config vars and add-ons.

### Dyno manager
- The [dyno manager](https://devcenter.heroku.com/articles/dynos) is responsible for managing dynos across all applications running on Heroku.
- [One-off dynos](https://devcenter.heroku.com/articles/one-off-dynos) are temporary dynos that can run with their input/output attached to your local terminal, and they are loaded with your latest release.
- Each dyne gets its own ephemeral filesystem, with a fresh copy of the most recent released.
- Applications that use the free dyne type will sleep after 30 minutes of inactivity.

### Add-ons
- Provided services by Heroku and third-parties, such as databases, queueing & caching systems, storage, email services etc.
- [Add-ons](https://devcenter.heroku.com/articles/add-ons) are third party, specialized, value-added cloud services that can be easily attached to an application, extending its functionality.

### Logging and monitoring
- Heroku treats logs as streams of time-stamped events, and collates the stream of logs produced from all processes running in all dynos, and the Heroku platform platform components, into the Logplex.
- [Logplex](https://devcenter.heroku.com/articles/logplex) keeps a limited buffer of log entries.

### HTTP routing
- The dynos that run process types named `web` will receive HTTP traffic. Heroku's [HTTP routers](https://devcenter.heroku.com/articles/http-routing) distribute incoming requests for your application across your running web dynos.

## Getting started on Heroku for Python
[source](https://devcenter.heroku.com/articles/getting-started-with-python#next-steps)

- Assumptions: Heroku account; Python 3.6, Pipenv and Postgres installed locally.
- Setup: download Heroku CLI and, on shell, type `$ heroku login`.
- Prepare the app: clone `python-getting-started` repo
- Inside the repo folder, type `$ heroku create`, that will create the app itself and a git remote called `heroku`.
- To deploy, type `$ git push heroku master` on terminal (inside app/repo folder).
- Ensure at least one instance is running with `$ heroku ps:scale web=1`.
- Visit the app at the URL generated typing `$ heroku open` on terminal.
- View information about your running app using `heroku logs --tail`.
- Define a Procfile to explicitly declare what command should be executed to start your app.
- You can check how many dynos are running using `$ heroku ps`.
- Free accounts support one dyno. To use more dynos, upgrade to another type of account and scale using  `$ heroku ps:scale web=#` where # is the number of dynos you want to use.
- Heroku recognizes an app as a Python app by the existence of a `Pipfile` or `requirements.txt` file in the root directory.
- The `Pipfile` file lists the app dependencies together with their versions.
- To install app dependencies locally, use Pipenv to create a virtualenv and install your dependencies:
	```
	$ pipenv --three
	$ pipenv install
	``` 
	- then, activate the virtualenv
	`$ pipenv shell`
- Django uses local assets, so you'll need to run `$ python manage.py collectstatic` on the terminal.
- Run `$ heroku local web` to run the app locally.
- Open [http://localhost:5000](http://localhost:5000) with your web browser to see it running locally.
- **Push local changes**
	- Install `requests` locally:
	```
	$ pipenv install requests
	```
	- modify what you want to on your source code, and then test locally:
	```
	$ heroku local
	```
	- To push the changes, add the files modified with `$ git add`, commit the changes with `$ git commit` and deploy using `$ git push heroku master`.
	- Check if it's working using `$ heroku open`.
- Provision add-ons with `$ heroku addons:create NAME OF ADD ON`
- Check which add-ons you have with `$ heroku addons`
- Open any given add-on with `$ heroku addons:open NAME OF THE ADD ON`
- You can run a command, typically scripts and applications that are part of your app, in a one-off dyne using `heroku run` command.
- You can create another one-off dyne and run the `bash` using `$ heroku run bash`.
- You can define an environment variable, let's say `TIMES`, that will be a config variable. If you use it inside your code, you can set the value with `$ heroku config:set TIMES=2` and in runtime Heroku will use this value in your application.
- View the config vars with `$ heroku config`.
- **Provision a database**
	- Heroku provides a `pg` command; use `$ heroku pg`.
	- The example app you deployed already has database functionality, and you're able to reach visiting your app URL and appending `/db`.
	- In this example, you have to type first `$ heroku run python manage.py migrate` to create the tables.
	- Then, access the `/db` route again.
	- Use the `heroku pg:psql` command to connect to the remote database.