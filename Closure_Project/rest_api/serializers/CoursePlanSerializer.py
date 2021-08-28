from rest_api.serializers.DynamicSerializer import DynamicFieldsModelSerializer, serializers
from rest_api.models import Take, CoursePlan


class TakeSerializer(DynamicFieldsModelSerializer):
    type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Take
        fields = ('course', 'course_plan_id', 'year_in_studies', 'semester', 'type')

class CoursePlanSerializer(DynamicFieldsModelSerializer):
    takes = TakeSerializer(many=True, source="take_set", partial=True)
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = CoursePlan
        fields = ('id', 'owner', 'name', 'public', 'created_at', 'modified_at', 'takes')
        read_only_fields = ('id', 'owner', 'created_at', 'modified_at')


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