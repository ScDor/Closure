# Deployment

In this file I'll describe how to deploy the project via a Linux environment(in `bash`, `zsh` or some other POSIX compatible shell), after
[setting up](https://cloud.google.com/sdk/docs/install) the `gcloud` SDK.



## Backend

### Initial configuration

1. It is assumed you followed the following [tutorial](https://cloud.google.com/python/django/run) up to(including) 
   "Preparing the backing services", without the "Cloning the Django app" step(of course, we'll use this repository instead)


2. Define some variables relating to the GCP, change them as needed and then run them in your terminal

    ```shell
    PROJECT_ID=django-closure
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

### Pushing & Building a new container

This step should be done whenever the backend code has changed, it is not necessary if you simply wish to update the settings.

```shell
cd GIT_PROJECT_ROOT_FOLDER/Closure_Project
gcloud builds submit --config cloudmigrate.yaml \
    --substitutions _INSTANCE_NAME=${INSTANCE_NAME},_REGION=${REGION},_SERVICE_NAME=${SERVICE_NAME}
```

### Deploying a new instance of the Django service

For the first deployment, after having done the above steps, do:
```shell
gcloud run deploy ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --image gcr.io/${PROJECT_ID}/${SERVICE_NAME} \
    --add-cloudsql-instances ${PROJECT_ID}:${REGION}:${INSTANCE_NAME} \
    --allow-unauthenticated
```

For the new deployments (whether because you pushed a new container, or
just changed the settings and want to re-deploy the current instance), do:

```shell
gcloud run deploy ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --image gcr.io/${PROJECT_ID}/${SERVICE_NAME}
```