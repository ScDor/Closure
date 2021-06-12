# Closure() #

Planning your next courses easily.

## About ##

This project is part of
the [Open Source Software Workshop](https://shnaton.huji.ac.il/index.php/NewSyl/67118/2/) at
the Hebrew University of Jerusalem.

## Getting Started ##

NOTE: It's highly recommended to perform everything inside a venv.
1. Clone this repo
2. Run `python3 -m venv venv`
3. Windows users: run `venv\Scripts\activate.bat`. Mac users: run `source venv/bin/activate`. From now your commands are executed inside a virtual environment, make sure to run this command every time you want to run terminal commands related to `Closure()` again in the future 
4. Run `pip install -r requirements.txt`
5. Run `python Closure_Project/manage.py makemigrations rest_api` _(the `python` command may be redundant if it's a globally-available command on your machine)_
6. Run `python Closure_Project/manage.py migrate`
7. On PyCharm, right-click the outer `Closure_Project` directory, choose `Mark Directory as` and click `Sources Root`. _(its icon will be colored cyan afterwards)_
8. Start the django server with `python Closure_Project/manage.py runserver`

You now have a django instance with the database configured (yet blank)

The next step would be populating the database with `Course` information, so the whole ordeal
can work.

See the `Parser` folder, or read the following subsection to learn more about the data
structures used.

### Populating the DB: HUJI Parser as example ###

The Hebrew University of Jerusalem serves course information as follows:

- [Course details](http://moon.cc.huji.ac.il/nano/pages/wfrCourse.aspx?faculty=2&year=2021&courseId=67118&language=en)
  provide everything to be known regards courses: points given, teachers, course schedule etc.
- [Track data](http://moon.cc.huji.ac.il/nano/pages/wfrMaslulDetails.aspx?year=2021&faculty=2&entityId=521&chugId=521&degreeCode=71&maslulId=23010&language=en)
  shows which courses are required or available on each study-track
- [Corner-Stone courses](https://ap.huji.ac.il/%D7%A8%D7%95%D7%97-%D7%9C%D7%A4%D7%99-%D7%A7%D7%9E%D7%A4%D7%95%D7%A1%D7%99%D7%9D-%D7%A9%D7%95%D7%A0%D7%99%D7%9D/%D7%A7%D7%95%D7%A8%D7%A1-%D7%9E%D7%A7%D7%95%D7%95%D7%9F)
  are listed on the program website, only available in Hebrew. _(These are required courses in
  topics unrelated to one's study program or topic)_

Note: 
* It is important to parse courses before parsing tracks. When parsing a track, the parser validates the relevant courses already exist in the database. 
* The example parser provided in the `Parser` folder is configured to fetch and parse
information from the Hebrew versions of the said websites.

#### Downloading and parsing ####
to get the relevant files, run `MoonDownloader.py`. The folders `tracks_html` and `course_details_html` will be created.

Downloading will take time! (the moon website is..._fragile_)

Once you have both folders populated, run `OfflineParser.py`.

Parsing happens in the following order:
1. Parsing course details, parsed data is stored in `parsed_courses.json`
2. Parsing data relevant for the `Track` and `CourseGroup` objects. parsed data is stored in folders named `parsed_tracks` and `parsed_groups` as json files.
3. Loading the parsed course data as `Models.Course` objects in the Django database. 
4. Fetching CornerStone course information (course id only), and marking relevant `Course` objects as `is_corner_stone = True` (None by default)
5. Loading the parsed Track data as `Models.Track` objects in the Django database. 
6. Loading the parsed `CourseGroup` data as `Models.CourseGroup` objects in the Django database. 

The aforementioned order is important, as some objects assume existence of others (e.g. `CourseGroup` and `Course` objects).

### Generating auth ###
1. If you don't have admin superuser, creat one with `python Closure_Project/manage.py createsuperuser`
2. Use basic authentication with your username and password created, or generate token with `python Closure_Project/manage.py drf_create_token` and add `{Autharization: Token <key>}` to request headers.

### Using the API ###
- To use the API, start the server with `python Closure_Project/manage.py runserver`.

- The base API url is `https://<host>/api/v1`.
- API documentation is available in `https://<host>/redoc/`
- Try to use API with: `https://<host>/swagger/`
- When making real requests, always remember to add the Authorization header to the request.


## Contributions ##

Feel free to PR or open issues.
