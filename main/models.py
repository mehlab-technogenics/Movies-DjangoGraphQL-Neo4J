

# Create your models here.
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo,RelationshipFrom)


# class Movie(StructuredNode):
#     pass


class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique=True)
    born = IntegerProperty()

    #traverse outgoing IS_FROM relations, inflate to Country objects
    wrote = RelationshipTo('Movie', 'WROTE')
    directed = RelationshipTo('Movie', 'DIRECTED')
    acted=RelationshipTo('Movie','ACTED_IN')
    reviewed=RelationshipTo('Movie', 'REVIEWED')
    produced = RelationshipTo('Movie', 'PRODUCED')


class Movie(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(required=True)
    tagline=StringProperty()
    released=IntegerProperty()


    wrote = RelationshipFrom(Person, 'WROTE')
    directed = RelationshipFrom(Person, 'DIRECTED')
    acted=RelationshipFrom(Person,'ACTED_IN')
    reviewed=RelationshipFrom(Person, 'REVIEWED')
    produced = RelationshipFrom(Person, 'PRODUCED')
    