'''
Created on Aug 9, 2013

@author: david_g_wild
'''
import matplotlib
matplotlib.use('Agg')
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
# Force matplotlib to not use any Xwindows backend.


import definitions
import Expression

#from mpl_toolkits.axes_grid.axislines import SubplotZero


class IQPictureList:
    def __init__(self):
        self.pictures = []

    def getPicturefromId(self, aId):
        result = None #not found
        for i in range(0, len(self.pictures)):
            if self.pictures[i].picId == aId:
                result = self.pictures[i]
                break
        return result


class IQPicture:
    def __init__(self, aRandomGenerator, labelpointsx, labelpointsy, graphicsfolder, picId, filepath='', filename=''):
        self.picId = picId
        self.GeneratedFile = False
        filepath = graphicsfolder
        if filename == '':
            filename = definitions.unique_filename()
        self.FileLocation = filepath + '/' + filename
        self.filename = filename
        self.RandomGenerator = aRandomGenerator
        self.scale = 100
        self.mthExpressions = []

        plt.clf()

        #label some specific points
        self.labelpointsx = labelpointsx
        self.labelpointsy = labelpointsy

        if self.labelpointsx != '' and self.labelpointsy != '' and labelpointsx != None and labelpointsy != None:
            self.labelpointsx = str(self.labelpointsx).split(',')
            self.labelpointsy = str(self.labelpointsy).split(',')
            if not len(self.labelpointsx) == len(self.labelpointsy):
                raise Exception('The number of x-coordinates does not match the number of y-coordinates')


    def SaveFile(self, figure, path, filename=''):
        '''generates the plot of the figure and stores it in path\filename.  If filename='' (default) then the file becomes a randomly generated guid filename.
        the filename is returned (with  path)'''

        figure.savefig(self.FileLocation)
        self.GeneratedFile = True


class IQPicture_Scatter(IQPicture):
    def __init__(self, aRandomGenerator, fitexpression, labelpointsx, labelpointsy, picId, graphicsfolder, xcoordinates,
                 ycoordinates, xlabel, ylabel, title, scale=50):
        IQPicture.__init__(self, aRandomGenerator, labelpointsx, labelpointsy, graphicsfolder, picId)
        # xcoordinates and ycoordinates are maths expression which will contain a matrix with one row
        # xpts and ypts are the corresponding lists containing the contents of xcoordinates and ycoordinates resp

        xpts = str(xcoordinates).split(',')
        ypts = str(ycoordinates).split(',')

        for i in range(0, len(xpts)):
            xpts[i] = Expression.EvalExpression(str(xpts[i]), True, aRandomGenerator).Evaluate()
            ypts[i] = Expression.EvalExpression(str(ypts[i]), True, aRandomGenerator).Evaluate()

        axis([min(xpts) - 1, max(xpts) + 1, min(ypts) - 1, max(ypts) + 1])
        plt.plot(xpts, ypts, 'o')
        self.scale = float(scale) / 100

        if fitexpression != '' and fitexpression != None:
            mthExpression = Expression.EvalExpression(fitexpression, True, aRandomGenerator)
            agraphExpr = mthExpression.ExpressionStringEval
            agraphExpr = agraphExpr.replace('^', '**')

            def fit(x):
                return eval(agraphExpr)

            x = np.linspace(min(xpts) - 1, max(xpts) + 1)
            y = eval(agraphExpr)
            plt.plot(x, y, 'b-', lw=1)

        # plot the specific points
        if self.labelpointsx != None and self.labelpointsy != None:
            for i in range(0, len(self.labelpointsx)):
                self.labelpointsx[i] = Expression.EvalExpression(str(self.labelpointsx[i]), True,
                                                                 self.RandomGenerator).Evaluate()
                self.labelpointsy[i] = Expression.EvalExpression(str(self.labelpointsy[i]), True,
                                                                 self.RandomGenerator).Evaluate()
                plt.plot(self.labelpointsx[i], self.labelpointsy[i], 'ro')
                coordtext = '(' + str(self.labelpointsx[i]) + ',' + str(self.labelpointsy[i]) + ')'
                plt.text(self.labelpointsx[i], self.labelpointsy[i], coordtext)

        self.latexCode = '\\includegraphics[scale=' + str(self.scale) + ']{gfx/' + self.filename + '}'
        return self.SaveFile(plt, './/', '')


class IQPicture_SimpleCartesian(IQPicture):
    def __init__(self, aRandomGenerator, labelpointsx, labelpointsy, picId, graphicsfolder, graphExpr, xfrom, xto,
                 xstep, yfrom, yto, xlabel, ylabel, title, scale=50):
        IQPicture.__init__(self, aRandomGenerator, labelpointsx, labelpointsy, graphicsfolder, picId)

        self.xFrom = Expression.EvalExpression(xfrom, True, aRandomGenerator).Evaluate()
        self.xTo = Expression.EvalExpression(xto, True, aRandomGenerator).Evaluate()
        # if the user has specified the domain in the wrong way, switch it round (e.g. a domain from 1->-3 will be changed to -3 -> 1
        if self.xFrom > self.xTo:
            tmp = self.xFrom
            self.xFrom = self.xTo
            self.xTo = tmp

        self.yFrom = Expression.EvalExpression(yfrom, True, aRandomGenerator).Evaluate()
        self.yTo = Expression.EvalExpression(yto, True, aRandomGenerator).Evaluate()

        # if the user has specified the domain in the wrong way, switch it round (e.g. a domain from 1->-3 will be changed to -3 -> 1
        if self.yFrom > self.yTo:
            tmp = self.yFrom
            self.yFrom = self.yTo
            self.yTo = tmp

        self.xStep = float(xstep)
        self.scale = float(scale) / 100

        if xlabel <> '':
            self.xLabel = '$' + Expression.EvalExpression(xlabel, True, aRandomGenerator).GetLateXMathExpression(None) + '$'
        else:
            self.xLabel = ''

        if ylabel <> '':
            self.yLabel = '$' + Expression.EvalExpression(ylabel, True, aRandomGenerator).GetLateXMathExpression(None) + '$'
        else:
            self.yLabel = ''

        self.Titles = title.split(',')
        for i in range(0, len(self.Titles)):
            self.Titles[i] = Expression.EvalExpression(self.Titles[i], True, aRandomGenerator).ExpressionStringEval
            self.Titles[i] = '$' + Expression.EvalExpression(self.Titles[i], True,
                                                             aRandomGenerator).GetLateXMathExpression(None) + '$'
            # create the maths expressions
        mathExpressions = graphExpr.split(',')

        for i in range(0, len(mathExpressions)):
            mthExpression = Expression.EvalExpression(mathExpressions[i], True, aRandomGenerator)
            mthExpression = Expression.EvalExpression(mthExpression.ExpressionStringEval, True, aRandomGenerator)
            self.mthExpressions.append(mthExpression)
            # self.graphExpr = mthExpression.ExpressionStringEval
            # self.graphExpr = self.graphExpr.replace('^','**')
        self.GenerateFile('.\\', '')

        self.latexCode = '\\includegraphics[scale=' + str(self.scale) + ']{gfx/' + self.filename + '}'


    def GenerateFile(self, path, filename=''):
        labelpositionsx = []

        for MathExpressionIdx in range(0, len(self.mthExpressions)):
            x = np.linspace(self.xFrom, self.xTo)
            y = []

            self.RandomGenerator.AddVariableFromExpressionString('x', '0', True, False)
            for i in range(0, len(x)):
                self.RandomGenerator.SetValueByName('x', x[i])
                yValue = self.mthExpressions[MathExpressionIdx].Evaluate()
                y.append(yValue)

            self.RandomGenerator.RemoveVariableByName('x', False)

            if MathExpressionIdx == 0:
                fig, ax = plt.subplots()


            #-- Set axis spines at 0
            for spine in ['left', 'bottom']:
                ax.spines[spine].set_position('zero')

            # Hide the other spines...
            for spine in ['right', 'top']:
                ax.spines[spine].set_color('none')

            #-- Decorate the spins
            arrow_length = 20 # In points

            # X-axis arrow
            ax.annotate('X', xy=(1, 0), xycoords=('axes fraction', 'data'),
                        xytext=(arrow_length, 0), textcoords='offset points',
                        ha='left', va='center',
                        arrowprops=dict(arrowstyle='<|-', fc='black'))

            # Y-axis arrow
            ax.annotate('Y', xy=(0, 1), xycoords=('data', 'axes fraction'),
                        xytext=(0, arrow_length), textcoords='offset points',
                        ha='center', va='bottom',
                        arrowprops=dict(arrowstyle='<|-', fc='black'))



            #-- Plot
            # plt.title(self.Title)
            if self.xLabel <> '':
                plt.xlabel(self.xLabel)
            if self.yLabel <> '':
                plt.ylabel(self.yLabel)
            ax.axis([self.xFrom, self.xTo, self.yFrom, self.yTo])
            ax.grid(True)

            # plot the specific points
            if self.labelpointsx != None and self.labelpointsy != None:
                for i in range(0, len(self.labelpointsx)):
                    self.labelpointsx[i] = Expression.EvalExpression(str(self.labelpointsx[i]), True,
                                                                     self.RandomGenerator).Evaluate()
                    self.labelpointsy[i] = Expression.EvalExpression(str(self.labelpointsy[i]), True,
                                                                     self.RandomGenerator).Evaluate()
                    plt.plot(self.labelpointsx[i], self.labelpointsy[i], 'ro')
                    coordtext = '(' + str(self.labelpointsx[i]) + ',' + str(self.labelpointsy[i]) + ')'
                    plt.text(self.labelpointsx[i] + (abs(self.xFrom - self.xTo)) / 40, self.labelpointsy[i], coordtext)

            # Point at each graph with a title and label them not all at the same point
            # try to be intelligent about where to label the graph so that it is not too close to the a or b in the domain [a,b]

            foundsuitableposition = False
            print 'generating the graph ' + self.Titles[MathExpressionIdx]

            if self.Titles[MathExpressionIdx] != '':

                for i in range(int(round(len(x) / 10)), int(9 * round(len(x) / 10))): #don't label at the domain edges
                    # don't want the label too close to the x-axis so make it 20% away from it
                    if math.fabs(y[i]) < self.yTo and  y[i] > self.yFrom:
                        # check that we don't already have a label in the vacinity - tody
                        labelpositionsx.append(i)
                        foundsuitableposition = True
                        break
                if not foundsuitableposition:
                    # can't find - put it in the default position
                    labelindex = int(round((MathExpressionIdx + 1) * len(x) / (len(self.mthExpressions) + 1)))
                    labelpositionsx.append(labelindex)

                # figure out if the function is increasing or decreasing
                # because we change the pointer arrows accordingly

                if y[labelpositionsx[MathExpressionIdx] - 1] < y[labelpositionsx[MathExpressionIdx]]:
                    # function is increasing
                    ax.annotate(self.Titles[MathExpressionIdx],
                                xy=(x[labelpositionsx[MathExpressionIdx]], y[labelpositionsx[MathExpressionIdx]]),
                                xycoords='data',
                                xytext=(-70, -60), textcoords='offset points',
                                size=20,
                                bbox=dict(boxstyle="round4,pad=.5", fc="0.8"),
                                arrowprops=dict(arrowstyle="->",
                                                connectionstyle="angle,angleA=0,angleB=-90,rad=10"),
                    )

                else:
                    # function must be decreasing or stationary
                    ax.annotate(self.Titles[MathExpressionIdx],
                                xy=(x[labelpositionsx[MathExpressionIdx]], y[labelpositionsx[MathExpressionIdx]]),
                                xycoords='data',
                                xytext=(-50, 30),
                                textcoords='offset points',
                                bbox=dict(boxstyle="round", fc="0.8"),
                                arrowprops=dict(arrowstyle="->",
                                                connectionstyle="angle,angleA=0,angleB=90,rad=10"),
                    )


            # Plot the actual graph
            plt.plot(x, y)

        return self.SaveFile(plt, path, filename)
        
    
    
