# Deployment

In this file I'll describe how to deploy the project via a Linux environment(in `bash`, `zsh` or some other POSIX compatible shell), after
[setting up](https://cloud.google.com/sdk/docs/install) the `gcloud` SDK.



## Backend

### Initial configuration

1. It is assumed you followed the following [tutorial](https://cloud.google.com/python/django/run) up to(including) 
   "Preparing the backing services", without the "Cloning the Django app" step(of course, we'll use this repository instead)


2. Define some variables relating to the GCP, change them as needed and then run them in your terminal

    ```shell
    PROJECT_ID=django-closure-kb
    INSTANCE_NAME=closure-postgres
    REGION=europe-west1
    SERVICE_NAME=closure-service
    
    # The name of the Django .env secret within the 'Secret Manager'
    # currently this is hardcoded and SHOULD NOT BE CHANGED
    SETTINGS_NAME=django_settings
    ```
    
    You may also save the above settings to a `.sh` file, and simply source it (e.g `. mySettings.sh`) 
    instead of copy-pasting the above to your terminal, but you should not commit this file.
    
3. Configure an appropriate `.env` file based on the example one provided at `GIT_PROJECT_DIR/Closure_Project/.env.example`

   It can has any name, in order to not clash with `.env` that is used for local development, you could use `.env.prod`

### Uploading a new .env file

This step should be done whenever you wish to change the settings used by the Django app in production. 

```shell
gcloud secrets versions add ${SETTINGS_NAME} --data-file=PATH_TO_PROD_DOTENV_FILE
```

### Pushing, building & deploying a new container

Usually it is recommended to use a CI/CD system to automatically push builds,
but you can also do so manually - this should be done whenever you changed the back-end code, it is not necessarily
if you merely wish to change the .env.

Note that you'll also need to define a tag (via the `TAG_NAME` environment variable) which will b used to
substitute the `COMMIT_SHA` variable, which by default is set by Cloud Build for builds triggered from a git commit.


```shell
gcloud builds submit --config backend-cloudbuild.yaml \
    --substitutions _INSTANCE_NAME=${INSTANCE_NAME},_REGION=${REGION},_SERVICE_NAME=${SERVICE_NAME},COMMIT_SHA=${TAG_NAME}

```

Note that this will automatically deploy the container.

#### For the first deployment

For the first deployment, you need to define some instance setttings which weren't automatically added by the Cloud
Build script, by doing:

```shell
gcloud run deploy ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --image gcr.io/${PROJECT_ID}/${SERVICE_NAME}:${TAG_NAME} \
    --add-cloudsql-instances ${PROJECT_ID}:${REGION}:${INSTANCE_NAME} \
    --allow-unauthenticated
```

This will allow everyone to reach the API, and connect it to the database. These settings will hold
for all future deployments as well.


### Deploying a new instance of the Django service for an existing container

Sometimes you might wish to deploy an existing container, for example, in order
to make it load newer settings. 

First, set `TAG_NAME` to be the name of a tag, whether it is a tag you manually assigned(as above),
or a commit hash, or `latest` if you wish to refer to the latest container that was built. Then, run:

```shell
gcloud run deploy ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --image gcr.io/${PROJECT_ID}/${SERVICE_NAME}:${TAG_NAME}
```


## Front-end

### Initial configuration

1. It is assumed you followed the following [tutorial](https://cloud.google.com/storage/docs/hosting-static-website) for hosting static files, and managed to deploy some files to the website at least manually.


1. All production settings are located within the `Closure_Project/.env` and `Closure_Project/.env.production` files (both files are loaded, the latter overrides any options in the former), you can override them if needed but don't commit these changes.

2. Define some variables relating to the GCP, change them as needed and then run them in your terminal
    ```shell
    FRONTEND_BUCKET_NAME=uniclosure.me
    IMAGE_NAME=closure-frontend
    ```

The `FRONTEND_BUCKET_NAME` is the name of the bucket to which the site
is deployed, and `IMAGE_NAME` is the name of the container used for
building the frontend assets.


### Pushing, building & deploying a new website

This step is nearly identical to the deployment of the backend,
aside from differrent substitutions.

The recommendation to use CI/CD also applies here.

Run the following in the terminal:
```shell
gcloud builds submit --config frontend-cloudbuild.yaml \
    --substitutions _FRONTEND_BUCKET_NAME=${FRONTEND_BUCKET_NAME},_IMAGE_NAME=${IMAGE_NAME},COMMIT_SHA=${TAG_NAME}
```

This will automatically deploy the website. Note that it might take an hour for the changes to propogate due to caching within Google Cloud Storage. 