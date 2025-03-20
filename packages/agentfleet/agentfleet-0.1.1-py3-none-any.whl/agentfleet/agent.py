from pydantic import BaseModel, SkipValidation
from typing import List, Optional
from langchain_core.language_models import BaseChatModel
from langchain.schema.messages import SystemMessage
from langchain_core.tools.structured import StructuredTool
from langchain_core.tools import BaseTool

class Agent(BaseModel):
    name: str = "Agent"
    llm: BaseChatModel
    sys_prompt: str = "You are a helpful Agent"
    util_tools: Optional[List[BaseTool]] = None
    transfer_tools: Optional[List[BaseTool]] = None
    tools: List = []
    llm_with_tools: Optional[SkipValidation] = None
    util_tools_map: dict = {}
    transfer_tools_map: dict = {}
    messages: List = []

    def __init__(self, 
                 name: str = "Agent", 
                 llm: BaseChatModel = None, 
                 sys_prompt: str = "You are a helpful Agent", 
                 util_tools: Optional[List[StructuredTool]] = None,
                 transfer_tools: Optional[List[StructuredTool]] = None):
        if llm is None:
            raise ValueError("llm cannot be None")
        util_tools = util_tools or []
        transfer_tools = transfer_tools or []
        super().__init__(name=name, llm=llm, sys_prompt=sys_prompt, util_tools=util_tools, transfer_tools=transfer_tools)  # Call the BaseModel's __init__ to handle data validation
        self.tools = util_tools + transfer_tools
        if self.tools:
            self.llm = self.llm.bind_tools(self.tools)
        # self.llm_with_tools = llm.bind_tools(self.tools)
        self.util_tools_map = {tool.name: tool for tool in self.util_tools}
        self.transfer_tools_map = {tool.name: tool for tool in self.transfer_tools}

    def invoke(self, messages):
        new_agent_name = self.name
        self.messages = [SystemMessage(self.sys_prompt)]
        self.messages.extend(messages)
        # ai_msg = self.llm_with_tools.invoke(self.messages)
        ai_msg = self.llm.invoke(self.messages)
        self.messages.append(ai_msg)        
        while ai_msg.tool_calls:
            for tool_call in ai_msg.tool_calls:
                tool_name = tool_call["name"].lower()
                selected_tool = self.util_tools_map.get(tool_name) or self.transfer_tools_map.get(tool_name)
                if selected_tool:
                    tool_msg = selected_tool.invoke(tool_call)
                    self.messages.append(tool_msg)
                    if selected_tool in self.transfer_tools_map.values():
                        new_agent_name = tool_msg.content                
            # ai_msg = self.llm_with_tools.invoke(self.messages)
            ai_msg = self.llm.invoke(self.messages)
            self.messages.append(ai_msg)
                    
        return self.messages[1:], new_agent_name # don't return the system message