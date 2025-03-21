import requests
import json
from mxupy import read_config
import bigOAINet as bigo

# dify 调用


class AgentCaller:

    def __init__(self, agentId, userId, conversationId):

        self.url = read_config().get('dify_api_url', {})
        self.agentId = agentId
        self.agent = bigo.AgentControl.inst().get_one_by_id(agentId).data
        self.userId = userId
        self.conversationId = conversationId

    def call(self, msg):

        payload = json.dumps({
            "inputs": msg.get('input', {}),
            "query": msg.get('query', ''),
            "response_mode": "streaming",
            "conversation_id": str(self.conversationId),
            "user": str(self.userId),
            "files": msg.get('files', [])
        })
        headers = {
            'Authorization': f'Bearer {self.agent.apiKey}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)

        return response

    def upload(self):
        url = self.url + "/files/upload"

        payload = {}
        files = [('file', ('file', open('/path/to/file', 'rb'), 'application/octet-stream'))]
        headers = {
            'Authorization': 'Bearer {self.agent.apiKey}'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        # print(response.text)
        return response
