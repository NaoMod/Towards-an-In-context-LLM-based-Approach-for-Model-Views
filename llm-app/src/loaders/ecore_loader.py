from pathlib import Path
from typing import Any, List, Union, AsyncIterator, Iterator

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document


class EcoreLoader(BaseLoader):
    """_summary_

    Parameters
    ----------
    BaseLoader : _type_
        _description_
    """
    def __init__(self, 
        file_path: Union[str, Path],
        mode: str = "single",
        serialization: str = "plantUML",) -> None:
        """Initialize the loader with the ecore file path.

        Args:
            file_path: The path to the ecore file
        """
        self.mode = mode
        self.serialization = serialization
        self.file_path = file_path

    def _get_elements(self) -> List:
        """Get elements."""
        pass

    def _get_metadata(self) -> dict:
        """Get metadata."""
        pass

    def lazy_load(self) -> Iterator[Document]:
        """Load file."""
        elements = self._get_elements()
        self._post_process_elements(elements)
        if self.mode == "elements":
            for element in elements:
                metadata = self._get_metadata()
                # NOTE(MthwRobinson) - the attribute check is for backward compatibility
                # with unstructured<0.4.9. The metadata attributed was added in 0.4.9.
                if hasattr(element, "metadata"):
                    metadata.update(element.metadata.to_dict())
                if hasattr(element, "category"):
                    metadata["category"] = element.category
                yield Document(page_content=str(element), metadata=metadata)
        elif self.mode == "paged":
            text_dict: Dict[int, str] = {}
            meta_dict: Dict[int, Dict] = {}

            for idx, element in enumerate(elements):
                metadata = self._get_metadata()
                if hasattr(element, "metadata"):
                    metadata.update(element.metadata.to_dict())
                page_number = metadata.get("page_number", 1)

                # Check if this page_number already exists in docs_dict
                if page_number not in text_dict:
                    # If not, create new entry with initial text and metadata
                    text_dict[page_number] = str(element) + "\n\n"
                    meta_dict[page_number] = metadata
                else:
                    # If exists, append to text and update the metadata
                    text_dict[page_number] += str(element) + "\n\n"
                    meta_dict[page_number].update(metadata)

            # Convert the dict to a list of Document objects
            for key in text_dict.keys():
                yield Document(page_content=text_dict[key], metadata=meta_dict[key])
        elif self.mode == "single":
            metadata = self._get_metadata()
            text = "\n\n".join([str(el) for el in elements])
            yield Document(page_content=text, metadata=metadata)
        else:
            raise ValueError(f"mode of {self.mode} not supported.")
