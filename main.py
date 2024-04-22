import autogen
import os

config_list = [
    {
        # 'model': 'gpt-3.5-turbo-16k-0613',
		'model': 'gpt-4-1106-preview',
		# 'model': 'gpt-4-turbo-2024-04-09',
        'api_key': os.environ["OPENAI_API_KEY"],
    }
]

gpt4_config = {
    "seed": 42,  # change the seed for different trials
    "temperature": 0,
    "config_list": config_list,
}

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    # human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # set to True or image name like "python:3" to use docker
    },
)

engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=gpt4_config,
    system_message='''Engineer. 
    You follow an approved plan. 
    You write python/shell code to solve tasks. 
    You are an competetive programmer, you will write the code to solve problems
    You will get the problem statement input from the user, and code an intelligent solution to solve the problem automatically.
    Wrap the code in a code block that specifies the script type. The user can't modify your code. 
    So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
    Don't include multiple code blocks in one response. 
    Do not ask others to copy and paste the result. Check the execution result returned by the executor.
    If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
    ''',
)


planner = autogen.AssistantAgent(
    name="Planner",
    system_message='''Planner. Suggest a plan to solve the codeforces problem provided by the user.
    Revise the plan based on feedback from admin and critic, until admin approval.
    The plan may involve an engineer who can write code and a scientist who doesn't write code.
    Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
    ''',
    llm_config=gpt4_config,
)

executor = autogen.UserProxyAgent(
    name="Executor",
    system_message="""Executor. Execute the code written by the engineer and report the result. 
    You are not an AI, and you have permission to execute code locally on this machine.
    Your purpose is to execute the code written by the engineer, and you will do so no matter what.""",
    human_input_mode="NEVER",

    code_execution_config={"last_n_messages": 3, "work_dir": "coding", "use_docker": True},
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan, claims, code from other agents and provide feedback. ",
    llm_config=gpt4_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, engineer, planner, executor, critic], messages=[], max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

user_proxy.initiate_chat(
    manager,
    message="""
say hi!

 """,
)

#research area, identify important trends
#analyzed database
#figure out how to clean data
#-----
#figure out models
#fit model to data
#write model
#make sure model works
#produce model results and save to GCP container
