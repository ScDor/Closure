from utils import setup_django_pycharm

setup_django_pycharm()
from rest_api.models import CourseType

COURSE_TYPE_EXCEPTIONS = {  # maps course_id to a {track_id:type}
    67501: {3009: CourseType.MUST, 3010: CourseType.MUST},
    80423: {3009: CourseType.MUST, 3010: CourseType.MUST}
}
