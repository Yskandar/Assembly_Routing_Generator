# -*- coding: utf-8 -*-
"""
Created on Fri May 10 07:38:31 2019

@author: Yskandar GAS
"""


class product() : #main class creation
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
            
    def add_relation(self, newrel) : #adding relation method creation
        if isinstance(newrel, relation): #checking the type of the given relation
            if newrel.get_components()[0] in self._mycomponents and newrel.get_components()[1] in self._mycomponents: #checking if the components in the given relation do belong to the main product
                self._myrelations.append(newrel)
            else:
                return "This relation involves one or two components which are not in this product"
        else:
            return "unrecognized relation"
                       
    def __repr__(self):
        return "{} contains {} and the following relations {}".format(self._name, self._mycomponents, self._myrelations)
                
class component(): #creation of the class describing the components of the product
    def __init__(self, yourname, yourfunctions=[]):
        self._name = str(yourname)
        self._functions = list(yourfunctions)
        
    def add_function_elem(self, newfunction): #each function realized by a component is either an elementary function or a function decomposable into elementary functions
        if isinstance(newfunction, functions_elem): #for simplification, only elementary functions will be associated with components
            self._functions.append(newfunction)
        else: 
            print("Unrecognized Function")
            
    def __repr__(self):
        return self._name
        
        
class functions_elem(): #each function realized by a component is either an elementary function or a function decomposable into elementary functions
    def __init__(self, yourname) : 
        self._name = str(yourname)
    def __repr__(self):
        return self._name
    
    def _get_name(self) : 
        return self._name

        
class functions_decomp() : #each function realized by a component is either an elementary function or a function decomposable into elementary functions
    def __init__(self,yourname, yourfunctions = []) : 
        self._name = str(yourname)
        self._functions = list()
        if isinstance(yourfunctions, list) : 
            for fonc in yourfunctions : 
                self.add_function(fonc)
    
    def add_function(self, newfunction) : # adding function method creation
        if isinstance(newfunction,functions_elem) or isinstance(newfunction,functions_decomp)  : 
            self._functions.append(newfunction)
    
    def _get_name(self) : 
        return self._name
    def _get_function_elem(self) : #displays the elementary functions which constitute this decomposable function
        return self._functions
        
        
    
class relation(): #creation of the class describing the relations binding each component to others
    def __init__(self, yourname, twocomponents, solutiontech): #solutiontech refers to the technical solution used (riveting, shrinking, sticking...)
        self._name = str(yourname)
        self._components = list()
        if isinstance(twocomponents,list) and len(twocomponents) == 2:
            for yourcomponent in twocomponents:
                if isinstance(yourcomponent, component):
                    self._components.append(yourcomponent)
                else:
                    return "given component unrecognized"
        else:
            return "incorrect list format or excessive list size"
        self._solution = str(solutiontech)
    def get_components(self):
        return self._components
        
    def __repr__(self):
        return "{} and {} are bound by {}".format(self._components[0], self._components[1], self._solution)
    

testfunction = functions_elem("ceci est la function test")
testcomponent = component("componenttest", [testfunction])
testcomponentb = component("componenttest2", [testfunction])
testrelation = relation("testrelation", [testcomponent, testcomponentb], "testsolution")
testproduct = product("testproduct")
testproduct.add_component(testcomponent)
testproduct.add_component(testcomponentb)


        

        
            
            
            
            
            