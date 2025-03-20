# AgentFleet

A Python package for managing AI agents and chatrooms that work with LLM-based capabilities.

## Installation

```bash
pip install agentfleet
```

## Usage

```python
from agentfleet import Agent, Chatroom, create_chatroom

# Example: Create an agent
from langchain_openai import ChatOpenAI
llm = ChatOpenAI()
agent = Agent(name="Assistant", llm=llm, sys_prompt="You are a helpful assistant")

# Example: Set up a chatroom
chatroom = Chatroom(llm=llm, agents=[agent], current_agent=agent)
```

## Features

- Create AI agents with different capabilities
- Build chatrooms with multiple specialized agents
- Transfer conversation control between agents
- Maintain conversation state across interactions

## Example Use Cases

AgentFleet includes several example applications:

1. **Customer Service** - Specialized agents for order placement and refund processing
2. **English Tutor** - Grammar and vocabulary tutor agents that collaborate
3. **Image OCR** - Extract and process text from images
4. **Course Planning** - Generate educational course plans

## Supported LLM Providers

AgentFleet supports multiple LLM providers:

- Azure OpenAI (ChatGPT, GPT-4)
- Zhipu AI (GLM-4)
- Yi (Yi-Large, Yi-Lightning)
- DeepSeek (DeepSeek-V3, DeepSeek-R1)

## License

MIT License

Copyright (c) 2025 Wei Zhou

## Contributing

Individual Contributor: Wei Zhou

We welcome contributions! Please review our contribution guidelines for details on our code of conduct, and the process for submitting pull requests.
