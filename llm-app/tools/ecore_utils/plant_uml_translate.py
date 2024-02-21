
from pyecore.utils import dispatch
import pyecore.ecore as ecore

from pyecore.resources import ResourceSet

class PlantUMLTranslate(object):
    """_summary_

    Attributes:
        visited (set): A set to keep track of visited elements during generation.

    Adapted from: https://gist.github.com/aranega/eca9c8fbbd87b2f9c70317da53676ac6

    """
    def __init__(self):
        self.visited = set()
        self.uml_string = ""

    @dispatch
    def generate(self, obj):
        """Generate PlantUML syntax for the given object.

        Parameters:
            obj: The object to generate PlantUML.

        """
        raise ValueError('Object kind unsupported: ' + obj.eClass.name)

    @generate.register(ecore.EPackage)
    def epackage_switch(self, p):
        """Generate PlantUML syntax for the given EPackage.

        Parameters:
            p (ecore.EPackage): The EPackage to generate PlantUML.

        """
        self.uml_string += 'package "'+ p.name +  '" {\n'
        for classif in p.eClassifiers:
            self.generate(classif)
        self.uml_string += '}\n\n'

    @generate.register(ecore.EClass)
    def eclass_switch(self, obj):
        """Generate PlantUML syntax for the given EClass.

        Parameters:
            obj (ecore.EClass): The EClass to generate PlantUML.

        """
        kind = 'interface' if obj.interface else 'class '
        abstract = 'abstract ' if obj.abstract else None
        if abstract:
            self.uml_string += abstract + " "
        self.uml_string += kind + obj.name + ' {\n'
        for attrib in obj.eAttributes:
            self.generate(attrib)
        self.uml_string += '\n}\n\n'
        for sclass in obj.eSuperTypes:
            self.uml_string += sclass.name + ' <|-- ' + obj.name + '\n'
        for ref in obj.eReferences:
            self.generate(ref)

    @generate.register(ecore.EAttribute)
    def eattribute_switch(self, attr):
        """Generate PlantUML syntax for the given EAttribute.

        Parameters:
            attr (ecore.EAttribute): The EAttribute to generate PlantUML.

        """
        self.uml_string += '\t' +  attr.name +  ': ' +  attr.eType.name + "\n"

    @generate.register(ecore.EReference)
    def ereference_switch(self, ref):
        """Generate PlantUML syntax for the given EReference.

        Parameters:
            ref (ecore.EReference): The EReference to generate PlantUML.

        """
        if ref in self.visited:
            return
        self.visited.add(ref)
        label = f"{ref.name} {ref.lower}..{'*' if ref.many else ref.upper}"
        link = "--"
        if ref.containment:
            link = '*' + link
        o_label = ""
        if ref.eOpposite:
            obj = ref.eOpposite
            self.visited.add(obj)
            o_label = f"{obj.name} {obj.lower}..{'*' if obj.many else obj.upper}"
            if obj.containment:
                link += '*'
            self.uml_string += f'{ref.eContainer().name} "{label}" {link} "{o_label}" {ref.eType.name}' + "\n"
        else:
            link += '>'
            self.uml_string += f'{ref.eContainer().name} "{label}" {link} {ref.eType.name}' + "\n"

    @generate.register(ecore.EEnum)
    def enum_switch(self, obj):
        """Generate PlantUML syntax for the given EEnum.

        Parameters:
            obj (ecore.EEnum): The EEnum to generate PlantUML.

        """
        self.uml_string += 'enum ' + obj.name + ' {\n'
        for literal in obj.eLiterals:
            self.uml_string += literal.name + "\n"
        self.uml_string += '}\n'

    @generate.register(ecore.EDataType)
    def edatatype_switch(self, obj):
        """Generate PlantUML syntax for the given EDataType.

        Parameters:
            obj (ecore.EDataType): The EDataType to generate PlantUML.

        """
        self.uml_string += 'class ' + obj.name + ' << (D,orchid) EDataType>>'

# JUST FOR TESTING
# def generate(mm):
#     plantuml = '@startuml\n'
#     translate = PlantUMLTranslate()
#     translate.generate(root)
#     plantuml += translate.uml_string
#     plantuml += '@enduml'
#     print(plantuml)


# if __name__ == '__main__':
#     import sys
#     if len(sys.argv) < 2:
#         print(f"Usage: {sys.argv[0]} ecore_file")
#         sys.exit(1)
#     rset = ResourceSet()
#     metamodel_resource = rset.get_resource(sys.argv[1])
#     root = metamodel_resource.contents[0]
#     generate(root)