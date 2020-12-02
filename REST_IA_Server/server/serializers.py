from rest_framework import serializers
from .models import Action, Application, Element, Owner, Page, TypeAction, TypeElement, TypePage, User, Visite
import numpy as np
import pandas as pd
import pickle
from django.db.models import Avg


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    # owner = serializers.StringRelatedField()
    # owner = serializers.PrimaryKeyRelatedField(read_only='True')
    # owner = serializers.StringRelatedField()
    class Meta:
        model = Application
        fields = '__all__'


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'


class TypeActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeAction
        fields = '__all__'


class TypeElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeElement
        fields = '__all__'


class TypePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePage
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class VisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visite
        fields = '__all__'


class PertinenceSerializer(serializers.ModelSerializer):
    page = PageSerializer(read_only=True)
    pertinence = serializers.SerializerMethodField('calcul_pertinence')

    def calcul_pertinence(self, foo):
        # load the model from disk
        loaded_model = pickle.load(open("finalized_model.sav", 'rb'))

        app_id = 1
        pge_name = foo.page.url
        vst_time = foo.time
        pge_estimated_time = foo.page.pge_estimated_time
        pge_type_id = foo.page.type_page.id

        features = [
            'app_id',
            'vst_time',
            'pge_estimated_time',
            'pge_type_id'
        ]

        my_array = np.array([[app_id, pge_name, vst_time, pge_estimated_time, pge_type_id]])

        my_data_frame = pd.DataFrame(my_array, columns=['app_id', 'pge_name', 'vst_time', 'pge_estimated_time', 'pge_type_id'])

        my_data_frame['pertinence_computed'] = loaded_model.predict(my_data_frame[features])

        return my_data_frame['pertinence_computed'][0]

    class Meta:
        model = Visite
        fields = ('page', 'pertinence', 'time')


class PertinenceSerializer2(serializers.ModelSerializer):
    pertinence = serializers.SerializerMethodField('calcul_pertinence')

    def calcul_pertinence(self, foo):
        # load the model from disk
        loaded_model = pickle.load(open("finalized_model.sav", 'rb'))

        if(Visite.objects.filter(page=foo.id)):
            app_id = 1
            pge_name = foo.url
            vst_time = Visite.objects.filter(page=foo.id).aggregate(Avg('time'))['time__avg']
            pge_estimated_time = foo.pge_estimated_time
            pge_type_id = foo.type_page.id

            # print('____________')
            # print(app_id)
            # print(pge_name)
            # print(vst_time)
            # print(pge_estimated_time)
            # print(pge_type_id)

            features = [
                'app_id',
                'vst_time',
                'pge_estimated_time',
                'pge_type_id'
            ]

            my_array = np.array([[app_id, pge_name, vst_time, pge_estimated_time, pge_type_id]])

            my_data_frame = pd.DataFrame(my_array,
                                         columns=['app_id', 'pge_name', 'vst_time', 'pge_estimated_time', 'pge_type_id'])

            my_data_frame['pertinence_computed'] = loaded_model.predict(my_data_frame[features])

            return my_data_frame['pertinence_computed'][0]
        return 1

    class Meta:
        model = Page
        fields = ('id', 'pertinence')
