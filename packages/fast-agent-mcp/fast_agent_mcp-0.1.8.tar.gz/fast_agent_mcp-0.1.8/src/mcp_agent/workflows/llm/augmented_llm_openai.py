import json
import os
from typing import Iterable, List, Type
from mcp.types import PromptMessage
from openai import OpenAI, AuthenticationError

# from openai.types.beta.chat import
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionContentPartParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionContentPartRefusalParam,
    ChatCompletionMessage,
    ChatCompletionSystemMessageParam,
    ChatCompletionToolParam,
    ChatCompletionToolMessageParam,
    ChatCompletionUserMessageParam,
)
from mcp.types import (
    CallToolRequestParams,
    CallToolRequest,
    CallToolResult,
    EmbeddedResource,
    ImageContent,
    TextContent,
    TextResourceContents,
)

from mcp_agent.workflows.llm.augmented_llm import (
    AugmentedLLM,
    ModelT,
    MCPMessageParam,
    MCPMessageResult,
    ProviderToMCPConverter,
    RequestParams,
)
from mcp_agent.core.exceptions import ProviderKeyError
from mcp_agent.logging.logger import get_logger
from rich.text import Text

_logger = get_logger(__name__)

DEFAULT_OPENAI_MODEL = "gpt-4o"
DEFAULT_REASONING_EFFORT = "medium"


class OpenAIAugmentedLLM(
    AugmentedLLM[ChatCompletionMessageParam, ChatCompletionMessage]
):
    """
    The basic building block of agentic systems is an LLM enhanced with augmentations
    such as retrieval, tools, and memory provided from a collection of MCP servers.
    This implementation uses OpenAI's ChatCompletion as the LLM.
    """

    def __init__(self, *args, **kwargs):
        # Set type_converter before calling super().__init__
        if "type_converter" not in kwargs:
            kwargs["type_converter"] = MCPOpenAITypeConverter

        super().__init__(*args, **kwargs)

        self.provider = "OpenAI"
        # Initialize logger with name if available
        self.logger = get_logger(f"{__name__}.{self.name}" if self.name else __name__)

        # Set up reasoning-related attributes
        self._reasoning_effort = kwargs.get("reasoning_effort", None)
        if self.context and self.context.config and self.context.config.openai:
            if self._reasoning_effort is None and hasattr(
                self.context.config.openai, "reasoning_effort"
            ):
                self._reasoning_effort = self.context.config.openai.reasoning_effort

        # Determine if we're using a reasoning model
        chosen_model = (
            self.default_request_params.model if self.default_request_params else None
        )
        self._reasoning = chosen_model and (
            chosen_model.startswith("o3") or chosen_model.startswith("o1")
        )
        if self._reasoning:
            self.logger.info(
                f"Using reasoning model '{chosen_model}' with '{self._reasoning_effort}' reasoning effort"
            )

    def _initialize_default_params(self, kwargs: dict) -> RequestParams:
        """Initialize OpenAI-specific default parameters"""
        chosen_model = kwargs.get("model", DEFAULT_OPENAI_MODEL)

        # Get default model from config if available
        if self.context and self.context.config and self.context.config.openai:
            if hasattr(self.context.config.openai, "default_model"):
                chosen_model = self.context.config.openai.default_model

        return RequestParams(
            model=chosen_model,
            modelPreferences=self.model_preferences,
            systemPrompt=self.instruction,
            parallel_tool_calls=True,
            max_iterations=10,
            use_history=True,
        )

    def _api_key(self) -> str:
        config = self.context.config
        api_key = None

        if hasattr(config, "openai") and config.openai:
            api_key = config.openai.api_key
            if api_key == "<your-api-key-here>":
                api_key = None

        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ProviderKeyError(
                "OpenAI API key not configured",
                "The OpenAI API key is required but not set.\n"
                "Add it to your configuration file under openai.api_key\n"
                "Or set the OPENAI_API_KEY environment variable",
            )
        return api_key

    def _base_url(self) -> str:
        return (
            self.context.config.openai.base_url if self.context.config.openai else None
        )

    async def generate(
        self,
        message,
        request_params: RequestParams | None = None,
        response_model: Type[ModelT] | None = None,
    ) -> List[ChatCompletionMessage]:
        """
        Process a query using an LLM and available tools.
        The default implementation uses OpenAI's ChatCompletion as the LLM.
        Override this method to use a different LLM.
        """

        try:
            openai_client = OpenAI(api_key=self._api_key(), base_url=self._base_url())
            messages: List[ChatCompletionMessageParam] = []
            params = self.get_request_params(request_params)
        except AuthenticationError as e:
            raise ProviderKeyError(
                "Invalid OpenAI API key",
                "The configured OpenAI API key was rejected.\n"
                "Please check that your API key is valid and not expired.",
            ) from e

        system_prompt = self.instruction or params.systemPrompt
        if system_prompt:
            messages.append(
                ChatCompletionSystemMessageParam(role="system", content=system_prompt)
            )

        # Always include prompt messages, but only include conversation history
        # if use_history is True
        messages.extend(self.history.get(include_history=params.use_history))

        if isinstance(message, str):
            messages.append(
                ChatCompletionUserMessageParam(role="user", content=message)
            )
        elif isinstance(message, list):
            messages.extend(message)
        else:
            messages.append(message)

        response = await self.aggregator.list_tools()
        available_tools: List[ChatCompletionToolParam] = [
            ChatCompletionToolParam(
                type="function",
                function={
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                    # TODO: saqadri - determine if we should specify "strict" to True by default
                },
            )
            for tool in response.tools
        ]
        if not available_tools:
            available_tools = []

        responses: List[ChatCompletionMessage] = []
        model = await self.select_model(params)
        chat_turn = len(messages) // 2
        if self._reasoning:
            self.show_user_message(
                str(message), f"{model} ({self._reasoning_effort})", chat_turn
            )
        else:
            self.show_user_message(str(message), model, chat_turn)

        for i in range(params.max_iterations):
            arguments = {
                "model": model or "gpt-4o",
                "messages": messages,
                "stop": params.stopSequences,
                "tools": available_tools,
            }
            if self._reasoning:
                arguments = {
                    **arguments,
                    "max_completion_tokens": params.maxTokens,
                    "reasoning_effort": self._reasoning_effort,
                }
            else:
                arguments = {**arguments, "max_tokens": params.maxTokens}
                if available_tools:
                    arguments["parallel_tool_calls"] = params.parallel_tool_calls

            if params.metadata:
                arguments = {**arguments, **params.metadata}

            self.logger.debug(f"{arguments}")
            self._log_chat_progress(chat_turn, model=model)

            if response_model is None:
                executor_result = await self.executor.execute(
                    openai_client.chat.completions.create, **arguments
                )
            else:
                executor_result = await self.executor.execute(
                    openai_client.beta.chat.completions.parse,
                    **arguments,
                    response_format=response_model,
                )

            response = executor_result[0]

            self.logger.debug(
                "OpenAI ChatCompletion response:",
                data=response,
            )

            if isinstance(response, AuthenticationError):
                raise ProviderKeyError(
                    "Invalid OpenAI API key",
                    "The configured OpenAI API key was rejected.\n"
                    "Please check that your API key is valid and not expired.",
                ) from response
            elif isinstance(response, BaseException):
                self.logger.error(f"Error: {response}")
                break

            if not response.choices or len(response.choices) == 0:
                # No response from the model, we're done
                break

            # TODO: saqadri - handle multiple choices for more complex interactions.
            # Keeping it simple for now because multiple choices will also complicate memory management
            choice = response.choices[0]
            message = choice.message
            responses.append(message)

            converted_message = self.convert_message_to_message_param(
                message, name=self.name
            )
            messages.append(converted_message)
            message_text = converted_message.content
            if (
                choice.finish_reason in ["tool_calls", "function_call"]
                and message.tool_calls
            ):
                if message_text:
                    await self.show_assistant_message(
                        message_text,
                        message.tool_calls[
                            0
                        ].function.name,  # TODO support displaying multiple tool calls
                    )
                else:
                    await self.show_assistant_message(
                        Text(
                            "the assistant requested tool calls",
                            style="dim green italic",
                        ),
                        message.tool_calls[0].function.name,
                    )

                # Execute all tool calls in parallel.
                tool_tasks = []
                for tool_call in message.tool_calls:
                    self.show_tool_call(
                        available_tools,
                        tool_call.function.name,
                        tool_call.function.arguments,
                    )
                    tool_tasks.append(self.execute_tool_call(tool_call))
                # Wait for all tool calls to complete.
                tool_results = await self.executor.execute(*tool_tasks)
                self.logger.debug(
                    f"Iteration {i}: Tool call results: {str(tool_results) if tool_results else 'None'}"
                )
                # Add non-None results to messages.
                for result in tool_results:
                    if isinstance(result, BaseException):
                        self.logger.error(
                            f"Warning: Unexpected error during tool execution: {result}. Continuing..."
                        )
                        continue
                    if result is not None:
                        self.show_oai_tool_result(str(result["content"]))
                        messages.append(result)
            elif choice.finish_reason == "length":
                # We have reached the max tokens limit
                self.logger.debug(
                    f"Iteration {i}: Stopping because finish_reason is 'length'"
                )
                if request_params and request_params.maxTokens is not None:
                    message_text = Text(
                        f"the assistant has reached the maximum token limit ({request_params.maxTokens})",
                        style="dim green italic",
                    )
                else:
                    message_text = Text(
                        "the assistant has reached the maximum token limit",
                        style="dim green italic",
                    )

                await self.show_assistant_message(message_text)
                # TODO: saqadri - would be useful to return the reason for stopping to the caller
                break
            elif choice.finish_reason == "content_filter":
                # The response was filtered by the content filter
                self.logger.debug(
                    f"Iteration {i}: Stopping because finish_reason is 'content_filter'"
                )
                # TODO: saqadri - would be useful to return the reason for stopping to the caller
                break
            elif choice.finish_reason == "stop":
                self.logger.debug(
                    f"Iteration {i}: Stopping because finish_reason is 'stop'"
                )
                if message_text:
                    await self.show_assistant_message(message_text, "")
                break

        # Only save the new conversation messages to history if use_history is true
        # Keep the prompt messages separate
        if params.use_history:
            # Get current prompt messages
            prompt_messages = self.history.get(include_history=False)

            # Calculate new conversation messages (excluding prompts)
            new_messages = messages[len(prompt_messages) :]

            # Update conversation history
            self.history.set(new_messages)

        self._log_chat_finished(model=model)

        return responses

    async def generate_str(
        self,
        message,
        request_params: RequestParams | None = None,
    ):
        """
        Process a query using an LLM and available tools.
        The default implementation uses OpenAI's ChatCompletion as the LLM.
        Override this method to use a different LLM.
        """
        responses = await self.generate(
            message=message,
            request_params=request_params,
        )

        final_text: List[str] = []

        for response in responses:
            content = response.content
            if not content:
                continue

            if isinstance(content, str):
                final_text.append(content)
                continue

        return "\n".join(final_text)

    async def generate_structured(
        self,
        message,
        response_model: Type[ModelT],
        request_params: RequestParams | None = None,
    ) -> ModelT:
        responses = await self.generate(
            message=message,
            request_params=request_params,
            response_model=response_model,
        )
        return responses[0].parsed

        # return response_model.model_validate(
        #     from_json(responses[0].content, allow_partial=True)
        # )
        # part1 = from_json(response, allow_partial=True)
        # return response_model.model_validate(part1)

        # TODO -- would prefer to use the OpenAI message[0].parsed function here
        # return response_model.model_validate(from_json(response, allow_partial=True))

    async def pre_tool_call(self, tool_call_id: str | None, request: CallToolRequest):
        return request

    async def post_tool_call(
        self, tool_call_id: str | None, request: CallToolRequest, result: CallToolResult
    ):
        return result

    async def execute_tool_call(
        self,
        tool_call: ChatCompletionToolParam,
    ) -> ChatCompletionToolMessageParam | None:
        """
        Execute a single tool call and return the result message.
        Returns None if there's no content to add to messages.
        """
        tool_name = tool_call.function.name
        tool_args_str = tool_call.function.arguments
        tool_call_id = tool_call.id
        tool_args = {}

        try:
            if tool_args_str:
                tool_args = json.loads(tool_args_str)
        except json.JSONDecodeError as e:
            return ChatCompletionToolMessageParam(
                role="tool",
                tool_call_id=tool_call_id,
                content=f"Invalid JSON provided in tool call arguments for '{tool_name}'. Failed to load JSON: {str(e)}",
            )

        tool_call_request = CallToolRequest(
            method="tools/call",
            params=CallToolRequestParams(name=tool_name, arguments=tool_args),
        )

        result = await self.call_tool(
            request=tool_call_request, tool_call_id=tool_call_id
        )

        if result.content:
            return ChatCompletionToolMessageParam(
                role="tool",
                tool_call_id=tool_call_id,
                content=[mcp_content_to_openai_content(c) for c in result.content],
            )

        return None

    def message_param_str(self, message: ChatCompletionMessageParam) -> str:
        """Convert an input message to a string representation."""
        if message.get("content"):
            content = message["content"]
            if isinstance(content, str):
                return content
            else:  # content is a list
                final_text: List[str] = []
                for part in content:
                    text_part = part.get("text")
                    if text_part:
                        final_text.append(str(text_part))
                    else:
                        final_text.append(str(part))

                return "\n".join(final_text)

        return str(message)

    def message_str(self, message: ChatCompletionMessage) -> str:
        """Convert an output message to a string representation."""
        content = message.content
        if content:
            return content

        return str(message)


class MCPOpenAITypeConverter(
    ProviderToMCPConverter[ChatCompletionMessageParam, ChatCompletionMessage]
):
    """
    Convert between OpenAI and MCP types.
    """

    @classmethod
    def from_mcp_message_result(cls, result: MCPMessageResult) -> ChatCompletionMessage:
        # MCPMessageResult -> ChatCompletionMessage
        if result.role != "assistant":
            raise ValueError(
                f"Expected role to be 'assistant' but got '{result.role}' instead."
            )

        return ChatCompletionMessage(
            role="assistant",
            content=result.content.text or str(result.context),
            # Lossy conversion for the following fields:
            # result.model
            # result.stopReason
        )

    @classmethod
    def to_mcp_message_result(cls, result: ChatCompletionMessage) -> MCPMessageResult:
        # ChatCompletionMessage -> MCPMessageResult
        return MCPMessageResult(
            role=result.role,
            content=TextContent(type="text", text=result.content),
            model=None,
            stopReason=None,
            # extras for ChatCompletionMessage fields
            **result.model_dump(exclude={"role", "content"}),
        )

    @classmethod
    def from_mcp_message_param(
        cls, param: MCPMessageParam
    ) -> ChatCompletionMessageParam:
        # MCPMessageParam -> ChatCompletionMessageParam
        if param.role == "assistant":
            extras = param.model_dump(exclude={"role", "content"})
            return ChatCompletionAssistantMessageParam(
                role="assistant",
                content=mcp_content_to_openai_content(param.content),
                **extras,
            )
        elif param.role == "user":
            extras = param.model_dump(exclude={"role", "content"})
            return ChatCompletionUserMessageParam(
                role="user",
                content=mcp_content_to_openai_content(param.content),
                **extras,
            )
        else:
            raise ValueError(
                f"Unexpected role: {param.role}, MCP only supports 'assistant' and 'user'"
            )

    @classmethod
    def to_mcp_message_param(cls, param: ChatCompletionMessageParam) -> MCPMessageParam:
        # ChatCompletionMessage -> MCPMessageParam

        contents = openai_content_to_mcp_content(param.content)

        # TODO: saqadri - the mcp_content can have multiple elements
        # while sampling message content has a single content element
        # Right now we error out if there are > 1 elements in mcp_content
        # We need to handle this case properly going forward
        if len(contents) > 1:
            raise NotImplementedError(
                "Multiple content elements in a single message are not supported"
            )
        mcp_content: TextContent | ImageContent | EmbeddedResource = contents[0]

        if param.role == "assistant":
            return MCPMessageParam(
                role="assistant",
                content=mcp_content,
                **typed_dict_extras(param, ["role", "content"]),
            )
        elif param.role == "user":
            return MCPMessageParam(
                role="user",
                content=mcp_content,
                **typed_dict_extras(param, ["role", "content"]),
            )
        elif param.role == "tool":
            raise NotImplementedError(
                "Tool messages are not supported in SamplingMessage yet"
            )
        elif param.role == "system":
            raise NotImplementedError(
                "System messages are not supported in SamplingMessage yet"
            )
        elif param.role == "developer":
            raise NotImplementedError(
                "Developer messages are not supported in SamplingMessage yet"
            )
        elif param.role == "function":
            raise NotImplementedError(
                "Function messages are not supported in SamplingMessage yet"
            )
        else:
            raise ValueError(
                f"Unexpected role: {param.role}, MCP only supports 'assistant', 'user', 'tool', 'system', 'developer', and 'function'"
            )

    @classmethod
    def from_mcp_prompt_message(
        cls, message: PromptMessage
    ) -> ChatCompletionMessageParam:
        """Convert an MCP PromptMessage to an OpenAI ChatCompletionMessageParam."""

        # Extract content
        content = None
        if hasattr(message.content, "text"):
            content = message.content.text
        else:
            content = str(message.content)

        # Extract extras
        extras = message.model_dump(exclude={"role", "content"})

        if message.role == "user":
            return ChatCompletionUserMessageParam(
                role="user", content=content, **extras
            )
        elif message.role == "assistant":
            return ChatCompletionAssistantMessageParam(
                role="assistant", content=content, **extras
            )
        else:
            # Fall back to user for any unrecognized role, including "system"
            _logger.warning(
                f"Unsupported role '{message.role}' in PromptMessage. Falling back to 'user' role."
            )
            return ChatCompletionUserMessageParam(
                role="user", content=f"[{message.role.upper()}] {content}", **extras
            )


def mcp_content_to_openai_content(
    content: TextContent | ImageContent | EmbeddedResource,
) -> ChatCompletionContentPartTextParam:
    if isinstance(content, list):
        # Handle list of content items
        return ChatCompletionContentPartTextParam(
            type="text",
            text="\n".join(mcp_content_to_openai_content(c) for c in content),
        )

    if isinstance(content, TextContent):
        return ChatCompletionContentPartTextParam(type="text", text=content.text)
    elif isinstance(content, ImageContent):
        # Best effort to convert an image to text
        return ChatCompletionContentPartTextParam(
            type="text", text=f"{content.mimeType}:{content.data}"
        )
    elif isinstance(content, EmbeddedResource):
        if isinstance(content.resource, TextResourceContents):
            return ChatCompletionContentPartTextParam(
                type="text", text=content.resource.text
            )
        else:  # BlobResourceContents
            return ChatCompletionContentPartTextParam(
                type="text", text=f"{content.resource.mimeType}:{content.resource.blob}"
            )
    else:
        # Last effort to convert the content to a string
        return ChatCompletionContentPartTextParam(type="text", text=str(content))


def openai_content_to_mcp_content(
    content: str
    | Iterable[ChatCompletionContentPartParam | ChatCompletionContentPartRefusalParam],
) -> Iterable[TextContent | ImageContent | EmbeddedResource]:
    mcp_content = []

    if isinstance(content, str):
        mcp_content = [TextContent(type="text", text=content)]
    else:
        # TODO: saqadri - this is a best effort conversion, we should handle all possible content types
        for c in content:
            if c.type == "text":  # isinstance(c, ChatCompletionContentPartTextParam):
                mcp_content.append(
                    TextContent(
                        type="text", text=c.text, **typed_dict_extras(c, ["text"])
                    )
                )
            elif (
                c.type == "image_url"
            ):  # isinstance(c, ChatCompletionContentPartImageParam):
                raise NotImplementedError("Image content conversion not implemented")
                # TODO: saqadri - need to download the image into a base64-encoded string
                # Download image from c.image_url
                # return ImageContent(
                #     type="image",
                #     data=downloaded_image,
                #     **c
                # )
            elif (
                c.type == "input_audio"
            ):  # isinstance(c, ChatCompletionContentPartInputAudioParam):
                raise NotImplementedError("Audio content conversion not implemented")
            elif (
                c.type == "refusal"
            ):  # isinstance(c, ChatCompletionContentPartRefusalParam):
                mcp_content.append(
                    TextContent(
                        type="text", text=c.refusal, **typed_dict_extras(c, ["refusal"])
                    )
                )
            else:
                raise ValueError(f"Unexpected content type: {c.type}")

    return mcp_content


def typed_dict_extras(d: dict, exclude: List[str]):
    extras = {k: v for k, v in d.items() if k not in exclude}
    return extras
