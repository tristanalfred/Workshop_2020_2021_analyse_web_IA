from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from server.models import Action, Application, Element, Owner, Page, TypeAction, TypeElement, TypePage, User, Visite
from server.serializers import ActionSerializer, ApplicationSerializer, ElementSerializer, OwnerSerializer, \
    PageSerializer, TypeActionSerializer, TypeElementSerializer, TypePageSerializer, UserSerializer, VisiteSerializer, PertinenceSerializer, PertinenceSerializer2
from rest_framework.response import Response
from django.db.models import Avg


# Create your views here.
class ActionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows actions to be viewed or edited.
    """
    queryset = Action.objects.all().order_by('-id')
    serializer_class = ActionSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # print(request)
        # print(args)
        # print(kwargs)

        # print(request.data)
        # print(dict(request.data.lists())['page'][0])
        # print(request.data['element'])
        # print(dict(request.data.lists())['typepage'][0])
        # print(request.data['type_element'])


        # if Page.objects.filter(url=dict(request.data.lists())['page'][0]).count() != 0:
        if Element.objects.filter(name=request.data['element']).count() != 0:
            # print('L elemenyt existe')
            if TypeElement.objects.filter(name=request.data['type_element']).count() == 0:
                # print('Le type d element n existe pas')
                TypeElement.objects.create(name=request.data['type_element'])
            request.data['page'] = Page.objects.filter(url=request.data['page']).first().url
            request.data['element'] = Element.objects.filter(name=request.data['element']).first().id

            # print(TypeAction.objects.filter(name=request.data['typeaction']))

            request.data['typeaction'] = TypeAction.objects.filter(name=request.data['typeaction']).first().id

            # print(request.data)
            return super().create(request)
        else:
            # print('L elemenyt n existe pas encore')
            if TypeElement.objects.filter(name=request.data['type_element']).count() == 0:
                # print('Le type d element n existe pas')
                TypeElement.objects.create(name=request.data['type_element'])

            # print(request.data['type_element'])
            # print(TypeElement.objects.filter(name=request.data['type_element']).first().name)

            Element.objects.create(name=request.data['element'], type_element=TypeElement.objects.filter(name=request.data['type_element']).first())

            # id_page = int(Page.objects.filter(url=dict(request.data.lists())['page'][0]).first().id)

            request.data['action'] = request.data['action']

            request.data['page'] = Page.objects.filter(url=request.data['page']).first().url
            request.data['element'] = Element.objects.filter(name=request.data['element']).first().id
            request.data['typeaction'] = TypeAction.objects.filter(name=request.data['typeaction']).first().id
            # request.data.update({"page": id_page})

            # print(request.data)
            return super().create(request)


class ElementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows elements to be viewed or edited.
    """
    queryset = Element.objects.all().order_by('-id')
    serializer_class = ElementSerializer
    permission_classes = [permissions.AllowAny]


class TypeActionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows type actions to be viewed or edited.
    """
    queryset = TypeAction.objects.all()
    serializer_class = TypeActionSerializer
    permission_classes = [permissions.AllowAny]


class OwnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows owners to be viewed or edited.
    """
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [permissions.AllowAny]


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows applications to be viewed or edited.
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # print(request)
        # print(request.data)
        # print(dict(request.data.lists())['owner'][0])
        Owner.objects.get_or_create(name=dict(request.data.lists())['owner'][0])
        return super().create(request)


class TypeElementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows type elements to be viewed or edited.
    """
    queryset = TypeElement.objects.all().order_by('-id')
    serializer_class = TypeElementSerializer
    permission_classes = [permissions.AllowAny]


class TypePageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows type page to be viewed or edited.
    """
    queryset = TypePage.objects.all().order_by('-id')
    serializer_class = TypePageSerializer
    permission_classes = [permissions.AllowAny]


class PageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows page to be viewed or edited.
    """
    queryset = Page.objects.all().order_by('-id')
    serializer_class = PageSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class VisiteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows visites to be viewed or edited.
    """
    queryset = Visite.objects.all()
    serializer_class = VisiteSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # if Page.objects.filter(url=dict(request.data.lists())['page'][0]).count() != 0:
        if Page.objects.filter(url=request.data['page']).count() != 0:
            request.data['page'] = Page.objects.filter(url=request.data['page']).first().id

            return super().create(request)
        else:
            # print('La page n existe pas encore')
            # print(Page.objects.count())

            Page.objects.create(url=request.data['page'],
                                pge_estimated_time=request.data['estimatedTimer'][0],
                                type_page=TypePage.objects.first())  #Mettre le vrai type page)

            # print(Page.objects.count())

            # id_page = int(Page.objects.filter(url=dict(request.data.lists())['page'][0]).first().id)
            request.data['page'] = Page.objects.filter(url=request.data['page']).first().id
            # request.data.update({"page": id_page})

            return super().create(request)


class PertinenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows pertinence to be viewed or edited.
    """
    print('avant')
    queryset = Page.objects.all()
    serializer_class = PertinenceSerializer2
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        print('on appel une pertinence particulière')


        return Response(serializer.data)


class PertinentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows pertinent to be viewed or edited.
    """
    queryset = TypePage.objects.all().order_by('-id')




    serializer_class = TypePageSerializer
    permission_classes = [permissions.AllowAny]
