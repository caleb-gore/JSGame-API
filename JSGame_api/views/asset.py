from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from JSGame_api.models import Asset
from django.core.files.base import ContentFile
import uuid
import base64

class AssetView(ViewSet):
    """Game Asset View"""
    
    def create(self, request):
        """Handle POST operations
        
        Returns
            Response -- JSON serialized game instance
        """
        
        format, imgstr = request.data['file'].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["name"]}-{uuid.uuid4()}.{ext}')
        
        asset = Asset.objects.create(
            name = request.data['name'],
            width = request.data['width'],
            height = request.data['height'],
            frames = request.data['frames'],
            type = request.data['type'],
            file = data
        )
        
        serializer = AssetSerializer(asset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request):
        """Handle GET requests to get all assets
        Returns:
            Response -- JSON serialized list of assets
        """
        assets = Asset.objects.all()

        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """Handle GET requests for single user
        Returns:
            Response -- JSON serialized user
        """
        try:
            asset = Asset.objects.get(pk=pk)
            serializer = AssetSerializer(asset)
            return Response(serializer.data)
        except Asset.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    
    def destroy(self, request, pk):
        """Handle DELETE request for a asset
        Returns:
            Response -- Empty body with 204 status code
        """
        asset = Asset.objects.get(pk=pk)
        asset.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, pk):
        """Handle PUT requests for a game
        Returns:
            Response -- Empty body with 204 status code
        """
        
        asset = Asset.objects.get(pk=pk)
        try:
            format, imgstr = request.data['file'].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["name"]}-{uuid.uuid4()}.{ext}')
            asset.file = data
        except:
            pass

        asset = Asset.objects.get(pk=pk)
        asset.name = request.data['name']
        asset.width = request.data['width']
        asset.height = request.data['height']
        asset.frames = request.data['frames']
        asset.type = request.data['type']
        asset.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class AssetSerializer(serializers.ModelSerializer):
    """JSON serializer for assets"""
    
    class Meta:
        model = Asset
        fields = (
            "id",
            "name",
            "width",
            "height",
            "frames",
            "file",
            "type"
        )