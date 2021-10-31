import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Project


class ProjectNode(DjangoObjectType):
    class Meta:
        model = Project
        filter_fields = {'name': ['iexact', 'icontains']}
        interfaces = (relay.Node,)


class ProjectMutation(relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)

    project = graphene.Field(Project)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        project_name = input.name
        project = Project.objects.create(name=name)


class Query(ObjectType):
    project = relay.Node.Field(ProjectNode)
    all_projects = DjangoFilterConnectionField(ProjectNode)
