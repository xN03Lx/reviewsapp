from datetime import datetime

from django.test.testcases import TestCase
from django.contrib.auth import get_user_model

import graphene
from graphene.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase
from graphql_jwt.shortcuts import get_token


from reviewsapp.celebrities.models import Celebrity
from reviewsapp.celebrities.schema import Query, Mutation



#from users.schema import schema

celebrity_list_query = """
    query {
        celebrities {
            id
            name
            biography
            birthday
            placeOfBirth
            gender
            urlImage
            principalJob
        }
    }
"""
single_celebrity_query = """
    query($id:Int!)
    {
        celebrity(id:$id){
            id
            name
            biography
            birthday
            placeOfBirth
            gender
            urlImage
            principalJob
        }
    }
"""

create_celebrity_mutation = """
mutation createCelebrity($name: String!, $biography: String!, $birthday: Date!, $placeOfBirth: String!, $gender: String!,$urlImage: String!, $principalJob: String!) {
    createCelebrity(name: $name, biography: $biography, birthday: $birthday, placeOfBirth: $placeOfBirth, gender: $gender, urlImage: $urlImage, principalJob: $principalJob) {
        status
        message
    		celebrity {
    		  id
          name
          biography
          birthday
          placeOfBirth
          gender
          urlImage
          principalJob
    		}
    }
}
"""



def sample_celebrity(user):
    celebrity_sample_data = {
        "name":"Brad Pitt",
        "biography":"""An actor and producer known as much for his
                    versatility as he is for his handsome face, Golden Globe-winner
                    Brad Pitt's most widely recognized role
                    may be Tyler Durden in Fight Club (1999). """ ,
        "birthday": "1963-12-18",
        "place_of_birth": "Shawnee, Oklahoma, USA",
        "gender": "MALE",
        "url_image": """https://m.media-amazon.com/images/Brad_Pitt.jpg""",
        "principal_job": "ACTOR",
        "created_by": user
    }
    return Celebrity.objects.create(**celebrity_sample_data)


class PublicCelebrityApiTest(TestCase):
    def setUp(self):
        self.schema = graphene.Schema(query=Query)
        self.client = Client(self.schema)
        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            password='test123',
            name='Test user full name'
        )
        self.celebrity = sample_celebrity(self.user)

    def test_single_celebrity_query(self):
        response = self.client.execute(single_celebrity_query, variables={"id": self.celebrity.id})
        response_celebrity = response.get("data").get("celebrity")
        assert response_celebrity["id"] == str(self.celebrity.id)

    def test_user_celebrity_query(self):
        #schema = graphene.Schema(query=Query)
        response = self.client.execute(celebrity_list_query)
        response_celebrities = response.get("data").get("celebrities")
        assert len(response_celebrities)


class PrivateCelebrityApiTests(JSONWebTokenTestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            password='test123',
            name='Test user full name'
        )
        self.client.authenticate(self.user)

    def test_create_celebrity(self):
        payload = {
            "name":"Brad Pitt",
            "biography":"""An actor and producer known as much for his
                        versatility as he is for his handsome face, Golden Globe-winner
                        Brad Pitt's most widely recognized role
                        may be Tyler Durden in Fight Club (1999). """ ,
            "birthday": "1963-12-18",
            "placeOfBirth": "Shawnee, Oklahoma, USA",
            "gender": "male",
            "urlImage": """https://m.media-amazon.com/images/Brad_Pitt.jpg""",
            "principalJob": "actor"
        }
        payload['biography'] = payload['biography'].strip('\n')
        response = self.client.execute(create_celebrity_mutation, payload)
        self.assertEqual(response.data['createCelebrity']['status'], 200)
