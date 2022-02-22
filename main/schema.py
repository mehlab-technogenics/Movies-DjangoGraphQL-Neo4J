import graphene
from graphene_django import DjangoObjectType

from .models import Movie, Person
import neomodel

from graphene_django import DjangoObjectType
import graphene


from graphene import ObjectType, String,Int,ID,UUID,Field


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
        list_result=fog.acted.all()
        for each_point in list_result:
            output.append(
               PersonType( name=each_point.name, born=each_point.born,)
            )
        list_result=fog.wrote.all()
        for each_point in list_result:
            output.append(
               PersonType( name=each_point.name, born=each_point.born)
            )
        list_result=fog.produced.all()
        for each_point in list_result:
            output.append(
               PersonType( name=each_point.name, born=each_point.born)
            )
        list_result=fog.directed.all()
        for each_point in list_result:
            output.append(
               PersonType( name=each_point.name, born=each_point.born)
            )
        list_result=fog.reviewed.all()
        for each_point in list_result:
            output.append(
               PersonType( name=each_point.name, born=each_point.born)
            )
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
    def resolve_find_like_movieD(root, info, id):
        # Querying a list
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
###############################------Mutation-----############################################



# class UpdateCategory(graphene.Mutation):
#     class Arguments:
#         # Mutation to update a category 
#         title = graphene.String(required=True)
#         id = graphene.ID()


#     category = graphene.Field(CategoryType)

#     @classmethod
#     def mutate(cls, root, info, title, id):
#         category = Category.objects.get(pk=id)
#         category.title = title
#         category.save()
        
#         return UpdateCategory(category=category)


class PersonInput(graphene.InputObjectType):
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

# class BookInput(graphene.InputObjectType):
#     title = graphene.String()
#     author = graphene.String()
#     pages = graphene.Int()
#     price = graphene.Int()
#     quantity = graphene.Int()
#     description = graphene.String()
#     status = graphene.String()

# class CreateBook(graphene.Mutation):
#     class Arguments:
#         input = BookInput(required=True)

#     book = graphene.Field(BookType)
    
#     @classmethod
#     def mutate(cls, root, info, input):
#         book = Book()
#         book.title = input.title
#         book.author = input.author
#         book.pages = input.pages
#         book.price = input.price
#         book.quantity = input.quantity
#         book.description = input.description
#         book.status = input.status
#         book.save()
#         return CreateBook(book=book)

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
    movie = graphene.Field(MovieType)
    
    @classmethod
    def mutate(cls, root, info, input):
        
        movie = Movie.nodes.get(title=input.title)
        movie.title = input.title
        movie.released = input.released
        movie.tagline=input.tagline
        movie.save()
        return UpdateMovie(movie=movie)

class Mutation(graphene.ObjectType):
    #update_category = UpdateCategory.Field()
    create_person = CreatePerson.Field()
    create_movie = CreateMovie.Field()
    update_person = UpdatePerson.Field()
    update_movie = UpdateMovie.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
