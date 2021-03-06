### Structure & Sources ###
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

### Downloading the data ###
To download the course files, run `Parser/MoonDownloader.py` (make sure venv is activated!). The folders `tracks_html` and `course_details_html` will be created.

Downloading will take time! (the moon website is..._fragile_)

#### Parsing the data ####
Once you have both folders populated, run `Parser/OfflineParser.py`.

Parsing happens in the following order:
1. Parsing course details, parsed data is stored in `parsed_courses.json`
2. Parsing data relevant for the `Track` and `CourseGroup` objects. parsed data is stored in folders named `parsed_tracks` and `parsed_groups` as json files.
3. Loading the parsed course data as `Models.Course` objects in the Django database. 
4. Fetching CornerStone course information (course id only), and marking relevant `Course` objects as `is_corner_stone = True` (None by default)
5. Loading the parsed Track data as `Models.Track` objects in the Django database. 
6. Loading the parsed `CourseGroup` data as `Models.CourseGroup` objects in the Django database. 

The aforementioned order is important, as some objects assume existence of others (e.g. `CourseGroup` and `Course` objects).

