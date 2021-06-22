# Local Development

## Backend

### Initial configuration

1. First, create an `.env` file based on the one provided as example

   `cp GIT_PROJECT_DIR/Closure_Project/.env.example GIT_PROJECT_DIR/Closure_Project/.env`

   Alternatively, if the environment variable `ENV_PATH` is set, it will be used instead of the default `.env` path.
   (If you do so, it is recommended to use an absolute path)

2. You can modify the `DATABASE_URL` to refer to a local `sqlite` database. Note that the database path is relative to your working directory
   when executing the backend server via `python manage.py`(or a WSGI/ASGI web server), and not to the env file.

   To be consistent with the project, it is recommended you set it to `sqlite:///db.sqlite3`, and
   run the server within the `GIT_PROJECT_DIR/Closure_Project` folder, that is:

   ```shell
   cd GIT_PROJECT_DIR/Closure_Project
   python manage.py runserver
   ```

   (within a virtual environment of course)

3. Make sure  `GS_BUCKET_NAME` is commented out in order to use Django's default filesystem based static file storage, otherwise
   the cloud storage will be used, which requires deployment in order to propogate any changes.