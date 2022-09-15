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
    
    def destroy(self, request, pk):
        """Handle DELETE request for a asset
        Returns:
            Response -- Empty body with 204 status code
        """
        asset = Asset.objects.get(pk=pk)
        asset.delete()
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
            "file",
            "type"
        )