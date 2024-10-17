from functools import wraps
from pprint import pprint as pp 
from auto_coder.include.config import init_config
apc = init_config.apc


def trace(func):
    @wraps(func) 
    def wrapper(*args, **kwargs):
       
        
        class_name = args[0].__class__.__name__
        method_name = func.__name__        
        branch=apc.tree['calling']
        apc.depth += 1
        apc.call_id +=1
        
        params=''
        if method_name == 'GROUPCHAT_loop':
            name=args[1]    
            max_turns=args[2]
            owner=args[0]
            
            params= f'{owner.name}: name: {name}, max_turns: {max_turns}'
        if method_name == 'GROUPCHAT_leg':
            loop_leg=args[1]
            owner=args[0]
            #params= recipient.name
            params= f'{owner.name}: loop_leg: {loop_leg} ||||||||||||||||||' 

        if method_name == 'create':
            pp(args)
            pp(kwargs)
            owner=args[0].__class__.__name__  
            agent=kwargs.get('agent', None)
            agent_name=agent.name if agent else 'None'
            if not agent_name:
                agent_name=kwargs.get('name', None) 
            if class_name=='OpenAIWrapper' and apc.show_create:
                messages=kwargs.get('messages', None)
                if not messages:
                    messages=args[1]['messages']
                params=f'{owner}: {agent_name}, {messages}'
            else:
                params=f'{owner}: {agent_name}'
            #e()
        if method_name == 'run_chat':
            pp(args)
            pp(kwargs)
            messages= kwargs['messages'] #[0]['content']
            sender= kwargs['sender']
            owner=args[0]

            params= f"{owner.name}: messages: {messages[:30]}, sender: {sender.name}"             

        branch['calling'][apc.call_id]={'name': f'{class_name}.{method_name} ({params})','depth':apc.depth,'calling':{},'caller':apc.depth-1}
       
        print("Before the function runs.", apc.depth, class_name, method_name)

        print(f"Method '{class_name}.{method_name}' is about to be called.")
        result = func(*args, **kwargs)
        print(f"Method '{class_name}.{method_name}' has finished execution.")
        if method_name == 'create':
            apc.call_id +=1
            owner=args[0].__class__.__name__
            if owner=='OpenAIWrapper' and apc.show_create:
                params=result
                if isinstance(params, ChatCompletion):
                    params=result.choices[0].message.content
                    pass
                
                branch['calling'][apc.call_id]={'name': f'{class_name}.{method_name} ({owner}: Result: {params})','depth':apc.depth,'calling':{},'caller':apc.depth-1}
                
        apc.depth -= 1
        return result
    return wrapper

class GroupChatManager:
    @trace
    def __init__(self,name, groupchat, llm_config):
        self.groupchat = groupchat
        self.llm_config = llm_config
        self.name=name
    @trace
    def GROUPCHAT_loop(self,  max_turns, name):
        #just for 
        pass
    @trace
    def GROUPCHAT_leg(self, loop_leg):
        #just for 
        pass   

    @trace
    def run_chat(self,sender, messages, groupchat):
        self.GROUPCHAT_loop(groupchat.max_round, 'GROUP_CHAT_MANAGER: run_chat')
        for i in range(groupchat.max_round):
            self.GROUPCHAT_leg(i)
            self.groupchat.select_speaker(sender, self, messages)
            break