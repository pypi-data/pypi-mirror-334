from RSPileScripting._client import Client
import RSPileScripting.generated_python_files.pile_section_services.DrivenCrossSectionHPileService_pb2 as DrivenCrossSectionHPileService_pb2
import RSPileScripting.generated_python_files.pile_section_services.DrivenCrossSectionHPileService_pb2_grpc as DrivenCrossSectionHPileService_pb2_grpc
from RSPileScripting.PileSection.CrossSectionTypes.Driven.UserSelectedArea import UserSelectedArea

from enum import Enum

class HPileTypeMetric(Enum):
	HP_360x174 = DrivenCrossSectionHPileService_pb2.HPileTypeMetric.E_360x174
	HP_360x152 = DrivenCrossSectionHPileService_pb2.HPileTypeMetric.E_360x152
	HP_360x132 = DrivenCrossSectionHPileService_pb2.HPileTypeMetric.E_360x132
	HP_360x108 = DrivenCrossSectionHPileService_pb2.HPileTypeMetric.E_360x108
	HP_310x125 = DrivenCrossSectionHPileService_pb2.HPileTypeMetric.E_310x125
	HP_310x110 = DrivenCrossSectionHPileService_pb2.HPileTypeMetric.E_310x110
	HP_310x93 = DrivenCrossSectionHPileService_pb2.HPileTypeMetric.E_310x93
	HP_310x79 = DrivenCrossSectionHPileService_pb2.HPileTypeMetric.E_310x79
	HP_250x85 = DrivenCrossSectionHPileService_pb2.HPileTypeMetric.E_250x85
	HP_250x62 = DrivenCrossSectionHPileService_pb2.HPileTypeMetric.E_250x62
	HP_200x53 = DrivenCrossSectionHPileService_pb2.HPileTypeMetric.E_200x53

class HPileTypeImperial(Enum):
	HP_14x117 = DrivenCrossSectionHPileService_pb2.HPileTypeImperial.E_14x117
	HP_14x102 = DrivenCrossSectionHPileService_pb2.HPileTypeImperial.E_14x102
	HP_14x89 = DrivenCrossSectionHPileService_pb2.HPileTypeImperial.E_14x89
	HP_14x73 = DrivenCrossSectionHPileService_pb2.HPileTypeImperial.E_14x73
	HP_12x84 = DrivenCrossSectionHPileService_pb2.HPileTypeImperial.E_12x84
	HP_12x74 = DrivenCrossSectionHPileService_pb2.HPileTypeImperial.E_12x74
	HP_12x63 = DrivenCrossSectionHPileService_pb2.HPileTypeImperial.E_12x63
	HP_12x53 = DrivenCrossSectionHPileService_pb2.HPileTypeImperial.E_12x53
	HP_10x57 = DrivenCrossSectionHPileService_pb2.HPileTypeImperial.E_10x57
	HP_10x42 = DrivenCrossSectionHPileService_pb2.HPileTypeImperial.E_10x42
	HP_8x36 = DrivenCrossSectionHPileService_pb2.HPileTypeImperial.E_8x36

class HPilePerimeter(Enum):
	H_PILE_PERIMETER = DrivenCrossSectionHPileService_pb2.HPilePerimeter.E_H_PILE_PERIMETER
	H_BOX_PERIMETER = DrivenCrossSectionHPileService_pb2.HPilePerimeter.E_H_BOX_PERIMETER

class HPileArea(Enum):
	H_PILE_AREA = DrivenCrossSectionHPileService_pb2.HPileArea.E_H_PILE_AREA
	H_BOX_AREA = DrivenCrossSectionHPileService_pb2.HPileArea.E_H_BOX_AREA
	USER_SELECT = DrivenCrossSectionHPileService_pb2.HPileArea.E_H_USER_SELECT

class HPile:
	"""
	Examples:
	:ref:`pile sections driven`
	"""
	def __init__(self, model_id: str, pile_id: str, client: Client):
		self._model_id = model_id
		self._pile_id = pile_id
		self._client = client
		self._stub = DrivenCrossSectionHPileService_pb2_grpc.DrivenCrossSectionHPileServiceStub(self._client.channel)
		self.UserSelectedArea = UserSelectedArea(self._model_id, self._pile_id, self._client)

	def _getHPileProperties(self) -> DrivenCrossSectionHPileService_pb2.HPileProperties:
		request = DrivenCrossSectionHPileService_pb2.GetHPilePropertiesRequest(
			session_id=self._client.sessionID, model_id=self._model_id, pile_id=self._pile_id)
		response = self._client.callFunction(self._stub.GetHPileProperties, request)
		return response.hpile_props

	def _setHPileProperties(self, hpileProps: DrivenCrossSectionHPileService_pb2.HPileProperties):
		request = DrivenCrossSectionHPileService_pb2.SetHPilePropertiesRequest(
			session_id=self._client.sessionID, model_id=self._model_id, pile_id=self._pile_id, 
			hpile_props=hpileProps)
		self._client.callFunction(self._stub.SetHPileProperties, request)

	def getHPileTypeMetric(self) -> HPileTypeMetric:
		properties = self._getHPileProperties()
		return HPileTypeMetric(properties.H_pile_type_m)
	
	def setHPileTypeMetric(self, hpileTypeMetric: HPileTypeMetric):
		properties = self._getHPileProperties()
		properties.H_pile_type_m = hpileTypeMetric.value
		self._setHPileProperties(properties)

	def getHPileTypeImperial(self) -> HPileTypeImperial:
		properties = self._getHPileProperties()
		return HPileTypeImperial(properties.H_pile_type_i)
	
	def setHPileTypeImperial(self, hpileTypeImperial: HPileTypeImperial):
		properties = self._getHPileProperties()
		properties.H_pile_type_i = hpileTypeImperial.value
		self._setHPileProperties(properties)

	def getHPilePerimeter(self) -> HPilePerimeter:
		properties = self._getHPileProperties()
		return HPilePerimeter(properties.H_pile_perimeter)
	
	def setHPilePerimeter(self, hpilePerimeter: HPilePerimeter):
		properties = self._getHPileProperties()
		properties.H_pile_perimeter = hpilePerimeter.value
		self._setHPileProperties(properties)

	def getHPileArea(self) -> HPileArea:
		properties = self._getHPileProperties()
		return HPileArea(properties.H_pile_area)
	
	def setHPileArea(self, hpileArea: HPileArea):
		properties = self._getHPileProperties()
		properties.H_pile_area = hpileArea.value
		self._setHPileProperties(properties)