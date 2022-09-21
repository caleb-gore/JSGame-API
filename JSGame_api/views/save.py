""" View module for handling request about games """
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from JSGame_api.models import Save, Trophy

class SaveSerializer(serializers.ModelSerializer):
    """ JSON serializer for games """
    
    class Meta:
        model = Save
        fields = (
            'id',
            'score',
            'level',
            'date_created',
            'last_saved',
            'player',
            'lives',
            'game_over',
            'awarded_trophies'
        )

class SaveView(ViewSet):
    """ JSGame games view """
    
    def update(self, request, pk):
        """Handle PUT requests for a game
        Returns:
            Response -- Empty body with 204 status code
        """

        save = Save.objects.get(pk=pk)
        save.score = request.data["score"]
        save.level = request.data["level"]
        save.lives = request.data["lives"]
        save.game_over = request.data["game_over"]
        save.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def retrieve(self, request, pk):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game
        """
        try:
            save = Save.objects.get(pk=pk)
            serializer = SaveSerializer(save)
            return Response(serializer.data)
        except Save.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        """ Handle POST operations 
        
        Returns
            Response -- JSON serialized game instance
        """
        
        
        save = Save.objects.create(
            score = request.data["score"],
            level = request.data["level"],
            lives = request.data["lives"],
            player = request.auth.user,
            game_over = request.data["game_over"]
        )
        
        serializer = SaveSerializer(save)
        return Response(serializer.data)
    
    def list(self, request):
        """Handle GET requests to get all games
        Returns:
            Response -- JSON serialized list of games
        """
        saves = Save.objects.all()
        saves = saves.filter(player=request.auth.user)

        serializer = SaveSerializer(saves, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        """Handle DELETE request for a game
        Returns:
            Response -- Empty body with 204 status code
        """
        save = Save.objects.get(pk=pk)
        save.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def award_trophy(self, request, pk):
        """Handle POST requests for awarded trophies"""
        
        save = Save.objects.get(pk=pk)
        trophy = Trophy.objects.get(pk=request.data["trophy_id"])
        save.awarded_trophies.add(trophy)
        return Response({'message': 'trophy saved'}, status=status.HTTP_201_CREATED)