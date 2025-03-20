from tgram import TgBot, filters
from tgram.types import (
    Message
)
from tgram_dnd.actions.action import Action
from typing import Optional, Union, List

class MessageBlock:
    '''the block that process Messages and runs a series of Actions (:ref:`what-is-an-action?`)
    
    Args:
        actions (Union[List[:class:`tgram_dnd.actions.Action`], :class:`tgram_dnd.actions.Action`]): the actions that will be executed
        filter (`tgram.filters.Filter <https://z44d.github.io/tgram/tgram.html#tgram.filters.Filter>`_, *optional*): filter incoming callbacks, pass Nothing to trigger all updates
    
    Returns:
        None'''
    def __init__(
        self,
        actions: Union[List[Action], Optional[Action]],
        filter: Optional[filters.Filter] = None,
    ):
        '''this defines a MessageBlock'''
        self.actions = [actions] if not isinstance(actions, list) else actions
        self.filter = filter or filters.all

    async def exec(
        self,
        bot: TgBot,
        m: Message
    ):
        '''this is where the block actions run'''
        if await self.filter(bot, m):
            for action in self.actions:
                await action(m)