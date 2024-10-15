import yaml, json
from os.path import join, isfile
from pprint import pprint as pp

# Import apc and execute_pipeline from auto_reflection
from auto_code import apc, execute_pipeline

# Set verbose to True
apc.verbose = True

if __name__ == '__main__':

    theme = "Write a blogpost about the stock price performance of "\
"Nvidia in the past month. Today's date is 2024-04-23."
    py_pipeline_name = 'blog'
    yaml_pprompt_config = join('yaml_config', 'blog.yaml')


    if 0:  # mock
        

        mock_file = join('mock', 'coding_blogger', 'blog.json')
        assert isfile(mock_file), f"Mock file not found: {mock_file}"
        apc.load_mock(mock_file)  # Access apc to load mock data
        
    # Use execute_pipeline
    if 1:
        blog = execute_pipeline({'theme':theme}, py_pipeline_name, yaml_pprompt_config)
        print(blog)
        pp(json.loads(blog))

