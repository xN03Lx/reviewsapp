from rest_framework import serializers

from .models import Celebrity

class CelebritySerializer(serializers.ModelSerializer):
    """Serializer for the celebrities object"""

    class Meta:
        model = Celebrity
        fields = (
                    "id",
                    "name",
                    "biography",
                    "birthday",
                    "place_of_birth",
                    "gender",
                    "url_image",
                    "principal_job",
                    "created_by"
        )

