import  auto_code as autogen

if 1:
    user_proxy = autogen.ConversableAgent(
        name="Admin",
        system_message="Give the task, and send "
        "instructions to writer to refine the blog post.",
        code_execution_config=False,
        llm_config=llm_config,
        human_input_mode="ALWAYS",
    )