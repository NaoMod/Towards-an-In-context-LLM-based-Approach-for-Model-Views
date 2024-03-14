
from pyecore.utils import dispatch
import pyecore.ecore as ecore

from pyecore.resources import ResourceSet

class PlantUMLTranslate(object):
    """_summary_"""
    def __init__(self):
        self.visited = set()
        self.uml_string = ""

    @dispatch
    def generate(self, obj):
        """Generate PlantUML syntax for the given object.

        :param obj: The object to generate PlantUML

        """
        raise ValueError('Object kind unsupported: ' + obj.eClass.name)

    @generate.register(ecore.EPackage)
    def epackage_switch(self, p):
        """Generate PlantUML syntax for the given EPackage.

        :param p: ecore EPackage

        """
        self.uml_string += 'package "'+ p.name +  '" {\n'
        for classif in p.eClassifiers:
            self.generate(classif)
        self.uml_string += '}\n\n'

    @generate.register(ecore.EClass)
    def eclass_switch(self, obj):
        """Generate PlantUML syntax for the given EClass.

        :param obj: ecore EClass

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

        :param attr: ecore EAttribute

        """
        self.uml_string += '\t' +  attr.name +  ': ' +  attr.eType.name + "\n"

    @generate.register(ecore.EReference)
    def ereference_switch(self, ref):
        """Generate PlantUML syntax for the given EReference.

        :param ref: ecore EReference

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

        :param obj: ecore EEnum

        """
        self.uml_string += 'enum ' + obj.name + ' {\n'
        for literal in obj.eLiterals:
            self.uml_string += literal.name + "\n"
        self.uml_string += '}\n'

    @generate.register(ecore.EDataType)
    def edatatype_switch(self, obj):
        """Generate PlantUML syntax for the given EDataType.

        :param obj: ecore EDataType

        """
        self.uml_string += 'class ' + obj.name + ' << (D,orchid) EDataType>>'