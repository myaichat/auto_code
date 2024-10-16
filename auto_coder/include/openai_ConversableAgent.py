from openai import OpenAI
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
            if class_name!='AssistantAgent':
                name=kwargs.get('name', None) 
                
                messages=kwargs.get('system_message', None)
                
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

class ConversableAgent:
    @trace
    def __init__(self, name,  llm_config=None,system_message =None, description=None,code_execution_config=None,
                 human_input_mode=None):
        self.name = name
        self.system_message = system_message
        self.llm_config = llm_config
        self.description=description
        self.chat_history = []
        self.client = OpenAI()  # Initialize the OpenAI client
    @trace
    def initiate_chat(self, manager, message):
        manager.start_chat(message)
    @trace
    def generate_reply(self, task, mocked_response=None, response_format=None):
        # Append user message to chat history
        print(self.name, len(self.chat_history))
        
        self.chat_history.append({"role": "user", "content": task})
        
        # Generate response from the LLM using the updated API
        format={}
        if response_format:
            format = {
                    'response_format' : response_format
            }
        if mocked_response:
            assistant_message=mocked_response
        else:
            response = self.client.chat.completions.create(
                model=self.llm_config["model"],
                messages=[
                    {"role": "system", "content": self.system_message},
                    *self.chat_history
                ],
            **format

            )
            

            

            # Append assistant message to chat history
            assistant_message = response.choices[0].message.content
        self.chat_history.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message
    @trace
    def reflect_with_llm(self, reflection_prompt, mocked_response=None, response_format=None):
        # Generate reflection based on the conversation history
        print('reflection', self.name, len(self.chat_history))
        reflection_message = {
            "role": "user",
            "content": reflection_prompt
        }
        format={}
        if response_format:
            format = {
                    'response_format' : response_format
            }
        if mocked_response:
            assistant_message=mocked_response
        else:
            response = self.client.chat.completions.create(
                model=self.llm_config["model"],
                messages=[
                    {"role": "system", "content": self.system_message},
                    *self.chat_history,
                    reflection_message  # Add reflection prompt at the end
                ],
                **format
            )
            assistant_message=response.choices[0].message.content
        return assistant_message
    @trace
    def summarize(self, summary_prompt, mocked_response=None, response_format=None):
        # Generate reflection based on the conversation history
        print('summary', self.name, len(self.chat_history))
        summarization_message = {
            "role": "user",
            "content": summary_prompt
        }
        format={}
        if response_format:
            format = {
                    'response_format' : response_format
            }        
        if mocked_response:
            assistant_message=mocked_response
        else:
            response = self.client.chat.completions.create(
                model=self.llm_config["model"],
                messages=[
                    {"role": "system", "content": self.system_message},
                    *self.chat_history,
                    summarization_message  # Add reflection prompt at the end
                ],
                **format
            )
            assistant_message=response.choices[0].message.content
        return assistant_message