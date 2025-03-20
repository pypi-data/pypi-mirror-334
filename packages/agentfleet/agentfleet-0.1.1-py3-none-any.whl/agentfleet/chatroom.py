from pydantic import BaseModel, Field, create_model
from langchain_core.language_models import BaseChatModel
from langchain.schema.messages import HumanMessage,AIMessage,BaseMessage
from typing import List, Optional, Dict, Any
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from agentfleet.mytools import *

from agentfleet.agent import Agent

class StateModel(BaseModel):
    conversation_summary: Optional[str] = Field(default=None, description="A concise summary of the conversation, not exceeding 50 words")

class Chatroom(BaseModel):
    llm: BaseChatModel
    agents: List[Agent]
    current_agent: Optional[Agent]
    agent_map: dict = {}
    stateList: list = []
    state: StateModel
    enable_state: bool = True
    
    def __init__(self,
                 llm: BaseChatModel = None,
                 agents: Optional[List[Agent]] = None, 
                 current_agent: Optional[Agent] = None, 
                 stateList: list = [],
                 state: StateModel = None,
                 enable_state: bool = True
                 ):
        if llm is None:
            raise ValueError("llm cannot be None")
        agents = agents or []  # Assign an empty list if agents is None
        state = state or StateModel(conversation_summary=None)
        super().__init__(llm=llm, agents=agents, current_agent=current_agent, stateList=stateList, state=state, enable_state=enable_state)
        self.agent_map = {agent.name: agent for agent in agents}

    def invoke(self, messages):
        messages_copy = messages[:]
        messages_copy, agent_name = self.current_agent.invoke(messages_copy)
        self.current_agent = self.agent_map.get(agent_name, self.current_agent)
        if self.enable_state:
            self.update_state(messages_copy)  # Update the state after each invocation
        return messages_copy

    def extract_messages(self, messages: List[BaseMessage]) -> str:
        concatenated_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role = "Human"
            elif isinstance(message, AIMessage):
                role = "AI"
            else:
                role = "Unknown"
            concatenated_messages.append(f"{role}: {message.content}")
        return '; '.join(concatenated_messages)
    
    def update_state(self, messages):
        # Update the state based on conversation messages
        messages_copy = messages[:]
        messages_str = self.extract_messages(messages_copy)  

        # Dynamically add new fields to the existing model to create a new model
        newFieldsList = self.stateList
        newFields = {
            state["name"]: (Optional[str], Field(None, description=state["description"]))
                for state in newFieldsList
        }

        newStateModel = create_model(
            'newStateModel',
            __base__=StateModel,
            **newFields
        )

        structured_llm = self.llm.with_structured_output(newStateModel)
        state_update_prompt = f"""
        You are responsible for extracting relevant state information from
        the conversation messages and updating the chatroom's state. 
        The state may include user preferences, conversation topics,
        or any key-value pairs useful for the chatroom's functionality.
        Please return a structured dictionary containing the updated state.
        {messages_str}
        """
        
        self.state = structured_llm.invoke(state_update_prompt)
        print("*****")
        print(self.state)
        print("*****")


    def get_state(self, key: str):
        """Get a value from the state by key."""
        return getattr(self.state, key, None)

    def set_state(self, key: str, value):
        """Set a value in the state."""
        setattr(self.state, key, value)

def create_transfer_function(target_agent_name, docstring=None):
    """Creates a transfer function to transfer to the specified agent.

    Args:
        target_agent_name (str): The name of the agent to transfer to.
        docstring (str, optional): Custom docstring for the generated function.

    Returns:
        BaseTool: A dynamically created transfer tool that transfers to the specified agent.
    """
    class TransferTool(BaseTool):
        name: str = f"transfer_to_{target_agent_name}"
        description: str = docstring if docstring else f"Transfer the conversation to {target_agent_name}."

        def _run(
            self, run_manager: Optional[CallbackManagerForToolRun] = None
        ) -> str:
            print(f"transfer to {target_agent_name}")
            return target_agent_name

    return TransferTool()

def create_chatroom(config_json, llm, tool_dict=None):
    stateList = config_json["states"]
    enable_state = config_json.get("enable_state", True)
    agents = []
    for agent_config in config_json["agents"]:
        name = agent_config["name"]
        sys_prompt = agent_config["sys_prompt"]
        
        # Use tool_dict if provided, otherwise fall back to globals()
        if tool_dict:
            util_tools = [tool_dict.get(tool_name) for tool_name in agent_config["util_tools"]]
        else:
            util_tools = [globals()[tool_name] for tool_name in agent_config["util_tools"]]
        
        transfer_tools = [create_transfer_function(transfer["name"], transfer["description"]) for transfer in agent_config["transfer_tools"]]
        agent = Agent(name=name, llm=llm, sys_prompt=sys_prompt, util_tools=util_tools, transfer_tools=transfer_tools)
        agents.append(agent)
    
    initial_agent_name = config_json["initial_agent"]
    initial_agent = next(agent for agent in agents if agent.name == initial_agent_name)
    return Chatroom(llm, agents, initial_agent, stateList, enable_state=enable_state)