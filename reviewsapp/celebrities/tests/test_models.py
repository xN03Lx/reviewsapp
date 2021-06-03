from django.test import TestCase
from django.contrib.auth import get_user_model

from reviewsapp.celebrities.models import Celebrity

celebrity_sample = {
    "name":"Brad Pitt",
    "biography":"""An actor and producer known as much for his
                versatility as he is for his handsome face, Golden Globe-winner
                Brad Pitt's most widely recognized role
                may be Tyler Durden in Fight Club (1999). """ ,
    "birthday": "1963-12-18",
    "place_of_birth": "Shawnee, Oklahoma, USA",
    "gender": "MALE",
    "url_image": """https://m.media-amazon.com/images/Brad_Pitt.jpg""",
    "principal_job" : "ACTOR"

}

class ModelTest(TestCase):
    def test_celebrity_str(self):
        """Test the celebrity string representation"""
        user = get_user_model().objects.create_user(
            email='user@gmail.com',
            password='test123',
            name='Test user full name'
        )
        celebrity = Celebrity.objects.create(created_by=user, **celebrity_sample)
        self.assertEqual(str(celebrity), celebrity.name)
