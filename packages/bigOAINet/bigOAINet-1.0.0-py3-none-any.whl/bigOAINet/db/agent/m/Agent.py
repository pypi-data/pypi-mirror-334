from peewee import (
    IntegerField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    BooleanField,
    AutoField,
)
from mxupy import EntityX
import bigOAINet as bigo


class Agent(EntityX):
    class Meta:
        database = bigo.db
        name = "智能体"

    agentId = AutoField()

    name = CharField(max_length=200)
    tags = CharField(max_length=200)
    logo = CharField(max_length=200)
    desc = CharField(max_length=500)

    # 是否可以多人，意思是群聊，此信息只有智能体本身才能确定
    canGroup = CharField(null=False)

    # 类型，可以是智能体Agent、工作流Workflow、聊天助手ChatAssistant、文本生成应用TextGen、Chatflow
    # 注意工具无法直接调用，dify没有给出对应的api，工具直接嵌入到智能体就可以了
    type = CharField(max_length=200)

    apiKey = CharField(max_length=200)
