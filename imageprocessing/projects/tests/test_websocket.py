from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase
from ...imageprocessing.asgi import application 

User = get_user_model()

class ProjectConsumerTest(TransactionTestCase):
    async def asyncSetUp(self):
        self.project_id = 1  # Replace with a valid project ID if necessary
        self.project_group_name = f'project_{self.project_id}'
        self.url = f'/ws/project/{self.project_id}/'

    async def test_connect(self):
        communicator = WebsocketCommunicator(application, self.url)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_disconnect(self):
        communicator = WebsocketCommunicator(application, self.url)
        await communicator.connect()
        await communicator.disconnect()

    async def test_project_update(self):
        communicator = WebsocketCommunicator(application, self.url)
        await communicator.connect()

        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            self.project_group_name,
            {
                'type': 'project_update',
                'status': 'updated'
            }
        )

        response = await communicator.receive_json_from()
        self.assertEqual(response, {'status': 'updated'})

        await communicator.disconnect()
