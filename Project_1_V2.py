#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Yskandar Gas
"""
"""
'Nom' is french for name
'Fonction Elementaire' is french for Elementary Function


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
      
                   
    def __repr__(self):
        return "{} contains {} and the following relations {}".format(self._name, self._mycomponents, self._myrelations)

        
    
        
class component(): #creation of the class describing the components of the product
    def __init__(self, yourname, yourID, yourfunctions=[]):
        self._name = str(yourname)
        self._id = str(yourID)
        self._functions = list(yourfunctions)
        
        
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


        
class functions_elem(): #each function realized by a component is either an elementary function or a function decomposable into elementary functions
    def __init__(self, yourname, yourdescription) : 
        self._name = str(yourname)
        self._description = str(yourdescription)
    
    def __repr__(self):
        return self._name
    
    def _get_name(self) : 
        return self._name
        
        
    
        
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
    
        
        

#testfonction = fonctions_elem("ceci est la fonction test")
#testpiece = piece("piecetest", [testfonction])
#testpieceb = piece("piecetest2", [testfonction])
#testrelation = relation("testrelation", testpiece, "testsolution")
#testproduit = produit("testproduit")
#testproduit.add_piece(testpiece)
#testproduit.add_piece(testpieceb)

xml_tree = ET.parse('ColonneV1.2.xml')
trunk = xml_tree.getroot()



def sort(function): #creates object functions (decomposable or elementary) based on the children of the given function

    if function.tag == 'Fonction_Elementaire':
        return functions_elem(function.attrib['Nom'], function.attrib['Description'])
    else:
        N = functions_decomp(function.attrib['Nom'], function.attrib['Description'])
        for child in function:
            N.add_function(sort(child)) 
        return N
    
#test
toto = sort(trunk[0][5])
# 
    
