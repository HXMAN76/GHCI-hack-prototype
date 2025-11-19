from typing import Any, Dict, Optional, Text


class LLMCommandGenerator:
    """Very small import-safe placeholder for `LLMCommandGenerator`.

    This implementation intentionally avoids importing Rasa internals so
    the module can be imported by the training graph. It performs no
    processing — replace with real LLM logic later.
    """

    name = "LLMCommandGenerator"
    provides = []
    requires = []
    defaults: Dict[Text, Any] = {}
    language_list = None

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        self.component_config = component_config or {}

    def train(self, training_data: Any, cfg: Any, **kwargs) -> None:
        return None

    def process(self, message: Any, **kwargs) -> None:
        return None

    @classmethod
    def load(
        cls, meta: Dict[Text, Any], model_dir: Optional[Text], model_metadata=None, cached_component=None, **kwargs
    ) -> "LLMCommandGenerator":
        return cls(meta)

    def persist(self, model_dir: Text) -> Dict[Text, Any]:
        return {}
