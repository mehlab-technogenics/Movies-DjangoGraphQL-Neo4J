from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import requests
from .models import Person,Movie
import neomodel 
from neomodel import match,Traversal

def home(request):
    #jim = Person(name='Juleaa', born=2020).save() # Create
    #fogjim.save() # Update, (with validation)
    #fog=Movie(title='Fog',tagline='Me Hon NA').save()
    jim = Person.nodes.get(name='Emil Eifrem')
    fog = Movie.nodes.get(title='The Matrix')
    # for p in fog.inhabitant.all():
    #     print(p.name)
    #Z = neomodel.db.cypher_query("MATCH (m:Movie)-[]-(p:Person) RETURN *", resolve_objects=True)
    # definition = dict(node_class=Person, direction=match.OUTGOING,
    #               relation_type=None, model=None)
    # relations_traversal = neomodel.match.Traversal(jim, Movie.__label__,
    #                             definition)
    # all_jims_relations = relations_traversal.all()
    # print(all_jims_relations)
    #print(fog.id)
    context=[jim]
    #print(context)
    #print('mehlab', context['history'][i.id])
    #fog.acted.is_connected(jim)
    definition = dict(node_class=Movie, direction=match.OUTGOING,
    relation_type=None, model=None)
    relations_traversal = Traversal(fog, Movie.__label__,
    definition)
    all_jims_relations = relations_traversal.all()
    return HttpResponse( all_jims_relations)