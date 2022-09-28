""" View module for handling request about trophies """
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from JSGame_api.models import Trophy, Asset

class TrophySerializer(serializers.ModelSerializer):
    """ JSON serializer for trophies """
    
    class Meta:
        model = Trophy
        fields = (
            'id',
            'type',
            'asset'
        )
        depth = 2

class TrophyView(ViewSet):
    """ JSGame trophies view """
    
    # def update(self, request, pk):
    #     """Handle PUT requests for a game
    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """

    #     save = Save.objects.get(pk=pk)
    #     save.score = request.data["score"]
    #     save.level = request.data["level"]
    #     save.lives = request.data["lives"]
    #     save.game_over = request.data["game_over"]
    #     save.save()

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def create(self, request):
        """ Handle POST operations 
        
        Returns
            Response -- JSON serialized trophy instance
        """
        asset = Asset.objects.get(pk=request.data["asset"])
        
        trophy = Trophy.objects.create(
            type = request.data["type"],
            asset = asset,
        )
        
        serializer = TrophySerializer(trophy)
        return Response(serializer.data)
    
    def list(self, request):
        """Handle GET requests to get all trophies
        Returns:
            Response -- JSON serialized list of trophies
        """
        trophies = Trophy.objects.all()

        serializer = TrophySerializer(trophies, many=True)
        return Response(serializer.data)
    
    # def destroy(self, request, pk):
    #     """Handle DELETE request for a game
    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     save = Save.objects.get(pk=pk)
    #     save.delete()
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)