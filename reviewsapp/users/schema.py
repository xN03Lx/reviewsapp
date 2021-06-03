from django.contrib.auth import logout, get_user_model
from django.conf import settings

import graphene
import graphql_jwt
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    """ User type object """

    class Meta:
        model = get_user_model()
        only_fields = [
            'id',
            'email',
            'name',
            'registered_at',
        ]


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    users = graphene.List(UserType)
    profile = graphene.Field(UserType)

    @staticmethod
    def resolve_user(cls, info, **kwargs):
        return get_user_model().objects.get(id=kwargs.get('id'))

    @staticmethod
    def resolve_users(cls, info, **kwargs):
        return get_user_model().objects.all()

    @staticmethod
    def resolve_profile(cls, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user


class Register(graphene.Mutation):
    """ Mutation to register a user """
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        name = graphene.String(required=True)

    def mutate(self, info, email, password, name):
        if get_user_model().objects.filter(email__iexact=email).exists():
            errors = ['emailAlreadyExists']
            return Register(success=False, errors=errors)

        # create user
        _user = get_user_model().objects.create(
            email=email,
            name=name,
        )
        _user.set_password(password)
        _user.save()
        return Register(success=True, user=_user)


class Logout(graphene.Mutation):
    """ Mutation to logout a user """
    success = graphene.Boolean()

    def mutate(self, info):
        logout(info.context)
        return Logout(success=True)


class Mutation(graphene.ObjectType):
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    register = Register.Field()
    logout = Logout.Field()

