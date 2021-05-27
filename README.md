# Closure() #

Planning your next courses easily.

## About ##

This project is part of
the [Open Source Software Workshop](https://shnaton.huji.ac.il/index.php/NewSyl/67118/2/) at
the Hebrew University of Jerusalem.

## Getting Started ##

1. Clone this repo
2. run `python Closure_Project/manage.py migrate --run-syncdb`
3. run the django server with `python Closure_Project/manage.py runserver`

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

#### Parsing ####
to get the relevant files, run `MoonDownloader.py`. The folders `tracks` and `course_details` will be created.

Downloading will take time! (the moon website is..._fragile_)

Once you have both folders populated, run `OfflineParer.py`.
This too will take time


## Contributions ##

Feel free to PR or open issues.
