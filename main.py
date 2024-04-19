from autogen import AssistantAgent, UserProxyAgent

llm_config = {"model": "gpt-4", "api_key": "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"}
assistant = AssistantAgent("assistant", llm_config=llm_config)
user_proxy = UserProxyAgent("user_proxy", code_execution_config=False)

# Start the chat
user_proxy.initiate_chat(
    assistant,
    message="Tell me a joke about NVDA and TESLA stock prices.",
)