import logging
from pathlib import Path
from typing import Any, List, Union, AsyncIterator, Iterator

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_community.document_loaders.helpers import detect_file_encodings

from loaders.utils import plant_uml_translate
from utils.ecore.parser import EcoreParser

logger = logging.getLogger(__name__)

class EcoreLoader(BaseLoader):
    """A loader for loading Ecore files.

    This class inherits from the BaseLoader class and provides methods to load Ecore files.

    Parameters
    ----------
    BaseLoader : type
        The base loader class.

    Attributes
    ----------
    mode : str
        The loading mode. Default is "single".
    serialization : str
        The serialization format. Default is "plantUML".
    file_path : Union[str, Path]
        The path to the Ecore file.

    Methods
    -------
    _get_elements() -> List
        Get the elements from the Ecore file.
    _get_metadata() -> dict
        Get the metadata of the Ecore file.
    lazy_load() -> Iterator[Document]
        Load the Ecore file lazily.
    """

    def __init__(self, file_path: Union[str, Path], mode: str = "single", serialization: str = "plantUML") -> None:
        """Initialize the EcoreLoader with the Ecore file path.

        Args:
            file_path (Union[str, Path]): The path to the Ecore file.
            mode (str, optional): The loading mode. Defaults to "single".
            serialization (str, optional): The serialization format. Defaults to "plantUML".

        """
        self.mode = mode
        self.serialization = serialization
        self.file_path = file_path
        self.ecore_parser = EcoreParser()
        self.plant_uml_translate = plant_uml_translate.PlantUMLTranslate()

    def _get_elements(self) -> List:
        """Get the elements from the Ecore file."""
        pass

    def _get_metadata(self) -> dict:
        """Get the metadata of the Ecore file."""
        pass

    def lazy_load(self) -> Iterator[Document]:
<<<<<<< Updated upstream
        """Load the Ecore file lazily.

        Returns:
            Iterator[Document]: An iterator of Document objects representing the loaded Ecore file.

        """
        # TODO: This versions basic mimic the TextLoader, but reading Ecore and converting to PlantUML. New features can be added here.
        text = ""
        try:
            self.ecore_parser.register_metamodel(self.file_path)
            contents = self.ecore_parser.get_metamodel_contents(self.file_path)
            if self.serialization == "plantUML":
                for content in contents:
                    self.plant_uml_translate.generate(content)
                text = '@startuml' + '\n'
                text += self.plant_uml_translate.uml_string
                text += '\n' + '@enduml'
            else:
                raise ValueError(f"Unsupported serialization format: {self.serialization}")
        except Exception as e:
            raise RuntimeError(f"Error loading {self.file_path}") from e

        metadata = {"source": str(self.file_path)}
        yield Document(page_content=text, metadata=metadata)
=======
        """Load file."""
        # elements = self._get_elements()
        # if self.mode == "elements":
        #     for element in elements:
        #         metadata = self._get_metadata()
        #         # NOTE(MthwRobinson) - the attribute check is for backward compatibility
        #         # with unstructured<0.4.9. The metadata attributed was added in 0.4.9.
        #         if hasattr(element, "metadata"):
        #             metadata.update(element.metadata.to_dict())
        #         if hasattr(element, "category"):
        #             metadata["category"] = element.category
        #         yield Document(page_content=str(element), metadata=metadata)
        # elif self.mode == "paged":
        #     text_dict: Dict[int, str] = {}
        #     meta_dict: Dict[int, Dict] = {}

        #     for idx, element in enumerate(elements):
        #         metadata = self._get_metadata()
        #         if hasattr(element, "metadata"):
        #             metadata.update(element.metadata.to_dict())
        #         page_number = metadata.get("page_number", 1)

        #         # Check if this page_number already exists in docs_dict
        #         if page_number not in text_dict:
        #             # If not, create new entry with initial text and metadata
        #             text_dict[page_number] = str(element) + "\n\n"
        #             meta_dict[page_number] = metadata
        #         else:
        #             # If exists, append to text and update the metadata
        #             text_dict[page_number] += str(element) + "\n\n"
        #             meta_dict[page_number].update(metadata)

        #     # Convert the dict to a list of Document objects
        #     for key in text_dict.keys():
        #         yield Document(page_content=text_dict[key], metadata=meta_dict[key])
        # elif self.mode == "single":
        #     metadata = self._get_metadata()
        #     text = "\n\n".join([str(el) for el in elements])
        #     yield Document(page_content=text, metadata=metadata)
        # else:
        #     raise ValueError(f"mode of {self.mode} not supported.")
>>>>>>> Stashed changes
