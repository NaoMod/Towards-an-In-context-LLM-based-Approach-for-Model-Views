# PyEcore
from typing import Tuple
from pyecore.resources import ResourceSet, URI
import os

class Singleton(type):
    def __init__(self, name, bases, mmbs):
        super(Singleton, self).__init__(name, bases, mmbs)
        self._instance = super(Singleton, self).__call__()

    def __call__(self, *args, **kw):
        return self._instance


class EcoreParser(metaclass=Singleton):
    """
    The EcoreParser class is used to parse Ecore metamodels and check if a given class exists in the specified Ecore metamodel.

    Attributes
    ----------
    resource_set : ResourceSet
        The resource set used for managing Ecore resources.
    classes_per_metamodel : dict
        A dictionary that stores the list of classes per metamodel.
    metamodels_uri : list
        A list that stores the URIs of the metamodels.

    Methods
    -------
    __init__()
        Initialize the EcoreParser class.
    check_ecore_class(ecore_path, class_to_test)
        Check if a given class exists in the specified Ecore metamodel.
    check_ecore_attribute(ecore_path, class_to_test, attr_to_test)
        Check if a given attribute exists in the specified class of the Ecore metamodel.
    get_metamodel_uri(ecore_path)
        Get the URI of the metamodel.

    """

    def __init__(self):
        """
        Initialize the EcoreParser class.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.resource_set = ResourceSet()
        self.classes_per_metamodel = {}
        self.metamodels_uri = []

    def register_metamodel(self, ecore_path: str) -> None:
        """
        Register the specified Ecore metamodel.

        Parameters
        ----------
        ecore_path : str
            The path to the Ecore metamodel file.

        Returns
        -------
        None
        """

        # ensure that all inner metamodels are registered before the main one
        metamodels_folder = os.path.dirname(ecore_path)
        extra_folder = os.path.join(metamodels_folder, "extra")
        if os.path.isdir(extra_folder):
            for extra_ecore_file in os.listdir(extra_folder):
                if extra_ecore_file.endswith(".ecore"):
                    self.register_metamodel(os.path.join(extra_folder, extra_ecore_file))

        resource_path = self.resource_set.get_resource(URI(ecore_path))
        if resource_path is None or not resource_path.contents:
            return

        content = resource_path.contents[0]
        if content is None or content.nsURI is None:
            return

        if content.nsURI not in self.resource_set.metamodel_registry:
            self.resource_set.metamodel_registry[content.nsURI] = content

    def get_metamodel_contents(self, ecore_path: str):
        """
        Get the contents of the specified Ecore metamodel.

        Parameters
        ----------
        ecore_path : str
            The path to the Ecore metamodel file.

        Returns
        -------
        object
            The contents of the metamodel.
        """
        resource_path = self.resource_set.get_resource(URI(ecore_path))
        if resource_path is None or not resource_path.contents:
            #try to register
            try:
                self.register_metamodel(ecore_path)
            except:
                return

        return resource_path.contents

    def check_ecore_class(self, ecore_path: str, class_to_test: str) -> bool:
        """
        Check if a given class exists in the specified Ecore metamodel.

        Parameters
        ----------
        ecore_path : str
            The path to the Ecore metamodel file.
        class_to_test : str
            The name of the class to check.

        Returns
        -------
        bool
            True if the class exists in the metamodel, False otherwise.
        """

        if ecore_path not in self.classes_per_metamodel:
            self.classes_per_metamodel[ecore_path] = []
        if class_to_test in self.classes_per_metamodel[ecore_path]:
            return True

        metamodel_contents = self.get_metamodel_contents(ecore_path)

        # check class
        for content in metamodel_contents:
            if content.eClass.name == 'EPackage':
                for element in content.eAllContents():
                    if element.eClass.name == 'EClass':
                        class_name = element.name
                        if class_name == class_to_test:
                            self.classes_per_metamodel[ecore_path].append(class_name)
                            return True

        return False
    
    def check_ecore_attribute(self, ecore_path: str, class_to_test: str, attr_to_test: str) -> bool:
        """
        Check if a given attribute exists in the specified class of the Ecore metamodel.

        Parameters
        ----------
        ecore_path : str
            The path to the Ecore metamodel file.
        class_to_test : str
            The name of the class containing the attribute to check.
        attr_to_test : str
            The name of the attribute to check.

        Returns
        -------
        bool
            True if the attribute exists in the specified class of the metamodel, False otherwise.
        """

        # Check if the class containing the attribute exists in the metamodel
        if class_to_test not in self.classes_per_metamodel[ecore_path]:
            # Class doesn't exist, return False
            return False

        
        resource_path = self.resource_set.get_resource(URI(ecore_path))
        if resource_path is None or not resource_path.contents:
            return False

        content = resource_path.contents[0]
        if content is None or content.nsURI is None:
            return False

        # register metamodel
        if content.nsURI not in self.resource_set.metamodel_registry:
            self.resource_set.metamodel_registry[content.nsURI] = content

        # Iterate through elements to find the class and check its attributes
        for content in resource_path.contents:
            if content.eClass.name == 'EPackage':
                for element in content.eAllContents():
                    if element.name == class_to_test:
                        # Found the class, now check its attributes
                        for attribute in element.eAttributes:
                            if attribute.name == attr_to_test:
                                # Attribute found, return True
                                return True

        # Attribute not found in the specified class
        return False
    
    def get_metamodel_uri(self, ecore_path: str) -> Tuple[str, str]:
        """
        Get the URI of the metamodel.

        Parameters
        ----------
        ecore_path : str
            The path to the Ecore metamodel file.

        Returns
        -------
        Tuple[str, str]
            The URI of the metamodel and its prefix.
        """
        resource_path = self.resource_set.get_resource(URI(ecore_path))
        if resource_path is None or not resource_path.contents:
            #try to register
            try:
                self.register_metamodel(ecore_path)
            except:
                return None

        content = resource_path.contents[0]
        if content is None or content.nsURI is None:
            return None

        return content.nsURI, content.nsPrefix or f'prefix_{content.nsURI}'
    
    def get_all_class_properties(self, meta_model_uri: str, class_name: str) -> list:
        """
        Get all properties of the specified class in the metamodel.

        Parameters
        ----------
        metamodel_name : str
            The name of the metamodel.
        class_name : str
            The name of the class.

        Returns
        -------
        list
            A list of properties of the specified class.
        """
        properties = []
        for _ , resource in self.resource_set.resources.items():
            content = resource.contents[0]

            if content.nsURI.strip() == meta_model_uri.strip():

                # Iterate through elements to find the class and add its properties
                for content in resource.contents:
                    if content.eClass.name == 'EPackage':
                        for element in content.eAllContents():
                            if element.name == class_name:
                                # Found the class, now check its properties
                                for property_ in element.eAllStructuralFeatures():
                                    properties.append(property_.name)
        return properties

