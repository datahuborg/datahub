from rest_framework import serializers

# do it without the file first, since that's testable



class DistillationSerializer(serializers.Serializer):

    training_input = serializers.CharField(trim_whitespace=False)
    training_output = serializers.CharField(trim_whitespace=False)
    record_separator = serializers.CharField(max_length=10, )
    o_fields_structure = serializers.CharField(trim_whitespace=False)
    i_structure = serializers.CharField(trim_whitespace=False)
    output = serializers.CharField(trim_whitespace=False)

    # file = serializers.FileField(
    #     max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)
