from mxupy import EntityXControl
import bigOAINet as bigo


class ChatControl(EntityXControl):
    class Meta:
        model_class = bigo.Chat
    
    def add(self, sessionId, userId, content, type='text'):
        """ 获取需要显示的内容

        Args:
            type (str): 内容类型
            content (str): 内容

        Returns:
            str: 显示的内容
        """
        sup = super()
        def _do():
            
            im = bigo.SessionControl.inst().get_one(select='roomId', where={'sessionId':sessionId})
            if im.error:
                return im
            
            if im.data is None:
                return im.set_error('会话不存在')
            
            roomId = im.data.roomId
            im = sup.add(bigo.Chat(roomId=roomId, sessionId=sessionId, content=content, type=type, userId=userId))
            
            return im
        
        return self.run(_do)
    