from rest_api.serializers.DynamicSerializer import DynamicFieldsModelSerializer, serializers
from rest_api.models import Take, CoursePlan
from rest_api.serializers.CourseSerializer import CourseOfTrackSerializer
from rest_api.serializers.TrackSerializer import TrackSerializer

class TakeSerializer(DynamicFieldsModelSerializer):
    type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Take
        fields = ('course', 'course_plan_id', 'year_in_studies', 'semester', 'type')

class DetailTakeSerializer(TakeSerializer):
    course = CourseOfTrackSerializer(read_only=True)

    class Meta:
        model = Take
        fields = TakeSerializer.Meta.fields


class CoursePlanSerializer(DynamicFieldsModelSerializer):
    takes = TakeSerializer(many=True, source="take_set", partial=True)
    owner = serializers.ReadOnlyField(source="owner.id")
    track_name = serializers.ReadOnlyField(source="track.name")

    remaining = serializers.JSONField(read_only=True)

    class Meta:
        model = CoursePlan
        fields = ('id', 'owner', 'name', 'track', 'track_name', 'public', 'remaining', 'created_at', 'modified_at', 'takes')
        read_only_fields = ('id', 'created_at', 'modified_at')


    def create(self, validated_data):
        takes = validated_data.pop("take_set")

        plan = CoursePlan.objects.create(**validated_data)
        if takes:
            for take in takes:
                Take.objects.create(course_plan=plan, **take)
        return plan
    
    def update(self, instance, validated_data):
        takes = validated_data.pop("take_set", None)

        CoursePlan.objects.filter(id=instance.id).update(**validated_data)
        if takes:
            Take.objects.filter(course_plan=instance).delete()
            for take in takes:
                Take.objects.create(course_plan=instance, **take)
        return CoursePlan.objects.get(id=instance.id)

class DetailCoursePlanSerializer(CoursePlanSerializer):
    takes = DetailTakeSerializer(many=True, source="take_set")
    track = TrackSerializer()


    def to_representation(self, instance):
        track = self.fields["track"].get_attribute(instance)
        self.context["track_pk"] = track.id if track else None
        return super().to_representation(instance)

    class Meta:
        model = CoursePlan
        fields = CoursePlanSerializer.Meta.fields
        read_only_fields = CoursePlanSerializer.Meta.read_only_fields