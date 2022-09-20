""" View module for handling request about games """
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from JSGame_api.models import Save

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
            'user',
            'lives',
            'game_over'
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
    
    def create(self, request):
        """ Handle POST operations 
        
        Returns
            Response -- JSON serialized game instance
        """
        
        
        save = Save.objects.create(
            score = request.data["score"],
            level = request.data["level"],
            lives = request.data["lives"],
            user = request.auth.user,
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
        saves = saves.filter(user=request.auth.user)

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