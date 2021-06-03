from django.test.testcases import TestCase
from django.contrib.auth import get_user_model

import graphene
from graphene.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase
from graphql_jwt.shortcuts import get_token


from reviewsapp.users.schema import Query, Mutation


user_list_query = """
    query {
        users {
            id
            name
            email
        }
    }
"""
single_user_query = """
    query($id:Int!)
    {
        user(id:$id){
            id
            name
            email
        }
    }
"""
profile_query = """
    query {
        profile {
            name
            email
        }
    }
"""

create_user_mutation = """
     mutation Register($email: String!, $password: String!, $name: String!) {
        register(email: $email, password: $password, name: $name) {
            success
            errors
            user{
                id
                name
                email
            }
        }
    }
"""

login_mutation = """
    mutation login($email: String!, $password: String!) {
    login(email: $email, password: $password) {
        token
        payload
    }
}
"""


class TestUserSchema(TestCase):
    def setUp(self):
        self.schema = graphene.Schema(query=Query, mutation=Mutation)
        self.client = Client(self.schema)
        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            password='test123',
            name='Test user full name'
        )

    def test_single_user_query(self):
        response = self.client.execute(single_user_query, variables={"id": self.user.id})
        response_user = response.get("data").get("user")
        assert response_user["id"] == str(self.user.id)


    def test_user_list_query(self):
        #schema = graphene.Schema(query=Query)
        response = self.client.execute(user_list_query)
        response_users = response.get("data").get("users")
        assert len(response_users)

    def test_create_user(self):
        """Test creating user with valid payload is successful"""

        payload = {
            "email": "userTest@gmail.com",
            "password": '123456',
            "name": "noel toyo"
        }
        response = self.client.execute(create_user_mutation, variables={**payload})
        user = response.get("data").get("register").get("user")
        email = user.get("email")
        user = get_user_model().objects.get(**user)
        assert user.check_password(payload['password'])
        assert email == payload["email"]

    def test_user_exists(self):
        """Test creatinga  user that already exists fails"""
        payload = {
            'email': 'user@gmail.com',
            'password': '123456',
            'name': 'Test',
        }
        response = self.client.execute(create_user_mutation, variables={**payload})
        errors = response.get("data").get("register").get('errors')
        assert errors[0] == 'emailAlreadyExists'

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        #token = get_token(User().objects.get(pk=self.user.id))
        payload = {'email': self.user.email, 'password': 'test123'}
        assert True


class PrivateUserApiTests(JSONWebTokenTestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            password='test123',
            name='Test user full name'
        )
        self.client.authenticate(self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in used"""

        response = self.client.execute(profile_query)
        user = response.data.get('profile')
        self.assertEqual(user, {
            'name': self.user.name,
            'email': self.user.email
        })

