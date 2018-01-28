# How Heroku works + Getting started on Heroku with Python
[How](https://devcenter.heroku.com/articles/how-heroku-works) and [Getting started](https://devcenter.heroku.com/articles/getting-started-with-python#next-steps)
### Defining an application
- Applications consist of your source code, a description of any dependencies and a [Procfile](https://devcenter.heroku.com/articles/procfile) (mechanism for declaring what commands are run by your applications dynos on Heroku platform).
- Dependency mechanisms vary according to language: in Ruby you use a `Gemfile`, in Python a `requirements.txt`, in Node.js a `package.json`, in Java a `pom.xml` etc.
- Each line of a Procfile declares a [process type](https://devcenter.heroku.com/articles/process-model) - a named command that can be executed against your built application.

### Deploying applications
- Heroku platform uses Git as the primary means for deploying applications.
- When you create an application on Heroku, it associates a new Git remote named `heroku`. To deploy the code, you just use `git push heroku master`.
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

### 
