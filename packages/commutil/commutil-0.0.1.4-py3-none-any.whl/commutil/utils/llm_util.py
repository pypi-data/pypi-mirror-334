from typing import Dict, Optional, Union, Iterator, List, Any
import functools
from datetime import datetime
from .import_util import lazy_load
from .debug_util import dbg


def format_messages(content):
    messages = []
    messages.append({"role": "user", "content": content})
    return messages


class OpenLLMChat:
    """A chat interface for large language models with optimized lazy loading."""

    def __init__(
            self,
            model_name: str,
            device: str = None,
            verbose: bool = False,
            trust_remote_code: bool = False,
            **kwargs
    ):
        """Initialize OpenLLMChat with lazy-loaded components"""
        self.verbose = verbose
        self._log("Initializing model: %s", model_name)
        self.start_time = datetime.now()

        # Store initialization parameters
        self.model_name = model_name
        self.device = device
        if self.device is None:
            self.device = self._get_default_device()
        self.trust_remote_code = trust_remote_code

        self.model_config = kwargs.get("model_config", {})
        self.tokenizer_config = kwargs.get("tokenizer_config", {})
        self.generate_config = kwargs.get("generate_config", {})

    def _log(self, message: str, *args) -> None:
        """Configurable logging function"""
        if not self.verbose:
            return
        from ..constants import YELLOW, RESET
        print(f"{YELLOW}[LLM] {message % args}{RESET}")

    @lazy_load
    def torch(self):
        """Lazy load PyTorch"""
        try:
            import torch
            self._log("PyTorch loaded successfully")
            return torch
        except ImportError:
            raise ImportError("PyTorch is required but not installed")

    @lazy_load
    def tokenizer(self):
        """Lazy load tokenizer"""
        try:
            from transformers import AutoTokenizer
            self._log("Loading tokenizer...")
            tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=self.trust_remote_code,
                **self.tokenizer_config
            )
            self._log("Tokenizer loaded successfully")
            return tokenizer
        except ImportError:
            raise ImportError("Transformers library is required")

    @lazy_load
    def model(self):
        """Lazy load model"""
        try:
            from transformers import (
                AutoModelForCausalLM,
                BitsAndBytesConfig,
                GPTQConfig
            )
            # Build kwargs
            self.model_config["trust_remote_code"] = self.trust_remote_code
            quantization = self.model_config.pop("quantization", None)

            self._log("Loading model: device=%s, quantization=%s", self.device, quantization)

            # Apply quantization if specified
            if quantization:
                if quantization == "8bit":
                    self.model_config["device_map"] = "auto"
                    self.model_config["quantization_config"] = BitsAndBytesConfig(load_in_8bit=True)
                    self._log("Using 8-bit quantization")
                elif quantization == "4bit":
                    self.model_config["device_map"] = "auto"
                    self.model_config["quantization_config"] = BitsAndBytesConfig(
                        load_in_4bit=True,
                        bnb_4bit_compute_dtype=self.torch.float16,
                        bnb_4bit_quant_type="nf4",
                        bnb_4bit_use_double_quant=True
                    )
                    self._log("Using 4-bit quantization")
                elif quantization == "gptq":
                    self.model_config["device_map"] = "auto"
                    self.model_config["quantization_config"] = GPTQConfig(bits=4)
                    self._log("Using GPTQ quantization")

            # Load the model
            model = AutoModelForCausalLM.from_pretrained(self.model_name, **self.model_config)
            # Move to device if needed
            # TODO check this
            if self.model_config.get("device_map", None) != "auto":
                model = model.to(self.device)
            model.eval()
            self._log("Model loaded successfully, took: %.2f seconds",
                      (datetime.now() - self.start_time).total_seconds())
            return model

        except ImportError as e:
            raise ImportError(f"Required library not found: {str(e)}")
        except Exception as e:
            self._log("Error loading model: %s", str(e))
            raise

    def _get_default_device(self) -> str:
        """Determine the best available device"""
        if self.torch.cuda.is_available():
            return "cuda"
        elif hasattr(self.torch.backends, "mps") and self.torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def chat(
            self,
            prompt: str,
            **kwargs
    ) -> Union[str, Iterator[str]]:
        # Set generation parameters
        self.generate_config.update({
            # "pad_token_id": self.tokenizer.eos_token_id,
            "output_attentions": True,
            "output_hidden_states": True,
            "output_scores": True,
            "return_dict_in_generate": True,
        })
        self.generate_config.update(**kwargs)  # 可以单独在这里改generate_kwargs，但不会影响默认的generate_kwargs

        # Prepare messages
        messages = []
        system_prompt = self.generate_config.get("system_prompt", None)
        if system_prompt is not None:
            messages.append({
                "role": "system",
                "content": system_prompt or system_prompt
            })
        messages.append({"role": "user", "content": prompt})

        if not self.tokenizer.chat_template:
            self.tokenizer.chat_template = self.tokenizer_config.get("chat_template_if_None", None)
        # if not self.tokenizer.pad_token_id:
        #     self.tokenizer.pad_token_id = self.tokenizer_config.eos_token_id

        formatted_prompt = self.tokenizer.apply_chat_template(messages, tokenize=False)
        self._log("Prompt: %s", formatted_prompt)

        inputs = self.tokenizer(formatted_prompt, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # TODO how attention mask works
        output = self.model.generate(**inputs, **self.generate_config)

        input_length = inputs["input_ids"].shape[1]
        response_ids = output.sequences[0, input_length:]
        response = self.tokenizer.decode(response_ids, skip_special_tokens=True)
        self._log("Response: %s", response)

        return response

    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "verbose": self.verbose,
            "model_name": self.model_name,
            "device": self.device,
            "trust_remote_code": self.trust_remote_code,
            "model_config": self.model_config,
            "tokenizer_config": self.tokenizer_config,
            "generate_config": self.generate_config,
        }
