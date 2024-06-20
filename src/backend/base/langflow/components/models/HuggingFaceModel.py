from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

from langflow.base.constants import STREAM_INFO_TEXT
from langflow.base.models.model import LCModelComponent
from langflow.field_typing import LanguageModel, Text
from langflow.io import BoolInput, DictInput, DropdownInput, MessageInput, Output, SecretStrInput, StrInput


class HuggingFaceEndpointsComponent(LCModelComponent):
    display_name: str = "Hugging Face API"
    description: str = "Generate text using Hugging Face Inference APIs."
    icon = "HuggingFace"

    inputs = [
        MessageInput(name="input_value", display_name="Input"),
        SecretStrInput(name="endpoint_url", display_name="Endpoint URL", password=True),
        DropdownInput(
            name="task",
            display_name="Task",
            options=["text2text-generation", "text-generation", "summarization"],
        ),
        SecretStrInput(name="huggingfacehub_api_token", display_name="API token", password=True),
        DictInput(name="model_kwargs", display_name="Model Keyword Arguments", advanced=True),
        BoolInput(name="stream", display_name="Stream", info=STREAM_INFO_TEXT, advanced=True),
        StrInput(
            name="system_message",
            display_name="System Message",
            info="System message to pass to the model.",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Text", name="text_output", method="text_response"),
        Output(display_name="Language Model", name="model_output", method="build_model"),
    ]

    def text_response(self) -> Text:
        input_value = self.input_value
        stream = self.stream
        system_message = self.system_message
        output = self.build_model()
        result = self.get_chat_result(output, stream, input_value, system_message)
        self.status = result
        return result

    def build_model(self) -> LanguageModel:
        endpoint_url = self.endpoint_url
        task = self.task
        huggingfacehub_api_token = self.huggingfacehub_api_token
        model_kwargs = self.model_kwargs or {}

        try:
            llm = HuggingFaceEndpoint(
                endpoint_url=endpoint_url,
                task=task,
                huggingfacehub_api_token=huggingfacehub_api_token,
                model_kwargs=model_kwargs,
            )
        except Exception as e:
            raise ValueError("Could not connect to HuggingFace Endpoints API.") from e

        output = ChatHuggingFace(llm=llm)
        return output
