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
        if method_name == 'create':
            pp(args)
            pp(kwargs)
            owher=args[0].__class__.__name__  
            agent=kwargs.get('agent', None)
            ahent_name=agent.name if agent else 'None'
            if class_name=='OpenAIWrapper' and apc.show_create:
                messages=kwargs.get('messages', None)
                if not messages:
                    messages=args[1]['messages']
                params=f'{owher}: {ahent_name}, {messages}'
            else:
                params=f'{owher}: {ahent_name}'
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

class GroupChat:
    def __init__(self, agents,messages, max_round=10):
        self.agents = agents
        self.max_round = max_round
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)
    @trace
    def run_chat(self, initial_message):
        self.add_message(initial_message)
        for round_num in range(self.max_round):

            if 0:
                for agent in self.agents:
                    response = agent.execute(initial_message)
                    self.add_message(response)
                    print(f"Round {round_num + 1}: {response}")