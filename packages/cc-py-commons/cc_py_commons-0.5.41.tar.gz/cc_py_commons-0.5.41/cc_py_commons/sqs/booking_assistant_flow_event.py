import json

from cc_py_commons.config.env import app_config
from cc_py_commons.sqs.sqs_service import SqsService
from cc_py_commons.utils.logger_v2 import logger

class BookingAssistantFlowEvent:

	def send(self, user_id, load, params, capacity_search_equipments, request_id, auto_invite_details=None):
		'''
		Sends and event to the Booking Assistant Flow SQS queue specified in the config.
		Returns the messageId of the enqueued message for later retrieval.
		'''
		event = {
			'userId': user_id,
			'loadDTO': load,
			'payload': params,
			'capacitySearchEquipments': capacity_search_equipments,
			'requestId': request_id,
			'subject': f'{app_config.BOOKING_ASSISTANT_SNS_SUBJECT}',
			'className': f'{app_config.BOOKING_ASSISTANT_SNS_CLASS_NAME}',
			'autoInviteDetails': auto_invite_details
		}
		logger.debug(f"sending event {event} to {app_config.BOOKING_ASSISTANT_FLOW_QUEUE}")

		try:
			sqs_service = SqsService()
			return sqs_service.send(app_config.BOOKING_ASSISTANT_FLOW_QUEUE, json.dumps(event), app_config.BOOKING_ASSISTANT_DELAY_SECONDS)
		except Exception as e:
			logger.error(f"failed to send BookingAssistantFlowEvent message: {e}")
			logger.error(f"BookingAssistantFlowEvent message: {event}")
