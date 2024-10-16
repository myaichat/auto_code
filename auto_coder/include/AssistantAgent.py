from auto_coder.include.openai_ConversableAgent import  ConversableAgent
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
        if method_name == '__init__':
            pp(args)
            pp(kwargs)
            #e()
            #class_name=args[0].__class__.__name__ 
            if 1:
                name=kwargs.get('name', None) 
                
                messages=kwargs.get('description', None)
                
                if  1:
                    params=f'{class_name}: {name}, {messages[:30]}'
                else:
                    params=f'{class_name}: {name}'
                #e()

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

class AssistantAgent(ConversableAgent):
    @trace
    def __init__(self, name,  llm_config,system_message =None, description=None):
        super().__init__(name,  llm_config,system_message, description)
        self.name = name
        self.system_message = system_message
        self.llm_config = llm_config
        self.description=description
        self.chat_history = []
        