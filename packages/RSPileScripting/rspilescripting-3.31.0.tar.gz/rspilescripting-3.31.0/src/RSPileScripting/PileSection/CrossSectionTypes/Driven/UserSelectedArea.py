from RSPileScripting._client import Client
import RSPileScripting.generated_python_files.pile_section_services.DrivenCrossSectionHPileUserSelectedAreaService_pb2 as DrivenCrossSectionHPileUserSelectedAreaService_pb2
import RSPileScripting.generated_python_files.pile_section_services.DrivenCrossSectionHPileUserSelectedAreaService_pb2_grpc as DrivenCrossSectionHPileUserSelectedAreaService_pb2_grpc

class UserSelectedArea:
    def __init__(self, model_id: str, pile_id: str, client: Client):
        self._model_id = model_id
        self._pile_id = pile_id
        self._client = client
        self._stub = DrivenCrossSectionHPileUserSelectedAreaService_pb2_grpc.DrivenCrossSectionHPileUserSelectedAreaServiceStub(self._client.channel)

    def _getUserSelectedAreaProperties(self) -> DrivenCrossSectionHPileUserSelectedAreaService_pb2.HPileUserSelectedAreaProperties:
        request = DrivenCrossSectionHPileUserSelectedAreaService_pb2.GetHPileUserSelectedAreaPropertiesRequest(
            session_id=self._client.sessionID, model_id=self._model_id, pile_id=self._pile_id)
        response = self._client.callFunction(self._stub.GetHPileUserSelectedAreaProperties, request)
        return response.hpile_user_selected_area_props

    def _setUserSelectedAreaProperties(self, hpileUserSelectedAreaProps: DrivenCrossSectionHPileUserSelectedAreaService_pb2.HPileUserSelectedAreaProperties):
        request = DrivenCrossSectionHPileUserSelectedAreaService_pb2.SetHPileUserSelectedAreaPropertiesRequest(
            session_id=self._client.sessionID, model_id=self._model_id, pile_id=self._pile_id, 
            hpile_user_selected_area_props=hpileUserSelectedAreaProps)
        self._client.callFunction(self._stub.SetHPileUserSelectedAreaProperties, request)

    def getAreaOfTip(self) -> float:
        properties = self._getUserSelectedAreaProperties()
        return properties.H_pile_area_user_select
    
    def setAreaOfTip(self, areaOfTip: float):
        properties = self._getUserSelectedAreaProperties()
        properties.H_pile_area_user_select = areaOfTip
        self._setUserSelectedAreaProperties(properties)