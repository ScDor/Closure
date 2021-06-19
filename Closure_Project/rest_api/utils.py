from .models import Course, Track, CourseType
import json
import jwt
import requests
from django.contrib.auth import authenticate

from project_settings.settings import API_IDENTIFIER, AUTH0_DOMAIN


def get_course_type(track: Track, course: Course) -> CourseType:
    if course.is_corner_stone:
        return CourseType.CORNER_STONE

    cg_set = track.coursegroup_set
    matching_cg = cg_set.filter(courses__id=course.id).all()
    types = {cg.course_type for cg in matching_cg}
    for course_type in [CourseType.MUST, CourseType.FROM_LIST, CourseType.CHOICE]:
        if course_type in types:
            return course_type

    return CourseType.SUPPLEMENTARY


def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format(AUTH0_DOMAIN)).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = 'https://{}/'.format(AUTH0_DOMAIN)
    return jwt.decode(token, public_key, audience=API_IDENTIFIER, issuer=issuer, algorithms=['RS256'])