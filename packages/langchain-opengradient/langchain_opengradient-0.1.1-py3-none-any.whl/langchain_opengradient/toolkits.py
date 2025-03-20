"""OpenGradient toolkits."""

import os
from typing import Callable, List, Optional, Type

import opengradient as og  # type: ignore
from langchain_core.tools import BaseTool, BaseToolkit
from opengradient import InferenceResult  # type: ignore
from opengradient.alphasense import (  # type: ignore
    ToolType,
    create_read_workflow_tool,
    create_run_model_tool,
)
from pydantic import BaseModel, Field


class OpenGradientToolkit(BaseToolkit):
    """OpenGradient toolkit.

    Setup:
    Install ``langchain-opengradient`` and set environment variable ``OPENGRADIENT_PRIVATE_KEY``.

    .. code-block:: bash

        pip install -U langchain-opengradient
        export OPENGRADIENT_PRIVATE_KEY="your-api-key"

    Key init args:
        private_key: str
            Your OpenGradient API private key for authentication. If not provided,
            the OPENGRADIENT_PRIVATE_KEY environment variable will be used.

            You can get your own OpenGradient API key by running
            .. code-block:: bash

                opengradient config init

    Instantiate:
        .. code-block:: python

            from langchain_opengradient import OpenGradientToolkit

            toolkit = OpenGradientToolkit(
                private_key="your-api-key"  # Optional if env var is set
            )

    Tools:
        .. code-block:: python

            toolkit.get_tools()

        .. code-block:: none

            [
                one_hour_eth_usdt_volatility({}): Generate the live 1 hour volatility measurement for the ETH/USDT trading pair.,
                ETH_Price_Forecast({}): Reads latest forecast for ETH price
            ]

    Use within an agent:
        .. code-block:: python

            from langgraph.prebuilt import create_react_agent
            from langchain_openai import ChatOpenAI

            llm = ChatOpenAI()
            toolkit = OpenGradientToolkit()

            # Create a volatility measurement tool for ETH/USDT
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
            )

            toolkit.add_tool(volatility_tool)
            tools = toolkit.get_tools()

            agent_executor = create_react_agent(llm, tools)

            example_query = "What's the current volatility of ETH/USDT?"

            events = agent_executor.stream(
                {"messages": [("user", example_query)]},
                stream_mode="values",
            )
            for event in events:
                event["messages"][-1].pretty_print()

        .. code-block:: none
        Example Output:
        ================================ Human Message =================================

        What's the current volatility of ETH/USDT?
        ================================== Ai Message ==================================
        Tool Calls:
        eth_usdt_volatility (chatcmpl-tool-92d6de9b46454d55aa5e845dc5a6ed84)
        Call ID: chatcmpl-tool-92d6de9b46454d55aa5e845dc5a6ed84
        Args:
        ================================= Tool Message =================================
        Name: eth_usdt_volatility

        0.038%
        ================================== Ai Message ==================================

        The most recent 1 hour volatility measure for the trading pair ETH/USDT is 0.038%.
    """  # noqa: E501

    model_config = {"arbitrary_types_allowed": True}
    client: Optional[og.client.Client] = Field(
        default=None, description="OpenGradient client"
    )
    tools: List[BaseTool] = Field(
        default_factory=list,
        description="List of OpenGradient tools currently in the toolkit",
    )

    def __init__(self, private_key: str | None = None):
        super().__init__()

        # Initialize OpenGradient client
        private_key = private_key or os.getenv("OPENGRADIENT_PRIVATE_KEY")
        if not private_key:
            raise ValueError("OPENGRADIENT_PRIVATE_KEY environment variable is not set")

        self.client = og.init(private_key=private_key, email=None, password=None)
        self.tools = []

    def get_tools(self) -> List[BaseTool]:
        """Get list of tools available in OpenGradient toolkit."""
        return self.tools

    def add_tool(self, tool: BaseTool) -> None:
        """Add tool to the list of tools for the OpenGradient Agentkit."""
        self.tools.append(tool)

    def create_run_model_tool(
        self,
        model_cid: str,
        tool_name: str,
        model_input_provider: Callable[..., InferenceResult],
        model_output_formatter: Callable[..., str],
        tool_input_schema: Optional[Type[BaseModel]] = None,
        tool_description: str = "Executes the given ML model",
        inference_mode: og.InferenceMode = og.InferenceMode.VANILLA,
    ) -> BaseTool:
        """
        Wrapper for create_run_model_tool from OpenGradient AlphaSense library.

        This function creates a langchain compatible tool to run inferences on the
        OpenGradient network.

        Args:
            model_cid (str): The CID of the OpenGradient model to be executed.
            tool_name (str): The name to assign to the created tool. This will be used
                to identify and invoke the tool within the agent.
            model_input_provider (Callable): A function that takes in the 
                tool_input_schema with arguments filled by the agent and returns input 
                data required by the model.

                The function should return data in a format compatible with the model's 
                expectations.
            model_output_formatter (Callable[..., str]): A function that takes the 
                output of the OpenGradient infer method (with type InferenceResult) and 
                formats it into a string.

                This is required to ensure the output is compatible with the tool 
                framework.

                InferenceResult has attributes:
                    * transaction_hash (str): Blockchain hash for the transaction
                    * model_output (Dict[str, np.ndarray]): Output of the ONNX model
            tool_input_schema (Type[BaseModel], optional): A Pydantic BaseModel class 
                defining the input schema.

                The defined schema will be used as input keyword arguments for the 
                `model_input_provider` function. If no arguments are required for 
                the `model_input_provider` function then this schema can be 
                unspecified.

                Default is None -- an empty schema will be provided for LangChain.
            tool_description (str, optional): A description of what the tool does.
                Defaults to "Executes the given ML model".
            inference_mode (og.InferenceMode, optional): The inference mode to use 
                when running the model. Defaults to VANILLA.
                
        Example usage:
            from og_langchain.toolkits import OpenGradientToolkit
            import opengradient as og

            toolkit = OpenGradientToolkit()

            class ExampleInputSchema(BaseModel):
                open_high_low_close: List[List] = Field(
                    description="[Open, High, Low, Close] "
                                "prices for the 10 most recent"
                    )

            def GetInputData():
                ... User defined function that gathers live-data. ...

            eth_volatility_tool = toolkit.create_run_model_tool(
                model_cid = "QmRhcpDXfYCKsimTmJYrAVM4Bbvck59Zb2onj3MHv9Kw5N",
                tool_name = "one_hour_eth_usdt_volatility",
                model_input_provider = GetInputData(),
                model_output_formatter = lambda x: format(
                    float(x.model_output["Y"].item()),
                    ".3%"
                    ),
                tool_input_schema = ExampleInputSchema,
                tool_description = "Generates the volatility measurement for the "\
                                   "ETH/USDT trading pair based on the latest 10 "\
                                   "measurements in the last hour.",
                inference_mode = og.InferenceMode.VANILLA,
            )

            toolkit.add_tool(eth_volatility_tool)

            for tool in toolkit.get_tools():
                print(tool)
        """
        tool = create_run_model_tool(
            tool_type=ToolType.LANGCHAIN,
            model_cid=model_cid,
            tool_name=tool_name,
            model_input_provider=model_input_provider,
            model_output_formatter=model_output_formatter,
            tool_input_schema=tool_input_schema,
            tool_description=tool_description,
            inference_mode=inference_mode,
        )

        return tool

    def create_read_workflow_tool(
        self,
        workflow_contract_address: str,
        tool_name: str,
        tool_description: str,
        output_formatter: Callable[..., str] = lambda x: x,
    ) -> BaseTool:
        """
        Wrapper for create_read_workflow_tool from OpenGradient AlphaSense library.

        This function creates a langchain compatible tool to read workflows on the
        OpenGradient network.

        Args:
            workflow_contract_address (str): The address of the workflow contract
            from which to read results.
            tool_name (str): The name to assign to the created tool. This will be
                used to identify and invoke the tool within the agent.
            tool_description (str): A description of what the tool does and how
                it processes the workflow results.
            output_formatter (Callable[..., str], optional): A function that takes
                the workflow output and formats it into a string. This ensures the
                output is compatible with the tool framework.

                Default returns string as is.

        Example usage:
            from og_langchain.toolkits import OpenGradientToolkit

            toolkit = OpenGradientToolkit()
            btc_workflow_tool = toolkit.create_read_workflow_tool(
                tool_type=ToolType.LANGCHAIN,
                workflow_contract_address="0x6e0641925b845A1ca8aA9a890C4DEF388E9197e0",
                tool_name="ETH_Price_Forecast",
                tool_description="Reads latest forecast for ETH price",
                output_formatter=lambda x: x,
            )

            toolkit.add_tool(btc_workflow_tool)

            for tool in toolkit.get_tools():
                print(tool)
        """
        tool = create_read_workflow_tool(
            tool_type=ToolType.LANGCHAIN,
            workflow_contract_address=workflow_contract_address,
            tool_name=tool_name,
            tool_description=tool_description,
            output_formatter=output_formatter,
        )

        return tool
