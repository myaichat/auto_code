from .include.config import init_config
from .include.utils import execute_pipeline
from .include.openai_ConversableAgent import  ConversableAgent
from .include.AssistantAgent import  AssistantAgent
from .include.GroupChat import  GroupChat
from .include.GroupChatManager import  GroupChatManager



# Initialize apc globally
init_config.init(**{})  # Initialize the configuration
apc = init_config.apc  # Expose apc

__all__ = ['execute_pipeline', 'apc', 'ConversableAgent','AssistantAgent', 'GroupChat', 'GroupChatManager']