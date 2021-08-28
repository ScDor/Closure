from typing import Any, Dict
import pytest
import json
import io
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from rest_api import models
from rest_api.views import CoursePlanViewSet
from rest_api.serializers.CoursePlanSerializer import CoursePlanSerializer

def create_dummy_student(username: str) -> models.Student:
    user = models.User(username=username)
    user.save()
    owner = models.Student.objects.get(user=user)
    return owner

@pytest.fixture
def courses():
    courses = [
        models.Course(course_id=1330, data_year=2015, name="Course A", semester=models.Semester.A, is_given_this_year=True, points=4),
        models.Course(course_id=1331, data_year=2015, name="Course B", semester=models.Semester.B, is_given_this_year=True, points=4),
        models.Course(course_id=1332, data_year=2015, name="Course C", semester=models.Semester.A, is_given_this_year=True, points=4),
        models.Course(course_id=1333, data_year=2015, name="Course D", semester=models.Semester.EITHER, is_given_this_year=True, points=4),
    ]
    models.Course.objects.bulk_create(courses)
    return models.Course.objects.all()



@pytest.mark.django_db
def test_courseplan_serializer(courses):
    owner = create_dummy_student("Stu A")
    # print("courses", courses)
    # print("courseplan serializer", repr(CoursePlanSerializer()))
    
    # deserialization
    course_plan = {
        "public": False,
        "takes": [
            { "course": courses[0].id, "semester": models.Semester.A.value, "year_in_studies": models.Year.FIRST.value },
            { "course": courses[1].id, "semester": models.Semester.B.value, "year_in_studies": models.Year.FIRST.value },
            { "course": courses[3].id, "semester": models.Semester.A.value, "year_in_studies": models.Year.SECOND.value }
        ]
    }

    deserializer = CoursePlanSerializer(data=course_plan)
    assert deserializer.is_valid(), f"Gotten errors: {deserializer.errors}"
    # print("deserializer validated_data", deserializer.validated_data)
    model_course_plan = deserializer.save(owner=owner)
    model_takes = model_course_plan.take_set.all()

    assert len(model_takes) == len(course_plan["takes"]), "The deserialized model object should match the data object"
    assert all(take.course_plan_id == model_course_plan.id 
               for take in model_takes), "The deserialized model object should match the data object"

    assert model_course_plan.id is not None, "Deserialized model object should have an ID"
    assert model_course_plan.owner.id == owner.id

    # print("model_takes", model_takes)

    # very simple testing of serialization
    serializer = CoursePlanSerializer(model_course_plan)
    serialization_result = serializer.data

    assert len(serialization_result["takes"]) == len(course_plan["takes"])

    # now, updating the previous instance, adding a title and changing the takes
    course_plan_2 = {
        "id": model_course_plan.id,
        "name": "now i have a name",
        "public": False,
        "takes": [
            { "course": courses[0].id, "semester": models.Semester.A.value, "year_in_studies": models.Year.FIRST.value },
            { "course": courses[2].id, "semester": models.Semester.A.value, "year_in_studies": models.Year.SECOND.value },
        ]
    }


    deserializer_2 = CoursePlanSerializer(model_course_plan, data=course_plan_2)
    assert deserializer_2.is_valid()
    model_course_plan_2 = deserializer_2.save()

    assert models.CoursePlan.objects.count() == 1
    assert models.Take.objects.count() == 2, "Old takes should have been deleted"
    assert model_course_plan_2.name == course_plan_2["name"], "should have a name now"


@pytest.fixture
def view():
    return CoursePlanViewSet.as_view(actions={'post': 'create', 'put': 'update', 'get': 'retrieve', 'patch': 'partial_update'})

@pytest.fixture
def stud1():
    return create_dummy_student("alice")

@pytest.fixture
def stud2():
    return create_dummy_student("bob")

@pytest.fixture
def stud1_plan(courses):
    return {
        "name": "a private plan",
        "public": False,
        "takes": [
            { "course": courses[0].id, "semester": models.Semester.A.value, "year_in_studies": models.Year.FIRST.value },
            { "course": courses[1].id, "semester": models.Semester.B.value, "year_in_studies": models.Year.FIRST.value },
            { "course": courses[3].id, "semester": models.Semester.A.value, "year_in_studies": models.Year.SECOND.value }
        ]
    }

@pytest.fixture
def stud2_plan(courses):
    return {
        "name": "a public plan",
        "public": True,
        "takes": [
            { "course": courses[0].id, "semester": models.Semester.A.value, "year_in_studies": models.Year.FIRST.value },
            { "course": courses[2].id, "semester": models.Semester.A.value, "year_in_studies": models.Year.SECOND.value },
        ]
    }

@pytest.fixture
def factory():
    return APIRequestFactory()


@pytest.fixture
def post_plan(factory, view):
    def _fun(plan, student: models.Student) -> Dict[Any, Any]:
        req = factory.post('/course_plans/', plan, format='json')
        force_authenticate(req, student.user)
        res = view(req)
        assert res.status_code == status.HTTP_201_CREATED, "Creating a course plan should succeed"

        res.render()
        post_result = json.load(io.BytesIO(res.content))
        assert post_result["owner"] == student.id, "The owner field should be automatically populated"
        assert post_result["owner"] == student.id, "The owner field should be automatically populated"
        return post_result

    return _fun

@pytest.mark.django_db
def test_courseplan_post(post_plan, stud1, stud1_plan):
    post_plan(stud1_plan, stud1)

@pytest.mark.django_db
def test_courseplan_partial_update(view, stud1, stud1_plan, post_plan):
    factory = APIRequestFactory()

    # post
    post_result = post_plan(stud1_plan, stud1)

    # partial update
    stud1_req2 = factory.patch('/course_plans/', { "name": "cool name"}, format='json')
    force_authenticate(stud1_req2, stud1.user)
    res2 = view(stud1_req2, pk = post_result["id"])

    assert res2.status_code == status.HTTP_200_OK, "Patching a course plan should succeed"
    res2.render()
    patch_result = json.load(io.BytesIO(res2.content))

    print("patch_result", patch_result)
    assert patch_result["name"] == "cool name", "patched name was changed"
    assert patch_result["modified_at"] > patch_result["created_at"]
    assert len(patch_result["takes"]) == len(stud1_plan["takes"]), "a patch that doesn't include takes, does not change them"






@pytest.mark.django_db
def test_courseplan_viewset_permissions(courses, view, stud1, stud2, stud1_plan, stud2_plan, post_plan):
    factory = APIRequestFactory()

    # setup, create a plan for each student
    plan1_res = post_plan(stud1_plan, stud1)
    plan2_res = post_plan(stud2_plan, stud2)
    print("res1", plan1_res)
    print("res2", plan2_res)

    # stud1 can access his own plan
    stud1_req2 = factory.get('/course_plans/')
    force_authenticate(stud1_req2, stud1.user)
    res3 = view(stud1_req2, pk=plan1_res["id"])
    assert res3.status_code == status.HTTP_200_OK

    res3.render()
    plan1_res2 = json.load(io.BytesIO(res3.content))
    assert plan1_res2 == plan1_res, "The retrieved plan is identical to the one created"

    # and also access stud2's plan, which is public
    stud1_req3 = factory.get('/course_plans/')
    force_authenticate(stud1_req3, stud1.user)
    res4 = view(stud1_req3, pk=plan2_res["id"])
    assert res4.status_code == status.HTTP_200_OK, "Student 1 can access a public plan"
    res4.render()
    res4_data = json.load(io.BytesIO(res4.content))
    assert res4_data == plan2_res, "The retrieved plan is identical to the one created"

    # which can also be accessed without being authenticated at all
    unauth_req = factory.get('/course_plans/')
    res5 = view(unauth_req, pk=plan2_res["id"])
    assert res5.status_code == status.HTTP_200_OK, "An unauthenticated user can access a public plan"
    res5.render()
    res5_data = json.load(io.BytesIO(res5.content))
    assert res5_data == plan2_res, "The retrieved plan is identical to the one created"

    # however, stud1 cannot modify stud2's plan
    stud1_modify_req = factory.patch("/course_plans/")
    force_authenticate(stud1_modify_req, stud1.user)
    modify_res = view(stud1_modify_req, pk=plan2_res["id"])
    assert modify_res.status_code == status.HTTP_403_FORBIDDEN, "A plan can only be modified by its user"

    # however, stud2 cannot access stud1's plan
    stud2_req2 = factory.get('/course_plans/')
    force_authenticate(stud2_req2, stud2.user)
    res6 = view(stud2_req2, pk=plan1_res["id"])
    assert res6.status_code == status.HTTP_404_NOT_FOUND, \
        "An authenticated user cannot access another student's private plan"

    # nor can unauthenticated users access stud1's plan
    unauth_req2 = factory.get('/course_plans/')
    res7 = view(unauth_req2, pk=plan1_res["id"])
    assert res7.status_code == status.HTTP_404_NOT_FOUND, \
        "An unauthenticated user cannot access another student's private plan"
