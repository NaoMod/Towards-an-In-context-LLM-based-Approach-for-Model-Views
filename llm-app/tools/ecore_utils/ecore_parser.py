#PyEcore
from pyecore.resources import ResourceSet, URI

class EcoreParser:

    def __init__(self):
        self.self.resource_set = ResourceSet()
        self.self.classes_per_metamodel = {}
    
    def check_ecore_class(self, ecore_path: str, class_to_test: str):
        if class_to_test in self.classes_per_metamodel[ecore_path]:
            return True
        #register metamodel
        resource_path = self.resource_set.get_resource(URI(ecore_path))
        content = resource_path.contents[0]
        if self.resource_set.metamodel_registry[content.nsURI] is None:
            self.resource_set.metamodel_registry[content.nsURI] = content
        for element in resource_path.contents.contents:    
            class_name = element.eClass.name
            if class_name == class_to_test:
                if self.classes_per_metamodel[ecore_path] is None:
                    self.classes_per_metamodel[ecore_path].append(class_name)
                return True        
        return False