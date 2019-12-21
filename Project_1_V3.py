
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Yskandar Gas
"""
"""
'Nom' is french for name
'Fonction Elementaire' is french for Elementary Function
'DDL' is french for Degree of Freedom
'DFC link' means technical relation between two components


"""

import xml.etree.ElementTree as ET

class Product() : #main class creation
    def __init__(self, yourname, yourcomponents=[], your_relations=[]):
        self._name = str(yourname)
        self._mycomponents = list()
        if isinstance(yourcomponents, list) : #checking the given components
            for component in yourcomponents : 
                self.add_component(component)
        self._myrelations = list()
        if isinstance(your_relations,list) : #checking the given relations
            for rel in your_relations : 
                self.add_relation(rel)
        
    def add_component(self, newcomponent) : #adding component method creation
        if isinstance(newcomponent,component) : #checking the type of the given component
            self._mycomponents.append(newcomponent)
            
    def add_components(self,componentstoadd) : 
        """adding a list of components method creation"""
        components = list(componentstoadd)
        for elt in components : 
            self.add_component(elt)
            
    def add_relation(self, newrelation):
        if isinstance(newrelation, relation):
            self._myrelations.append(newrelation)
            
    def add_relations(self, relationstoadd):
        rel = list(relationstoadd)
        for elt in rel:
            self.add_relation(elt)
        
    def _get_components(self):
        return self._mycomponents
    
    def _get_relations(self):
        return self._myrelations
    
    def _get_name(self):
        return self._name
    
    relations = property(_get_relations) #property methods creation
    components = property(_get_components)
    name = property(_get_name)
      
                   
    def __repr__(self):
        return "{} contains {} and the following relations {}".format(self._name, self._mycomponents, self._myrelations)

        
    
        
class component(): #creation of the class describing the components of the product
    def __init__(self, yourname, yourID, yourfunctions=[], your_relations=[]):
        self._name = str(yourname)
        self._id = str(yourID)
        self._functions = list(yourfunctions)
        self._relations = list(your_relations)
        
    def add_function_elem(self, newfunction): #each function realized by a component is either an elementary function or a function decomposable into elementary functions
        if isinstance(newfunction, functions_elem): #for simplification, only elementary functions will be associated with components
            self._functions.append(newfunction)
        else: 
            print("Unrecognized function")
        
    def add_functions_elem(self, functionstoadd) : 
        """ adding a list of functions to a component method creation"""
        func = list(functionstoadd)
        for elt in func : 
            self.add_function_elem(elt)
            
    def add_relation(self, newrel) :
        """ adding a relation involving the component method creation"""
        if isinstance(newrel, relation): #checking the type of the given relation
            if newrel._get_destination() != self : 
                self._relations.append(newrel)
            else : 
                return "this relation bounds the component with itself"
        else:
            return "unrecognized relation"
            
    def __repr__(self):
        return "{}".format(self._name)
    
    def _get_functions(self):
        return self._functions
    
    def _get_id(self):
        return self._id
    
    def _get_name(self):
        return self._name
    
    def _get_relations(self):
        return self._relations
    
    functions = property(_get_functions)
    name = property(_get_name)


        
class functions_elem(): #each function realized by a component is either an elementary function or a function decomposable into elementary functions
    def __init__(self, yourname, yourdescription) : 
        self._name = str(yourname)
        self._description = str(yourdescription)
    
    def __repr__(self):
        return self._name
    
    def _get_name(self) : 
        return self._name
    
    def _get_description(self):
        return self._description
    
    description = property(_get_description)
    name = property(_get_name)  
        
        
    
        
class functions_decomp() : #each function realized by a component is either an elementary function or a function decomposable into elementary functions
    def __init__(self,yourname, yourdescription, yourfunctions = []) : 
        self._name = str(yourname)
        self._description = str(yourdescription)
        self._functions = list()
        if isinstance(yourfunctions, list) : #checking the type of the given function
            for func in yourfunctions : 
                self.add_function(func)
    
    def add_function(self, newfunction) : # adding function method creation
        if isinstance(newfunction,functions_elem) or isinstance(newfunction,functions_decomp)  : 
            self._functions.append(newfunction)
        
    def _get_name(self) : 
        return self._name
    def _get_function_child(self) : #displays the elementary functions which constitute this decomposable function
        return self._functions
    
    def __repr__(self):
        return self._name
    
    def _get_description(self):
        return self._description
    
    
    description = property(_get_description)
    name = property(_get_name)
    children = property(_get_function_child)   
        
        
        
        
class relation(): #creation of the class describing the relations binding each component to others
    def __init__(self, maincomponent, destination, yourDOF, solutiontech):
        if isinstance(destination,component) :
            self._component = destination
        else:
            return "unrecognized component"
        if isinstance(yourDOF,int) : 
            self._DOF = str(yourDOF)
        else : 
            return "DOF (degree of freedom) must be of type integer"
        if isinstance(maincomponent, component):
            self._mcomponent = maincomponent
        self._solution = str(solutiontech)
        
    def _get_destination(self):
        return self._component
            
    def __repr__(self):
        return "{} and {} are bound by {}".format(self._mcomponent, self._component, self._solution)
    
        
        

Functionselem = dict() #creating 3 dictionnaries allowing for retrieving elements using only their ID
Functionsdecomp = dict()
components = dict()

xml_tree = ET.parse('ColonneV1.2.xml')
trunk = xml_tree.getroot()



def sort(function): #creates object functions (decomposable or elementary) based on the children of the given function

    if function.tag == 'Fonction_Elementaire':
        Functionselem[function.attrib['Nom']] = functions_elem(function.attrib['Nom'], function.attrib['Description']) #filling the Functionselem dictionnary using the key "Nom"
        return functions_elem(function.attrib['Nom'], function.attrib['Description'])
    else:
        N = functions_decomp(function.attrib['Nom'], function.attrib['Description'])
        Functionsdecomp[function.attrib['Nom']] = N #filling the Functionsdecomp dictionnary using the key "Nom"
        for child in function:
            N.add_function(sort(child)) 
        return N
    


def xml_loader(xml_file) : 
    """loads all the informations contained in a XML file into new elements whose types are the different classes above"""
    
    componentslist=[]
    listefunction=[]
    relation_list=[]
    xmltree = ET.parse(xml_file)
    trunk = xmltree.getroot()
    
    for function in trunk[0]:
        listefunction.append(sort(function)) #retreives all the functions given in the XML file and puts them in listefunction

    for pc in trunk[1]:
        newcomponent = component(pc.attrib['Nom'], pc.attrib['ID']) #creating components object from the components given in the XML file
        components[pc.attrib['ID']] = newcomponent #adding these new components in the components dictionnary, with the key "ID"
        componentslist.append(newcomponent)
        


#To create relations between components, I must first import all the components from the XML file into new components-type objects
#Then, I create all the relations by retrieving all the components using their ID and the components dictionnary

    
    for pc in trunk[1]:
        maincomponent = components[pc.attrib['ID']] #retrieving the main component using its ID
        
        for function in pc.iter('Fonction_realisee'):
            maincomponent.add_function_elem(Functionselem[function.attrib['Nom']]) #adding the functions linked to this component using their name
        
        
        for lien in pc.iter('Lien_DFC'): #retrieving the components connected to this relation (Lien means link) using their ID
            newrelation = relation(maincomponent, components[lien.attrib['Destination']], int(lien.attrib['Ddl']), lien.attrib['Techno']) #creating the corresponding relation-type objects
            relation_list.append(newrelation) #adding the relation to relation_list
            maincomponent.add_relation(newrelation) #adding the relation to the main component
            
    product = Product(trunk.attrib['Nom']) #creating the product-type object from the product given in the XML file 
    product.add_components(componentslist)
    product.add_relations(relation_list)


Test = xml_loader("ColonneV1.3.xml")
listefunction = Test[1]
producttest = Test[0]
listecomponents = Test[2]

    
def xmlbuilder(Built_product): #converts a product-type object into an XML file (featuring its components, relations...)
    if not isinstance(Built_product, Product):
        return "unrecognized product"
    
    trunk = ET.Element("Product",{"Nom": Built_product.name}) #creating the XML main trunk using the name of the given product
    trunk.append(ET.Element("Fonctions")) #adding the Functions and Components sections
    trunk.append(ET.Element("components"))
    
    for function in listefunction: #for each function, adding its subtree containing all of its children (using the sortb function) to the main trunk
        trunk[0].append(sortb(function))
        
    for component in Built_product.components: 
        elemcomponent = (ET.Element("Piece",{"Nom":component.name, "ID":component._get_id()})) #adding each component
        for function in component.functions:
            elemcomponent.append(ET.Element("Fonction_realisee",{"Nom":function.name})) #adding each of the component's functions
        for lien in component.relations:
            componentdestination = lien.dest
            elemcomponent.append(ET.Element("Lien_DFC", {"Techno": lien.solution, "Ddl": lien.DOF, "Destination": componentdestination.yourID})) #adding DFC links to the component (DFC link = relation)
            
        trunk[1].append(elemcomponent) #adding the component to the components tree     
    

def sortb(function): #recursive algorithm creating the XML subtree of the given function featuring all of its children
    
    if isinstance(function, functions_elem): #STOP condition: an elementary function doesn't have any children
        newfunction_elem = ET.Element("Fonction_Elementaire",{"Nom":function.name, "Description":function.description})

        return newfunction_elem
        
    if isinstance(function, functions_decomp): #adding the function to the tree and applying sortb to all of its children
        newfunction_decomp = ET.Element("Fonction",{"Nom":function.name, "Description":function.description})
        
        for child in function.children:
            newfunction_decomp.append(sortb(child))
        return newfunction_decomp #returns the final XML tree