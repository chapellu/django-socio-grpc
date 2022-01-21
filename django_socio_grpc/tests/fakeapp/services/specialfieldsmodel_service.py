from django_socio_grpc import generics
from fakeapp.models import SpecialFieldsModel
from fakeapp.serializers import SpecialFieldsModelSerializer, CustomRetrieveResponseSpecialFieldsModelSerializer
from django_socio_grpc.decorators import grpc_action
from asgiref.sync import sync_to_async


class SpecialFieldsModelService(generics.AsyncModelService):
    queryset = SpecialFieldsModel.objects.all().order_by("uuid")
    serializer_class = SpecialFieldsModelSerializer

    @sync_to_async
    def format_custom_message(self, instance):
        serializer = CustomRetrieveResponseSpecialFieldsModelSerializer(instance)
        return serializer.message 

    @grpc_action(request=[{"name": "uuid", "type": "string"}], response=CustomRetrieveResponseSpecialFieldsModelSerializer)
    async def Retrieve(self, request, context):
        instance = self.get_object()
        return await self.format_custom_message(instance)
