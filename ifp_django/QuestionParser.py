'''
Created on Jul 19, 2013

@author: david_g_wild
'''

import re

from Randoms import RandomGenerator
from Expression import EvalExpression
from iqPictures import IQPicture_SimpleCartesian, IQPictureList, IQPicture_Scatter


class EventHook(object):
    def __init__(self):
        self.__handlers = []
 
    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self
 
    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self
    
    def fire(self, *args, **keywargs):
        for handler in self.__handlers:handler(*args, **keywargs)
         
    def clearObjectHandlers(self, inObject):
        for theHandler in self.__handlers:
            if theHandler.im_self == inObject:
                self -=theHandler


class IQText:
    def __init__(self):
        self.RandomGenerator = RandomGenerator()
        self.pictureObjects = IQPictureList()
        None

    def parseLatexObjects(self, objectsForSplitting, outputObjects, textstart, textend, outputstart, outputend, isExpression=True, fireevent=False):
        # now that we have the questiontexts and the randoms in the generator, I can get the latex for each of the questiontexts
        for i in range(0, len(objectsForSplitting)):
            # for each of the text objects, look for mathematics in $ signs
            # we hold the non-maths in SplittedObjects and the mathematics in mathsExpressions.
            # then at the end, we replace the maths objects with the LaTeX equivalent and sow it all back together
            SplittedObjects = re.split('(' + re.escape(textstart) + '.*?' + re.escape(textend) + ')', objectsForSplitting[i])

            # TODO: cater for \[ maths \] and $$ maths $$ as well as $ maths $ situations
            for j in range(0, len(SplittedObjects)):
                #SplittedObjects[j] = SplittedObjects[j].decode('utf-8')
                if unicode(SplittedObjects[j]).startswith(textstart) and str(SplittedObjects[j]).endswith(textend):
                    if isExpression:
                        expr = EvalExpression(SplittedObjects[j][len(textstart):len(SplittedObjects[j]) - len(textend)], False, self.RandomGenerator)
                        if expr.syntaxError != '':
                            raise Exception('Maths expression "'+expr.ExpressionString+'" has an error: ' + expr.syntaxError)
                        LaTeX = expr.GetLateXMathExpression(self.pictureObjects)
                        if not SplittedObjects[j].startswith('$picture'):
                            LaTeX = str(outputstart) + LaTeX + str(outputend)
                        if expr.syntaxError != '':
                            LaTeX = LaTeX + '\\textcolor{red}{Expression} ' + LaTeX + ' \\textcolor{red}{has a syntax error: ' + expr.syntaxError + '}'


                        SplittedObjects[j] =  str(LaTeX)



            outputObjects.append(''.join(unicode(e) for e in SplittedObjects))

class IQQuestion(IQText):
    

    def HandleRequirePicture(self, pictureLatex):
        print('HandleRequirePicture called with parameter ' + str(pictureLatex))
        return pictureLatex
        
    def __init__(self, questionNode, graphicsfolder ):
        IQText.__init__(self)
        self.onRequirePicture = EventHook()
        self.onRequirePicture += self.HandleRequirePicture
        questionTextObjects = []
        solutionObjects = []

        self.questionTexts = []
        self.questionSolutions = []
        self.questionPictures = []
        self.graphicsfolder = graphicsfolder


        questionsCanSpanPages = questionNode.get('questionscanspanpages') == 'yes'
        for questionTextNode in questionNode.findall('questiontext'):
            if not questionsCanSpanPages:
                questionTextObjects.append('\\vspace*{0.3cm}\\begin{minipage}[t]{1.0\\textwidth} ' + questionTextNode.text + '\\end{minipage}')
            else:
                questionTextObjects.append( questionTextNode.text )

        solutionsCanSpanPages = questionNode.get('solutionscanspanpages') == 'yes'
        for solutionNode in questionNode.findall('solution'):
            if not solutionsCanSpanPages:
                solutionObjects.append('\\vspace*{0.3cm}\\begin{minipage}[t]{1.0\\textwidth} ' + solutionNode.text + '\\end{minipage}')
            else:
                solutionObjects.append( solutionNode.text  )


        for randomNode in questionNode.findall('randoms/random'):
            self.RandomGenerator.AddVariableFromExpressionString(randomNode.get('name'), randomNode.get('expression'), randomNode.get('issystem'))
    
        self.RandomGenerator.AddDependencies()
        self.RandomGenerator.EvaluateAll()
#         self.RandomGenerator.PrintDependencies()
#         self.RandomGenerator.PrintValues()

        for pictureNode in questionNode.findall('pictures/picture'):
            if pictureNode.get('type') == 'simplecartesian':
                self.pictureObjects.pictures.append(IQPicture_SimpleCartesian(self.RandomGenerator,
                                                    pictureNode.get('labelpointsx'),
                                                    pictureNode.get('labelpointsy'),
                                                    pictureNode.get('id'), self.graphicsfolder,
                                                    pictureNode.get('expression'),
                                                    pictureNode.get('xfrom'),
                                                    pictureNode.get('xto'),
                                                    pictureNode.get('xstep'),
                                                    pictureNode.get('yfrom'),
                                                    pictureNode.get('yto'),
                                                    pictureNode.get('xlabel'),
                                                    pictureNode.get('ylabel'),
                                                    pictureNode.get('title'),
                                                    pictureNode.get('scale'),
                                                    ))
            elif pictureNode.get('type') == 'scatter':
                self.pictureObjects.pictures.append(IQPicture_Scatter(self.RandomGenerator,
                                                                      pictureNode.get('fitexpression'),
                                                                      pictureNode.get('labelpointsx'),
                                                                      pictureNode.get('labelpointsy'),
                                                                      pictureNode.get('id'),
                                                                      self.graphicsfolder,
                                                                      pictureNode.get('xcoordinates'),
                                                                      pictureNode.get('ycoordinates'),
                                                                      pictureNode.get('xlabel'),
                                                                      pictureNode.get('ylabel'),
                                                                      pictureNode.get('title'),
                                                                      pictureNode.get('scale'),
                                                                      ))
            else:
                raise Exception('Picture has an unknown type ' + pictureNode.get('type'))
            

        
       
        self.parseLatexObjects(questionTextObjects, self.questionTexts, '$', '$', '$', '$', True, False)
        self.parseLatexObjects(solutionObjects, self.questionSolutions, '$', '$', '$', '$', True, False)
        # self.parseLatexObjects(questionTextObjects, self.questionPictures, '\\includegraphics{', '}', '\\includegraphics[scale=0.25]{', '}',False, True)
        # self.parseLatexObjects(solutionObjects, self.questionPictures, '\\includegraphics{', '}', '\\includegraphics[scale=0.25]{', '}',False,True)
        
            
            

                      
if __name__ == '__main__':
    for j in range(0, 10):
        myQuestion = IQQuestion('National5Sample1.xml')
        print(myQuestion.questionTexts[0])
    
    
