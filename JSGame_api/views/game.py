""" View module for handling request about games """
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from JSGame_api.models import Game

class GameSerializer(serializers.ModelSerializer):
    """ JSON serializer for games """
    
    class Meta:
        model = Game
        fields = (
            'id',
            'score',
            'level',
            'date_created',
            'last_saved',
            'user',
            'lives',
            'game_over'
        )

class GameView(ViewSet):
    """ JSGame games view """
    
    def create(self, request):
        """ Handle POST operations 
        
        Returns
            Response -- JSON serialized game instance
        """
        
        
        game = Game.objects.create(
            score = request.data["score"],
            level = request.data["level"],
            lives = request.data["lives"],
            user = request.auth.user,
            game_over = request.data["game_over"]
        )
        
        serializer = GameSerializer(game)
        return Response(serializer.data)
    
    def list(self, request):
        """Handle GET requests to get all games
        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()
        games = games.filter(user=request.auth.user)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        """Handle DELETE request for a game
        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)