import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from graphene.types.scalars import Scalar
from graphql_jwt.decorators import login_required


from .models import Celebrity
from .serializers import CelebritySerializer

class CelebrityType(DjangoObjectType):
    """ Celebrity type object """

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
                    "principal_job"
        )


class Query(graphene.ObjectType):
    celebrities = graphene.List(CelebrityType)
    celebrity = graphene.Field(CelebrityType, id=graphene.Int(required=True))


    @staticmethod
    def resolve_celebrities(cls, info):
        """Resolver to get all celebrities"""
        return Celebrity.objects.all()

    # Resolver for post field
    @staticmethod
    def resolve_celebrity(cls, info, **kwargs):
        """Resolver to get a celebrity by id"""
        return Celebrity.objects.get(id=kwargs.get('id'))



class CelebrityInput(graphene.InputObjectType):
    id = graphene.ID()

class ObjectField(Scalar):
    @staticmethod
    def serialize(dt):
        return dt


class CelebrityType(DjangoObjectType):
    class Meta:
        model= Celebrity


class CreateCelebrity(graphene.Mutation):
    celebrity=graphene.Field(CelebrityType)
    message=ObjectField()
    status=graphene.Int()

    class Arguments:
        name = graphene.String(required=True)
        biography = graphene.String(required=True)
        birthday = graphene.Date(required=True)
        place_of_birth = graphene.String(required=True)
        gender = graphene.String(required=True)
        url_image = graphene.String(required=True)
        principal_job = graphene.String(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        kwargs['created_by'] = user.id
        serializer=CelebritySerializer(data=kwargs)
        if serializer.is_valid():
            obj=serializer.save()
            msg='success'
        else:
            msg=serializer.errors
            obj=None
        return cls(celebrity=obj,message=msg,status=200)


class Mutation(graphene.ObjectType):
    create_celebrity = CreateCelebrity.Field()
