# langchain-opengradient

This package contains the LangChain integration with OpenGradient. 

More information about OpenGradient can be found [here](https://docs.opengradient.ai/).

## Installation

```bash
pip install -U langchain-opengradient
```

And you should configure credentials by setting the following environment variables:

```bash
OPENGRADIENT_PRIVATE_KEY - Your OpenGradient private API key
```

If you do not have an OpenGradient private key configured you can get one by running
```bash
pip install opengradient
opengradient config init
```

## Toolkits
`OpenGradientToolkit` class provides a set of functions for creating tools that integrate OpenGradient models and workflows into LangChain agents.

```python
from langchain_opengradient import OpenGradientToolkit
import opengradient as og
from pydantic import BaseModel, Field
from typing import List

# Initialize the toolkit
# Either set the environment variable "OPENGRADIENT_PRIVATE_KEY"
# or directly pass in private key.
toolkit = OpenGradientToolkit(private_key="MY_PRIVATE_KEY")

# Example 1: Create a volatility prediction tool with no input schema
def model_input_provider():
    return {
        "open_high_low_close": [
            [2535.79, 2535.79, 2505.37, 2515.36],
            [2515.37, 2516.37, 2497.27, 2506.94],
            # ... more price data
        ]
    }
    
def output_formatter(inference_result):
    return format(float(inference_result.model_output["Y"].item()), ".3%")
    
volatility_tool = toolkit.create_run_model_tool(
    model_cid="QmRhcpDXfYCKsimTmJYrAVM4Bbvck59Zb2onj3MHv9Kw5N",
    tool_name="eth_usdt_volatility",
    model_input_provider=model_input_provider,
    model_output_formatter=output_formatter,
    tool_description="Generates volatility measurement for ETH/USDT",
    inference_mode=og.InferenceMode.VANILLA,
)

# Example 2: Create a tool with an input schema
class VolatilityInputSchema(BaseModel):
    token: str = Field(description="Token name (e.g., 'ethereum' or 'bitcoin')")

def model_input_provider_with_schema(**llm_input):
    token = llm_input.get("token")
    # Fetch appropriate data based on token
    if token == "bitcoin":
        return {"price_series": [100001.1, 100013.2, 100149.2, 99998.1]}    # Replace with live data
    elif token == "ethereum":
        return {"price_series": [2010.1, 2012.3, 2020.1, 2019.2]}           # Replace with live data
    else:  # ethereum
        raise ValueError("Received unexpected token")

token_volatility_tool = toolkit.create_run_model_tool(
    model_cid="QmZdSfHWGJyzBiB2K98egzu3MypPcv4R1ASypUxwZ1MFUG",
    tool_name="token_volatility",
    model_input_provider=model_input_provider_with_schema,
    model_output_formatter=lambda x: format(float(x.model_output["std"].item()), ".3%"),
    tool_input_schema=VolatilityInputSchema,
    tool_description="Measures return volatility for specified token"
)

# Example 3: Create a workflow reading tool
workflow_tool = toolkit.create_read_workflow_tool(
    workflow_contract_address="0x58826c6dc9A608238d9d57a65bDd50EcaE27FE99",
    tool_name="ETH_Price_Forecast",
    tool_description="Reads latest forecast for ETH price",
    output_formatter=lambda x: f"Price change forecast: {
        format(float(x.numbers['regression_output'].item()), '.2%')
        }"
)

# Add tools to the toolkit
toolkit.add_tool(volatility_tool)
toolkit.add_tool(token_volatility_tool)
toolkit.add_tool(workflow_tool)

# Get all tools
tools = toolkit.get_tools()

# Use with an agent
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
agent_executor = create_react_agent(llm, tools)

example_query ="What's the current volatility of ETH/USDT?"

events = agent_executor.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
    )

for event in events:
    event["messages"][-1].pretty_print()
```