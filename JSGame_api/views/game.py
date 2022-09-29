""" View module for handling request about games """
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from JSGame_api.models import Game, Asset

class GameSerializer(serializers.ModelSerializer):
    """ JSON serializer for games """
    
    class Meta:
        model = Game
        fields = (
            'id',
            'name',
            'access_code',
            'background_asset',
            'character_asset',
            'creator',
            'enemy_asset',
            'trophy_asset',
            'other_asset',
        )
        
class GameView(ViewSet):
    """ JSGame games view """
    
    def create(self, request):
        """ Handle POST operations 
        
        Returns
            Response -- JSON serialized game instance
        """
        
        game = Game.objects.create(
            name = request.data["name"],
            creator = request.auth.user,
            access_code = request.data["access_code"],
            background_asset = request.data["background_asset"],
            character_asset = request.data['character_asset'],
            collectable_asset = request.data["collectable_asset"],
            enemy_asset = request.data["enemy_asset"],
            trophy_asset = request.data["trophy_asset"],
            other_asset = request.data["other_asset"]
        )
        
        serializer = GameSerializer(game)
        return Response(serializer.data)
    
    def list(self, request):
        """Handle GET requests to get all games
        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()
        
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk):
        """Handle DELETE request for a game
        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, pk):
        """Handle PUT requests for a game
        Returns:
            Response -- Empty body with 204 status code
        """

        character_asset = Asset.objects.get(pk=request.data["character_asset"])
        background_asset = Asset.objects.get(pk=request.data["background_asset"])
        enemy_asset = Asset.objects.get(pk=request.data["enemy_asset"])
        trophy_asset = None
        other_asset = None
        collectable_asset = None

        game = Game.objects.get(pk=pk)
        game.name = request.data["name"]
        game.creator = request.auth.user
        game.character_asset = character_asset
        game.background_asset = background_asset
        game.enemy_asset = enemy_asset
        game.trophy_asset = trophy_asset
        game.other_asset = other_asset
        game.collectable_asset = collectable_asset
        game.access_code = request.data["access_code"]
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)