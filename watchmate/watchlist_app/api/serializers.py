from platform import platform
from rest_framework import serializers
from watchlist_app import models

#--part-2/3 replaced movies wiht watch serializers.ModelSerializer --------------------------------


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.Review
        
        fields ="__all__"

class WatchListSerializer(serializers.ModelSerializer):
    #to add extra fields inside
    platform= serializers.CharField(source='platform.name')
    reviews = ReviewSerializer(many=True,read_only=True)
    # len_name = serializers.SerializerMethodField()

    class Meta:
        model=models.WatchList
        fields="__all__"
        #if you want to exclude
        # exclude =['active']
    
    def get_len_name(self,object):
        length = len(object.title)
        return length

    def validate(self, data):
        if data['title']==data['description']:
            raise serializers.ValidationError('Title and description cannot be same')
        else:
            return data

    def validate_name(self,value):
        if len(value)<2:
            raise serializers.ValidationError('Name is too short!!')
        else:
            return value

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many = True,read_only = True)
    # watchlist = serializers.StringRelatedField(many=True)
    # watchlist=serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # watchlist=serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='movie_details')
    class Meta:
        model=models.StreamPlatform
        fields= "__all__"






#---Part 1 serializer.Serializer --------------------------------

# def name_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError('Name is too short!..')

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name=serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active= serializers.BooleanField()

#     def create(self,validated_data):
#         return models.Movie.objects.create(**validated_data)

#     def update(self,instance,validated_data):
#         instance.name = validated_data.get('name',instance.name)
#         instance.description = validated_data.get('description',instance.description)
#         instance.active= validated_data.get('active',instance.active)
#         instance.save()
#         return instance
#     def validate(self,data):
#         if data['name']==data['description']:
#             raise serializers.ValidationError("Title and Description should be different")
#         else:
#             return data


    # def validate_name(self,value):

    #     if len(value)<2:
    #         raise serializers.ValidationError('Name is too short')
    #     else:
    #         return value
# print('serializers 85')