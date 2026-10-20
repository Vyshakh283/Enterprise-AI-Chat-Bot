from Backend.app.Services.ingestion.processor.base_processor import (
    BaseProcessor,
)
from Backend.app.Services.ingestion.processor.text_processor import (
    TextProcessor,
)
from Backend.app.Services.ingestion.processor.ocr_processor import (
    OCRProcessor,
)
from Backend.app.Services.ingestion.processor.idp_processor import (
    IDPProcessor,
)
from Backend.app.Services.ingestion.processor.vlm_processor import (
    VLMProcessor,
)
from Backend.app.Services.ingestion.processor.mixed_content_processor import (
    MixedContentProcessor,
)

from Backend.app.Services.ingestion.processor.empty_content_processor import (
    EmptyContentProcessor,
)


class ProcessorRegistry:
    """
    Central registry for document-content processors.

    The registry maps processing strategies to
    their corresponding processor implementations.

    Responsibilities:
    - Register processors
    - Retrieve processors by strategy
    - Keep processor selection centralized

    The registry does NOT:
    - Process document content
    - Analyze documents
    - Perform routing decisions
    """

    def __init__(self) -> None:
        self._processors: dict[
            str,
            BaseProcessor,
        ] = {}

        self._register_default_processors()

    def _register_default_processors(self) -> None:
        """
        Register the processors currently supported
        by the ingestion pipeline.
        """

        self.register(
            "text_processing",
            TextProcessor(),
        )

        self.register(
            "ocr",
            OCRProcessor(),
        )

        self.register(
            "idp",
            IDPProcessor(),
        )

        self.register(
            "vlm",
            VLMProcessor(),
        )
        self.register(
            "mixed_content_processing",
            MixedContentProcessor(),
        )

        self.register(
            "empty_content",
            EmptyContentProcessor(),
        )

    def register(
        self,
        strategy: str,
        processor: BaseProcessor,
    ) -> None:
        """
        Register a processor for a processing strategy.
        """

        if not isinstance(strategy, str):
            raise TypeError(
                "strategy must be a string."
            )

        if not strategy.strip():
            raise ValueError(
                "strategy cannot be empty."
            )

        if not isinstance(
            processor,
            BaseProcessor,
        ):
            raise TypeError(
                "processor must inherit from BaseProcessor."
            )

        self._processors[strategy] = processor

    def get(
        self,
        strategy: str,
    ) -> BaseProcessor:
        """
        Retrieve a processor for a processing strategy.
        """

        if not isinstance(strategy, str):
            raise TypeError(
                "strategy must be a string."
            )

        if strategy not in self._processors:
            raise ValueError(
                f"No processor registered for "
                f"strategy: {strategy}"
            )

        return self._processors[strategy]