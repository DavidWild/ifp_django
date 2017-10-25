'''
Created on May 28, 2013

@author: david_g_wild
'''

from __future__ import division
import math
import datetime

import Expression


class RandomRange:
    def __init__(self, aStart, aEnd, aStep=1):
        self.RangeStart = aStart
        self.RangeEnd = aEnd
        self.RangeStep = aStep
        print('Start, End, Step = ' + str(aStart) + ',' + str(aEnd) + ',' + str(aStep) )

        self.NumOutcomes = int(round(abs((aEnd - aStart) / aStep)) + 1)


class RandomString:
    def __init__(self, aValue):
        self.value = aValue


class RandomVariable:
    def __init__(self, aName, aExpression, aRandomGenerator, aIsSystem=0, aValue = None):
        self.name = aName
        self.evaluated = aValue != None
        self.IsSystem = aIsSystem
        self.ExpressionStr = ''
        self.value = aValue # makes no sense when evaluated is False
        self.EvalExpr = Expression.EvalExpression(aExpression, False, aRandomGenerator)
        self.EvalExpr.UpdateVariables()
        self.ExpressionStr = aExpression
        self.DependentRandomList = []

    def Evaluate(self, originalfocus, focus, aRandomGenerator, depth):
        if (focus.name == originalfocus.name) and (depth > 0):
            raise Exception(originalfocus.name + ' is dependent on itself in expression ' + focus.ExpressionStr)
        if not focus.evaluated:
            if len(focus.DependentRandomList) == 0:
                # there are no dependencies so the value can be gotten from its own expression
                focus.value = focus.EvalExpr.Evaluate()
                focus.evaluated = True
            else:
                # for each random in the dependent list, call evaluate for it recursively
                for i in range(0, len(focus.DependentRandomList)):
                    variable = aRandomGenerator.GetVariableByName(focus.DependentRandomList[i])
                    if variable == None:
                        raise Exception('Error while trying to evaluate variable ' + focus.name + '.  It depends on ' +  str(focus.DependentRandomList[i]) + ' which has not been defined yet.')

                    focus.Evaluate(originalfocus, variable,
                                   aRandomGenerator, depth + 1)
                focus.value = focus.EvalExpr.Evaluate()
                focus.evaluated = True


    def AddDependentRandom(self, aRandomVariable):
        try:
            self.DependentRandomList.index(aRandomVariable)
        except: #it isn't already a dependent random
            self.DependentRandomList.append(aRandomVariable)

    def GetDependentRandoms(self):
        '''returns a list of dependent randoms in the form
        x -> y (if x is dependent on y)
        y -> z, a  (if y is dependent on z and a)'''
        result = self.name
        for i in range(0, len(self.DependentRandomList)):
            result = result + '-> ' + self.DependentRandomList[i] + ','
        return result


class RandomGenerator:
    def __init__(self):
        self.RandomsList = []
        self.EvaluatedAll = False #Can only become True after a call to EvaluateAll
        #self.AddVariableFromExpressionString('FUDGE', '0', True) # used for evaluating unary minuses  -1 -> fudge-1 = 0-1 = -1
        #self.EvaluateAll()
        # add the system variables
        self.RandomsList.append(RandomVariable('pi',str(math.pi),self,True,math.pi))
        self.RandomsList.append(RandomVariable('currentyear',str(datetime.datetime.now().year),self,True,datetime.datetime.now().year))
        self.RandomsList.append(RandomVariable('currentmonth',str(datetime.datetime.now().month),self,True,datetime.datetime.now().month))
        self.RandomsList.append(RandomVariable('currentday',str(datetime.datetime.now().day),self,True,datetime.datetime.now().day))
        self.RandomsList.append(RandomVariable('vat',str(20),self,True,20))




    def RemoveVariableByName(self, aName, ChangeEvaluatedState=True):
        VariableIdx = self.GetVariableIdxByName(aName)
        if VariableIdx >= 0:
            # variable already exists
            self.RandomsList.pop(VariableIdx)
            return VariableIdx
        if ChangeEvaluatedState:
            self.EvaluatedAll = False

    def AddVariableFromExpressionString(self, aName, aExpression, aIsSystem=0, ChangeEvaluatedState=True):
        """

        :param aName:
        :param aExpression:
        :param aIsSystem:
        """
        if ChangeEvaluatedState:
            self.EvaluatedAll = False
        # if the variable already exists then amend the details, else add a new one
        RemoveIdx = self.RemoveVariableByName(aName, ChangeEvaluatedState)
        if RemoveIdx >= 0:
            self.RandomsList.insert(RemoveIdx, RandomVariable(aName, aExpression, self, aIsSystem))
        else:
            self.RandomsList.append(RandomVariable(aName, aExpression, self, aIsSystem))


    def InsertVariableFromExpression(self, aIndex, aName, aExpression, aIsSystem=0):
        """

        :param aIndex:
        :param aName:
        :param aExpression:
        :param aIsSystem:
        """
        self.RandomsList.insert(aIndex, RandomVariable(aName, aExpression, self, aIsSystem))
        self.EvaluatedAll = False

    def GetVariableByName(self, aName):
        Result = self.GetVariableIdxByName(aName)
        if Result < 0:
            return None
        else:
            return self.RandomsList[Result]


    def GetVariableIdxByName(self, aName):
        idx = 0
        Result = -1
        while idx < len(self.RandomsList):
            if self.RandomsList[idx].name == aName:
                Result = idx
                break
            idx = idx + 1
        return Result

    def PrintRandoms(self):
        Result = ''
        for i in range(0, len(self.RandomsList)):
            Result = Result + self.RandomsList[i].name + ' = ' + self.RandomsList[i].ExpressionStr + '\n'
        return Result

    def PrintDependencies(self):
        for i in range(0, len(self.RandomsList)):
            print(self.RandomsList[i].GetDependentRandoms())

    def PrintValues(self):
        print ('Values of randoms in Generator:\n')
        for i in range(0, len(self.RandomsList)):
            print( self.RandomsList[i].name + '=' + str(self.RandomsList[i].value) + '\n')

    def AddDependencies(self):
        ''' For each variable, go through the expression and add the variables to the DependentRandomList'''
        for i in range(0, len(self.RandomsList)):

            self.RandomsList[i].EvalExpr.UpdateVariables()
            # Search for variables that appear in the EvalExpr and add them to the DependentRandomList of the variable
            for j in range(0, len(self.RandomsList[i].EvalExpr.variables)):
                self.RandomsList[i].AddDependentRandom(self.RandomsList[i].EvalExpr.variables[j])
                if self.RandomsList[i].EvalExpr.variables[j] == self.RandomsList[i].name:
                    raise Exception(self.RandomsList[i].name +
                                    ' evaluation leads to indeterminate value.  '
                                    'Perhaps it is a self-referencing variable?')


    def HasCircularReference(self):
        # Look through all the variables and return true of there is a circular reference (meaning that a variable cannot be evaluate)
        # An example of a circular reference is if x = y + z; y = x (x depends on y and vice versa)
        if len(self.RandomsList) == 0:
            return False
        else:
            # go through all the randoms in the RandomsList and see if any child of the particular random has itself as a dependency
            for randomCounter in range(0, len(self.RandomsList)):
                ThisRandom = self.RandomsList[randomCounter]
                return ThisRandom.DependentRandomList.index(ThisRandom)

    def Reset(self):
        self.EvaluatedAll = False
        del self.RandomsList[:]

    def ResetValues(self, ResetOnlyList=[]):
        for i in range(0,len(self.RandomsList)):
            if len(ResetOnlyList) > 0:
                if self.RandomsList[i].name in ResetOnlyList:
                    self.RandomsList[i].value = None
            else:
                self.RandomsList[i].value = None


    def EvaluateAll(self,EvaluateOnlyList=[]):
        '''Evaluates all of the variables in the RandomsList - returns True if successful, 
        False otherwise e.g. if there is a circular reference or an EvalExpr is ill-formed.
        It works by creating a directed graph. Two nodes on the graph, n1 and n2, are related n1->n2 if the EvalExpr
        defining n1 contains n2.  
        
        Example.  Given a=b+c, b=d+1, c=4-pi, d=6 then we get the following relationships
        a->b, a->c, b->d
        
        Example.  Given a=b+c, b=a+c  then a<->b, a->c, b->c  (this would result in a circular reference which means we can't evaluate)
        
        self.EvaluatedAll = True'''
        if self.EvaluatedAll and len(self.RandomsList) > 0:
            raise Exception('Call to EvaluateAll without reset')

        for i in range(0, len(self.RandomsList)):
            self.RandomsList[i].Evaluate(self.RandomsList[i], self.RandomsList[i], self, 0)
        self.EvaluatedAll = True

    def GetValueByIdx(self, aIdx):
        return self.RandomsList[aIdx].value

    def GetValueByName(self, aName):
        variable = self.GetVariableByName(aName)
        if variable == None:
            return None
        else:
            return variable.value

    def SetValueByName(self, aName, aValue):
        variable = self.GetVariableByName(aName)
        if variable == None:
            raise Exception('The variable ' + aName + ' does not exist to set its value')
        else:
            variable.value = aValue


if __name__ == '__main__':
    aRandomGenerator = RandomGenerator()

    aRandomGenerator.AddVariableFromExpressionString('person','randomstr("David","Scarlett","Adam","Sandra")')
    aRandomGenerator.AddVariableFromExpressionString('She','match(person="David","He",person="Adam","He","She")')


    #     aRandomGenerator.AddVariableFromExpressionString('s2','s4^s3')
    #     aRandomGenerator.AddVariableFromExpressionString('s3','random(range(-1,s4,2))')
    #     aRandomGenerator.AddVariableFromExpressionString('s4','eval(s5+5)')
    #     aRandomGenerator.AddVariableFromExpressionString('s1', 'randomstr("string1","string2","string3","string4","string5")')
    #     aRandomGenerator.AddVariableFromExpressionString('a1', 'random(range(2,a5,1))')
    #     aRandomGenerator.AddVariableFromExpressionString('a2', 'a1+2')
    #     aRandomGenerator.AddVariableFromExpressionString('a3', 'a2+a4')
    #     aRandomGenerator.AddVariableFromExpressionString('a4', '4*a2')
    #     aRandomGenerator.AddVariableFromExpressionString('a5', 'random(range(3,9,1))')
    #     aRandomGenerator.AddVariableFromExpressionString('SandraAge', 'random(range(24,34,1))')
    #     aRandomGenerator.AddVariableFromExpressionString('DavidAge', 'random(range(35,45,1))')
    #     aRandomGenerator.AddVariableFromExpressionString('SumAges', 'SandraAge+DavidAge-SandraAge/DavidAge+DavidAge^4/(SandraAge+DavidAge)')


    aRandomGenerator.AddDependencies()
    aRandomGenerator.PrintDependencies()
    aRandomGenerator.EvaluateAll()
    aRandomGenerator.PrintValues()

    print('Random Generator\n' + aRandomGenerator.PrintRandoms())

#     print myexpression.Evaluate(RandomGenerator()) 
        