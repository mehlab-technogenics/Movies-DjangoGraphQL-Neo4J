
import graphene
from graphene_django import DjangoObjectType
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Person
import neomodel
import graphql_jwt
from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required

from graphene import ObjectType, String,Int,ID,UUID,Field
from django.contrib.auth import get_user_model


from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

# class MovieType(DjangoObjectType):
#     class Meta: 
#         model = Movie
#         fields = ('id','title','tagline','released')

class MovieType(ObjectType):
    title = String()
    tagline = String()
    id=ID()
    uid=UUID()
    released=Int()

class ConnectionType(ObjectType):
    name = String()
    title = String()
    def __init__(self, name=None,title=None):   
        self.name = name
        self.title = title
    def __init__(self, temp):   
        print('Hello World')
        print(temp,'Hello')
        self.name = temp['name']
        self.title = temp['title'] 
class PersonType(ObjectType):
    id=ID()
    uid=UUID()
    name=String()
    born=Int()
    #role=graphene.List(String)
    role=graphene.Field(graphene.List(String), temp=graphene.String(required=False))
    def resolve_role(parent, info,temp=None):
        print('Temp',temp)
        output = [] # output to return
        fog = Person.nodes.get(name=parent.name)
        if(temp==None):
            print('None')
            list_result=fog.acted.all()
            if(len(list_result)>0):
                output.append('ACTED_IN')
            list_result=fog.wrote.all()
            if(len(list_result)>0):
                output.append('WROTE')
            list_result=fog.directed.all()
            if(len(list_result)>0):
                output.append('DIRECTED')
            list_result=fog.reviewed.all()
            if(len(list_result)>0):
                output.append('REVIEWED')
            list_result=fog.produced.all()
            if(len(list_result)>0):
                output.append('PRODUCED')
            return output
        else:
            print('Temp')
            jim = Movie.nodes.get(title=temp)
            list_result=fog.acted.is_connected(jim)
            if(list_result):
                output.append('ACTED_IN')
            list_result=fog.wrote.is_connected(jim)
            if(list_result):
                output.append('WROTE')
            list_result=fog.directed.is_connected(jim)
            if(list_result):
                output.append('DIRECTED')
            list_result=fog.reviewed.is_connected(jim)
            if(list_result):
                output.append('REVIEWED')
            list_result=fog.produced.is_connected(jim)
            if(list_result):
                output.append('PRODUCED')
            return output

class MovieDType(ObjectType):
    title = String()
    tagline = String()
    id=ID()
    uid=UUID()
    released=Int()
    actors=graphene.List(PersonType)
    def resolve_actors(parent, info):
        output = [] # output to return
        
        fog = Movie.nodes.get(title=parent.title)
        d={}
        list_result=fog.acted.all()

        for each_point in list_result:
            if(d.get(each_point.name)==None):
                output.append(
                PersonType( name=each_point.name, born=each_point.born,)
                )
                d[each_point.name]=True
        list_result=fog.wrote.all()
        for each_point in list_result:
            if(d.get(each_point.name)==None):
                output.append(
                PersonType( name=each_point.name, born=each_point.born)
                )
                d[each_point.name]=True
        list_result=fog.produced.all()
        for each_point in list_result:
            if(d.get(each_point.name)==None):
                output.append(
                PersonType( name=each_point.name, born=each_point.born)
                )
                d[each_point.name]=True
        list_result=fog.directed.all()
        for each_point in list_result:
            if(d.get(each_point.name)==None):
                output.append(
                PersonType( name=each_point.name, born=each_point.born)
                )
                d[each_point.name]=True
        list_result=fog.reviewed.all()
        
        for each_point in list_result:
            if(d.get(each_point.name)==None):
                output.append(
                PersonType( name=each_point.name, born=each_point.born)
                )
                d[each_point.name]=True
        return output
        
    def resolve_role(parent, info):
        fog = Movie.nodes.get(title=parent.title)
        list_result=fog.acted.all()

class Query(graphene.ObjectType):
    movies = graphene.List(MovieType)
    moviesD = graphene.List(MovieDType)
    persons = graphene.List(PersonType)
    find_movie=graphene.Field(MovieType, id=graphene.String(required=True))
    find_movieD=graphene.Field(MovieDType, id=graphene.String(required=True))
    find_like_movieD=graphene.Field(graphene.List(MovieDType), id=graphene.String(required=True))
    
    find_person=graphene.Field(PersonType, id=graphene.String(required=True))

    #category_by_name = graphene.Field(PersonType, name=graphene.String())
    viewer = graphene.Field(UserType, token=graphene.String(required=True))

    @login_required
    def resolve_viewer(self, info, **kwargs):
        return info.context.user

    def resolve_movies(root, info, **kwargs):
        # Querying a list
        return Movie.nodes.all()
    def resolve_moviesD(root, info, **kwargs):
        # Querying a list
        # DB Query Logic
        list_result=Movie.nodes.all()
        print('Hi',list_result[0].title)
        output = []
        for each_point in list_result:
            output.append(
                MovieDType(
                    title=each_point.title, 
                    tagline=each_point.tagline, 
                    released=each_point.released
                )
            )
        return output

    def resolve_persons(root, info, **kwargs):
        # Querying a list
        return Person.nodes.all()


    @login_required
    def resolve_find_person(root, info, id):
        # Querying a list
        jim = Person.nodes.get(name=id)
        return jim

        
    def resolve_find_movie(root, info, id):
        # Querying a list
        jim = Movie.nodes.get(title=id)
        return jim

    def resolve_find_movieD(root, info, id):
        # Querying a list
        list_result=Movie.nodes.get(title=id)
        output = MovieDType(
                    title=list_result.title, 
                    tagline=list_result.tagline, 
                    released=list_result.released
                )
        return output

    #@login_required
    def resolve_find_like_movieD(root, info, id):
        # Querying a list
        print('root')
        print(info.context.headers)
        user = info.context.user
        print(user)
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        print('Root')
        print(info)
        list_result=Movie.nodes.filter(title__icontains=id)
        output = []
        for each_point in list_result:
            output.append(
                MovieDType(
                    title=each_point.title, 
                    tagline=each_point.tagline, 
                    released=each_point.released
                )
            )
        return output



class PersonInput(graphene.InputObjectType):
    uid=graphene.String()
    name = graphene.String()
    born = graphene.Int()



class CreatePerson(graphene.Mutation):
    class Arguments:
        input = PersonInput(required=True)

    # Class attributes define the response of the mutation
    person = graphene.Field(PersonType)

    @classmethod
    def mutate(cls, root, info, input):
        jim=Person(name=input.name, born=input.born).save()
        jim = Person.nodes.get(name=input.name)
        
        return CreatePerson(person=jim)

class ConnectionInput(graphene.InputObjectType):
    uid=graphene.String()
    name = graphene.String()
    title = graphene.String()
    ctype= graphene.String()

    


class CreateConnection(graphene.Mutation):
    class Arguments:
        input = ConnectionInput(required=True)

    # Class attributes define the response of the mutation
    connection = graphene.Field(ConnectionType)

    @classmethod
    def mutate(cls, root, info, input):
        print('Hello')
        print(input)
        jim = Person.nodes.get(name=input.name)
        fog=Movie.nodes.get(title=input.title)         
        if(input.ctype=='acted'):
            print('acted')
            print(jim.acted.connect(fog))
        elif(input.ctype=='produced'):
            print(jim.produced.connect(fog))
            print('produced')
        elif(input.ctype=='wrote'):
            print('acted')
            jim.wrote.connect(fog)
        elif(input.ctype=='directed'):
            print('acted')
            jim.directed.connect(fog)
        else:
            pass
        output={'name':jim.name,'title':fog.title}
        return CreateConnection(connection=ConnectionType(output))

class MovieInput(graphene.InputObjectType):
    uid=graphene.String()
    title = graphene.String()
    released = graphene.Int()
    tagline = graphene.String()



class CreateMovie(graphene.Mutation):
    class Arguments:
        input = MovieInput(required=True)

    # Class attributes define the response of the mutation
    movie = graphene.Field(MovieType)

    @classmethod
    def mutate(cls, root, info, input):
        jim1=Movie(title=input.title, released=input.released,tagline=input.tagline).save()
        jim = Movie.nodes.get(title=input.title)
        
        return CreateMovie(movie=jim1)


class UpdatePerson(graphene.Mutation):
    class Arguments:
        input = PersonInput(required=True)
    person = graphene.Field(PersonType)
    
    @classmethod
    def mutate(cls, root, info, input):
        
        person = Person.nodes.get(name=input.name)
        person.name = input.name
        person.born = input.born
        person.save()
        return UpdatePerson(person=person)

class UpdateMovie(graphene.Mutation):
    class Arguments:
        input = MovieInput(required=True)
        actors=graphene.List(PersonInput)
        directors=graphene.List(PersonInput,required=False)
        producers=graphene.List(PersonInput,required=False)
        writers=graphene.List(PersonInput,required=False)
    movie = graphene.Field(MovieType)
    
    @classmethod
    def mutate(cls, root, info, input,actors,directors,producers,writers):
        print(info.context.headers)
        user = info.context.user
        print(user)
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        movie = Movie.nodes.get(title=input.title)
        print (input)
        print(actors)
        movie.title = input.title
        movie.released = input.released
        movie.tagline=input.tagline
        movie.save()
        for actor in actors:
            try:
                person=Person.nodes.get(name=actor.name)
                person.acted.connect(movie)
            except:
                raise Exception("Please create person with Actor name first")
        for actor in producers:
            try:
                person=Person.nodes.get(name=actor.name)
                person.produced.connect(movie)
            except:
                raise Exception("Please create person with Producer name first")
        for actor in writers:
            try:
                person=Person.nodes.get(name=actor.name)
                person.wrote.connect(movie)
            except:
                raise Exception("Please create person with Writer name first")
        for actor in directors:
            try:
                person=Person.nodes.get(name=actor.name)
                person.directed.connect(movie)
            except:
                raise Exception("Please create person with Director name first")

        print(movie)
        return UpdateMovie(movie=movie)

class Mutation(graphene.ObjectType):
    #update_category = UpdateCategory.Field()
    create_person = CreatePerson.Field()
    create_movie = CreateMovie.Field()
    create_connection = CreateConnection.Field()
    update_person = UpdatePerson.Field()
    update_movie = UpdateMovie.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
