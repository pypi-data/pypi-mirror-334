from datetime import datetime
from peewee import AutoField, CharField, DateTimeField, ForeignKeyField
from mxupy import EntityX
import bigOAINet as bigo


class Session(EntityX):
    """ 会话
    """
    sessionId = AutoField()

    # 主题、创建时间
    title = CharField()
    createTime = DateTimeField(default=datetime.now)

    # 对应dify的会话id，是一个guid
    conversationId = CharField(null=True)

    # 聊天室、创建者
    room = ForeignKeyField(bigo.Room, backref='sessions', column_name='roomId', on_delete='CASCADE')
    createUser = ForeignKeyField(bigo.User, backref='sessions', column_name='createUserId', on_delete='CASCADE')

    # 最后一条消息
    # lastRecord = ForeignKeyField(Record, backref='Session', column_name='lastRecordId', on_delete='CASCADE')

    class Meta:
        database = bigo.db
        name = '会话'
