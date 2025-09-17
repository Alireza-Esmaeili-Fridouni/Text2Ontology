from owlready2 import get_ontology

class OntologyParser:
    def __init__(self, ontology_file:str):
        self.ontology_file = ontology_file
        self.onto = None
        
    def load_ontology(self):
        self.onto = get_ontology(self.ontology_file).load()
        return self.onto
    
    def instance_extractor(self):
        if self.onto is None:
            self.load_ontology()
        instance_info = []
        instance_text = []
        for cls in self.onto.classes():
            for inst in cls.instances():
                instance_info.append({"instance":inst.name,
                                      "class":cls.name,
                                      "uri":inst.iri})
                instance_text.append(f"{inst.name} a type of {cls.name}")
        return instance_info, instance_text
    
# from owlready2 import get_ontology

# class OntologyParser:
#     def __init__(self, ontology_file: str):
#         self.ontology_file = ontology_file
#         try:
#             self.onto = get_ontology(self.ontology_file).load()
#             if self.onto is None:
#                 raise RuntimeError(f"Failed to load ontology from {self.ontology_file}")
#         except Exception as e:
#             raise RuntimeError(f"Error loading ontology: {e}")

#     def instance_extractor(self):
#         instance_info = []
#         instance_text = []
#         for cls in self.onto.classes():
#             for inst in cls.instances():
#                 instance_info.append({
#                     "instance": inst.name,
#                     "class": cls.name,
#                     "uri": inst.iri
#                 })
#                 instance_text.append(f"{inst.name} a type of {cls.name}")
#         return instance_info, instance_text

          