from functools import wraps
from pprint import pprint as pp 
from auto_coder.include.openai_ConversableAgent import  ConversableAgent

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
        if method_name == 'select_speaker': 
            pp(args)

            pp(kwargs)
            #e()
            _,last_speaker, selector, messages=args
            message=messages #[0]['content']
            owner=args[0]
            params= f'{class_name}: last_speaker: {last_speaker.name}, selector: {selector.name}, "{message[:30]}"'
            # e()               

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
    def select_speaker(self, last_speaker, selector,message):
        checking_agent = ConversableAgent(name="checking_agent")

        sysmsg=('You are in a role play game. The following roles are available:\n'
 '                Engineer: An engineer that writes code based on the plan '
 'provided by the planner.\n'
 'Writer: Writer.Write blogs based on the code execution results and take '
 'feedback from the admin to refine the blog.\n'
 'Executor: Execute the code written by the engineer and report the result.\n'
 'Planner: Planner. Given a task, determine what information is needed to '
 'complete the task. After each step is done by others, check the progress and '
 'instruct the remaining steps.\n'
 '                Read the following conversation.\n'
 "                Then select the next role from ['Engineer', 'Writer', "
 "'Executor', 'Planner'] to play. Only return the role.")
        speaker_selection_agent = ConversableAgent(
            name="speaker_selection_agent",
            system_message=sysmsg,
            chat_messages=message,
            llm_config=selector.llm_config,
            human_input_mode="NEVER",  # Suppresses some extra terminal outputs, outputs will be handled by select_speaker_auto_verbose
        )
        start_message={'content': 'Read the above conversation. Then select the next role from '
            "['Engineer', 'Writer', 'Executor', 'Planner'] to play. Only "
            'return the role.',
 'name': 'checking_agent',
 'override_role': 'system'}
        max_turns=10
        result= checking_agent.initiate_chat(speaker_selection_agent, messages=start_message, loop_name='SELECT_SPEAKER',
                                             max_turns=max_turns)
        print("select_speaker: result",result)
