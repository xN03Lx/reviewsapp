from django.conf import settings

import graphene
from graphene_django.debug import DjangoDebug

from reviewsapp.users.schema import Query as UserQuery, Mutation as UserMutation
from reviewsapp.celebrities.schema import Query as CelebrityQuery, Mutation as CelebrityMutation


class Query(UserQuery, CelebrityQuery, graphene.ObjectType):
     if settings.DEBUG:
         # Debug output - see
         # http://docs.graphene-python.org/projects/django/en/latest/debug/
        debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(UserMutation, CelebrityMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
