'''
Created on May 23, 2013

@author: david_g_wild
'''

from __future__ import division
import re
import math
import decimal
import fractions

import random

import definitions
import Randoms
from definitions import tokenRandomiser, tokenRandomRange, tokenRandomString, \
    tokenEvaluate, tokenScientificFunctionName



class NoPictureException(Exception):
    pass

class Expression:
    '''object that is a maths expression'''

    # InputOnly is True when the maths expression only contains ones which can be input by students (e.g. for evaluation)
    InputOnly = False

    def setSyntaxError(self, aError):
        #only set the error if it hasn't already been set
        if self.syntaxError == '':
            self.syntaxError = aError

    def __init__(self, ExpressionString, MakeLegal, aRandomGenerator):
        # InfixArray holds the tokens in an infix array (e.g. 1+x)
        self.syntaxError = ''
        self.ExpressionString = ExpressionString
        self.LatexCode = ''

        print('Creating expression :' + str(ExpressionString))
        self.RandomGenerator = aRandomGenerator
        ExpressionString = self.ScientificNotation(ExpressionString)
        ExpressionString = self.ImpliedMultiplication(ExpressionString)

        if self.RandomGenerator.EvaluatedAll:
            ExpressionString = self.ReplaceEvalFns(ExpressionString)
        self.ExpressionStringEval = ExpressionString

        self.InfixArray = []

        # PostfixArray holds the tokens in a post fix array (e.g. x,1,+)
        self.PostfixArray = []
        self.ClearAll()
        self.InsertTokensFromString(ExpressionString, 0, False)
        #self.MakeUnaries()


        Fixed = not self.MakeLegal(0, len(self.InfixArray), 'red')
        while Fixed:
            Fixed = not self.MakeLegal(0, len(self.InfixArray), 'red')

        self.InFixToPostFix()

    '''------------------------------------------------------------------------------
     * NAME       : IsDigit
     * PURPOSE    : Checks whether the character specified by chrArg is a numeric 
     *              character.
     * PARAMETERS : chrArg - The character to be checked
     * RETURNS    : False - If chrArg is not a numeric character
     *              True - Otherwise 
     *----------------------------------------------------------------------------'''

    def IsDigit(self, chrArg):
        return chrArg in definitions.listDigits

    '''
* 
* Purpose - Checks whether the specified parameter is a boolean value.
* @param : stringValue - The string to be checked.
* RETURNS    : True - If supplied parameter is a boolean constant
*              False - Otherwise
*----------------------------------------------------------------------------'''

    def IsBoolean(self, stringValue):
        return False

    # {
    #     var varType = typeof(stringValue)
    #     var strTmp  = null
    #
    #     if (varType == "boolean") return true
    #     if (varType == "number" || varType == "function" || varType == undefined)
    #         return false
    #     if (IsNumber(stringValue)) return false
    #     if (varType == "object")
    #     {
    #         strTmp = stringValue.toString()
    #         if (strTmp.toUpperCase() == "TRUE" || strTmp.toUpperCase() == "FALSE")
    #             return true
    #     }
    #     if (stringValue.toUpperCase() == "TRUE" || stringValue.toUpperCase() == "FALSE")
    #         return true
    #     return false
    # }

    def IsNumber(self, stringValue):
        return (re.search('^(-|%){0,1}\d*\.{0,1}\d+$', str(stringValue)) != None)


    def IsFloat(self, stringValue):
        if self.IsNumber(stringValue):
            if float(stringValue).is_integer():
                return False
            else:
                return True
        else:
            return False

    def IsInt(self, stringValue):
        if self.IsNumber(stringValue):
            if float(stringValue).is_integer():
                return True
            else:
                return False
        else:
            return False


    def convertStringToNumber(self, stringValue):

        if type(stringValue) is str:
            return float(stringValue) if '.' in stringValue else int(stringValue)
        else:
            # floating point stuff is strange in python
            if math.fabs(math.modf(stringValue)[0]) < 0.0000000001:
                return int(stringValue)
            else:
                return stringValue
        # elif stringValue is float:
        #     return stringValue
        # else:
        #
        #     try:
        #         return int(stringValue)
        #     except exceptions.ValueError:
        #         return float(stringValue)


    '''------------------------------------------------------------------------------
     * 
     * PURPOSE Checks whether the character specified by chrArg is a alphabet 
     * @param  chrArg - The character to be checked
     * @return False - If chrArg is not a alphabet
     *         True - Otherwise 
     *----------------------------------------------------------------------------'''

    def IsAlpha(self, chrArg):
        return (str(chrArg) in definitions.listAlpha) or (str(chrArg).lower() in definitions.listAlpha) or (
            str(chrArg).upper() in definitions.listAlpha)


    '''------------------------------------------------------------------------------
     * 
     * PURPOSE    : Checks whether the string specified by strArg is an operator
     * @param strArg - The string to be checked
     * @return False - If strArg is not an operator symbol
     *         True - Otherwise 
     *----------------------------------------------------------------------------'''

    def IsOperator(self, strArg):
        return strArg in definitions.listArithOps

    def ClearAll(self):
        del self.InfixArray[:]
        del self.PostfixArray[:]


    def ReturnOperator(self, strArg):
        if self.IsOperator(strArg):
            return definitions.listArithOps[definitions.listArithOps.index(strArg)]
        else:
            raise Exception('Incorrect call to ReturnOperator')

    def IsRelation(self, aRelatorString):
        return aRelatorString in definitions.listCompaOps


    def ReturnRelation(self, aRelatorString):
        if self.IsRelation(aRelatorString):
            return definitions.listCompaOps[definitions.listCompaOps.index(aRelatorString)]
        else:
            raise Exception('Incorrect call to ReturnRelation ')


    '''------------------------------------------------------------------------------
     * NAME       : IsFunction
     * PURPOSE    : Checks whether the string specified by strArg is a function name
     * PARAMETERS : strArg - The string to be checked
     * RETURNS    : False - If strArg is not a valid built-in function name.
     *              True - Otherwise 
     *----------------------------------------------------------------------------'''

    def IsFunction(self, strArg):
        return str(strArg).upper() in definitions.listFuncOps


    def IsGreekLetter(self, strArg):
        return str(strArg) in definitions.listGreekLetters

    def IsString(self, strArg):
        return self.TokenType(str(strArg), None) == 'STRING'


    def IsSeparator(self, strArg):
        return str(strArg) in definitions.listSeparators or str(strArg).lower in definitions.listSeparators or str(
            strArg).upper in definitions.listSeparators

    def IsDelimiter(self, strArg):
        return str(strArg) in ['(', ')']

    # returns true if aToken is a special token, such as PI, 
    def IsSpecialToken(self, aToken):
        return str(aToken) in definitions.special_cases


    def Tokanize(self, aExpr, automendbrackets):
        intCntr = 0
        intBraces = 0
        intIndex = 0
        strToken = ""
        arrTokens = []
        del arrTokens[:]
        aExpr = str(aExpr).strip()

        while (intCntr < len(aExpr)):
            chrChar = aExpr[intCntr: intCntr + 1]

            # // more unusual operators such as \pm for plusorminus
            if chrChar == "\\":
            # keep reading characters until a space or non alpha is found
                arrTokens.append('\\')
                nextCharacterCounter = intCntr + 1
                nextCharacter = aExpr[nextCharacterCounter: nextCharacterCounter + 1]
                while (not nextCharacter  in  [" "]) and (nextCharacter != ""):
                    arrTokens[intIndex] = arrTokens[intIndex] + nextCharacter
                    nextCharacterCounter = nextCharacterCounter + 1
                    nextCharacter = aExpr[nextCharacterCounter: nextCharacterCounter + 1]
                    intCntr = intCntr + 1
                intIndex = intIndex + 1


            elif chrChar == " ":

                if len(strToken) > 0:
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                    strToken = ""

            elif chrChar == "(":

                intBraces = intBraces + 1
                if len(strToken) > 0:
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                    strToken = ""

                arrTokens.append(chrChar)
                intIndex = intIndex + 1

            elif chrChar == ")":
                intBraces = intBraces - 1
                if len(strToken) > 0:
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                    strToken = ""

                arrTokens.append(chrChar)
                intIndex = intIndex + 1

            elif chrChar == "^":
                if len(strToken) > 0:
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                    strToken = ""

                arrTokens.append(chrChar)
                intIndex = intIndex + 1

            elif (chrChar == "*") or (chrChar == "\u2062"):
                if len(strToken) > 0:
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                    strToken = ""

                arrTokens.append(chrChar)
                intIndex = intIndex + 1

            elif chrChar == "/":
                if (len(strToken) > 0):
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                    strToken = ""
                arrTokens.append(chrChar)
                intIndex = intIndex + 1

            elif chrChar == "%":
                if len(strToken) > 0:
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                    strToken = ""

                arrTokens[intIndex] = chrChar
                intIndex = intIndex + 1

            elif chrChar == "&":
                if len(strToken) > 0:
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                    strToken = ""

                arrTokens[intIndex] = chrChar
                intIndex = intIndex + 1

            elif chrChar == "|":
                if len(strToken) > 0:
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                    strToken = ""

                arrTokens.append(chrChar)
                intIndex = intIndex + 1

            elif (chrChar == "," ) or (chrChar == ";" ):
                if len(strToken) > 0:
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                    strToken = ""

                arrTokens.append(chrChar)
                intIndex = intIndex + 1

            elif chrChar == "-":
                if len(strToken) > 0:
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                    strToken = ""
                arrTokens.append(chrChar)
                intIndex = intIndex + 1
                strToken = ""


            elif chrChar == "+":
                if len(strToken) > 0:
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                    strToken = ""
                arrTokens.append(chrChar)
                intIndex = intIndex + 1
                strToken = ""



            elif self.IsRelation(chrChar):

                # keep reading characters until no longer have a relation
                if len(strToken) > 0:
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                    strToken = ""

                strToken = chrChar
                chrNext = aExpr[intCntr + 1:intCntr + 2]
                while (chrNext != None) and (chrNext != "") and (self.IsRelation(strToken + chrNext)):
                    strToken = strToken + chrNext
                    intCntr = intCntr + 1
                    chrNext = aExpr[intCntr + 1:intCntr + 2]

                arrTokens.append(strToken)
                intIndex = intIndex + 1
                strToken = ""



            elif chrChar == "'":
                if len(strToken) > 0:
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                intPos = aExpr.find(chrChar, intCntr + 1)
                if (intPos < 0):
                    raise Exception('Unterminated string constant')
                else:
                    strToken = strToken + aExpr[intCntr + 1:intPos]
                    arrTokens.append(chrChar + strToken + chrChar) # keep the quotes
                    intIndex = intIndex + 1
                    strToken = ""
                    intCntr = intPos

            elif chrChar == '"':
                if len(strToken) > 0:
                    arrTokens.append(strToken)
                    intIndex = intIndex + 1
                intPos = aExpr.find(chrChar, intCntr + 1)
                if (intPos < 0):
                    raise Exception('Unterminated string constant')
                else:
                    strToken = strToken + aExpr[intCntr + 1:intPos]
                    arrTokens.append(chrChar + strToken + chrChar) # keep the quotes
                    intIndex = intIndex + 1
                    strToken = ""
                    intCntr = intPos

            elif chrChar == "\"":
                if len(strToken) > 0:
                    arrTokens[intIndex] = strToken
                    intIndex = intIndex + 1
                    strToken = ""

                intPos = aExpr.find(chrChar, intCntr + 1)
                if (intPos < 0):
                    raise Exception("Unterminated string constant : " + strToken);

                else:
                    strToken = strToken + aExpr[intCntr + 1: intPos]
                    arrTokens.append(strToken)
                    #arrTokens[intIndex] = strToken
                    intIndex = intIndex + 1
                    strToken = ""
                    intCntr = intPos

            else:
                strToken = strToken + chrChar

            intCntr = intCntr + 1
            # end while
        if (intBraces > 0):
            if (automendbrackets):
                for i in range(0, intBraces - 1):
                    arrTokens.append(")")
                print( "Missing " + str(intBraces) + " closing brackets on expression " + self.ExpressionString )

        if len(strToken) > 0:
            arrTokens.append(strToken)

        return arrTokens;

    def Precedence(self, pstrTok):
        if (pstrTok in ['-', '+']):
            return 5
        elif pstrTok in ['*', '\\times', '\u2062', '/']:
            return 6
        elif (pstrTok == "^"):
            return 10
        elif pstrTok in [definitions.UNARY_NEG, definitions.UNARY_PM, definitions.UNARY_MP, '!']:
            return 7
        elif (pstrTok == "("):
            return 99
        elif (pstrTok == "&"):
            return 3
        elif (pstrTok == "|"):
            return 3
        elif (pstrTok in [definitions.tokenfunctioniser]):
            return 98
        elif self.IsRelation(pstrTok):
            return 4
        elif self.IsFunction(pstrTok):
            return 9
        elif self.IsOperator(pstrTok):
            return 5
        elif self.IsNumber(pstrTok):
            return 0.1
        elif self.IsGreekLetter(pstrTok):
            return 0
        elif self.IsString(pstrTok):
            return 0
        elif self.TokenType(pstrTok) == "VARIABLE":
            return 0
        else:
            return 0


    '''------------------------------------------------------------------------------
     * NAME       : GetTokenType(strArg)
     * PURPOSE    : Returns a tokType enumeration depending on what type of token there is
     * PARAMETERS : strArg  - the string of the token
     * RETURNS    : Returns a tokType enumeration depending on what type of token there is
     *              Returns unknown otherwise.
     *----------------------------------------------------------------------------'''

    def TokenType(self, strArg, NextTok=None):
        if (strArg == None):
            return ""
        elif (str(strArg).upper() == "PI" or str(strArg).upper() == "FUDGE"):
            return "SPECIAL"
        elif (str(strArg) == ""):
            return ""
        elif (self.IsFunction(str(strArg))):
            return "FUNCTION"
        elif (strArg == definitions.ARG_TERMINAL):
            return "TERMINAL"
        elif (self.IsOperator(str(strArg))):
            return "OPERATOR"
        elif (self.IsAlpha(strArg)):
            return "VARIABLE"
        elif (self.IsDigit(str(strArg))):
            return "NUMBER"
        elif (self.IsRelation(str(strArg))):
            return "RELATION"
        elif (self.IsDelimiter(str(strArg))):
            return "DELIMITER"
        elif (self.IsSeparator(str(strArg))):
            return "SEPARATOR"


        elif (re.search('^[a-zA-Z_\\\]+[_0-9]*$', str(strArg)) != None):
            return "VARIABLE"
        elif (re.search('^\".*\"$', str(strArg)) != None):
            return "STRING"

        elif (re.search('^(-|%){0,1}\d*\.{0,1}\d+$', str(strArg)) != None):
            return "NUMBER"
        else:
            return "UNKNOWN"


    def MakeUnaries(self):
        index = 0;
        result = False

        while (index <= len(self.InfixArray) - 1):

            ThisToken = self.InfixArray[index]
            #// if the token is allowed to be changed to unary then do so if necessary
            #// change a x-+4 to x-fudge+4
            if ((self.InfixArray[index] == "+") and (self.InfixArray[index - 1] == "-")):
                self.InfixArray.insert(index, "FUDGE")
                result = False

            elif ((index < len(self.InfixArray) - 1) and (
                    self.TokenType(ThisToken, self.InfixArray[index + 1]) == "OPERATOR") and (ThisToken == "-")):
                #// ThisToken is allowed to be changed to unary
                if index == 0: # {  //{ minus in first token must be unary }
                    #// convert -x to 0-x - we use "FUDGE" so that if the student types 0-x we do not delete their 0
                    self.InfixArray.insert(index, "FUDGE");
                #//infixTokenArray[index]=UNARY_NEG;


                else:
                    #//{ it's neither the last or the first token in the list }
                    if ((self.TokenType(self.InfixArray[index - 1]) == "DELIMITER") and (
                            self.InfixArray[index] == "-") and (self.InfixArray[index - 1] == "(")):

                        #// any operator following an open bracket must be unary
                        #//infixTokenArray[index]=UNARY_NEG;
                        #// convert -x to 0-x
                        self.InfixArray.insert(index, "FUDGE")
                        result = False

                    elif (
                            (self.TokenType(self.InfixArray[index - 1]) == "OPERATOR") and (
                                self.InfixArray[index] == "-")):
                        self.InfixArray[index] = definitions.UNARY_NEG
                        #//convert -x to 0-x
                        #//infixTokenArray.splice(index,0,"FUDGE");
                        result = False

            elif ((self.TokenType(ThisToken) == "NUMBER")):
                ThisToken = self.convertStringToNumber(ThisToken)
                if ThisToken < 0:
                    #// turn -6 into two tokens: %,6
                    saveindex = index
                    index = -1
                    self.InfixArray[saveindex] = "-"
                    #//todo, look at the formatting of this
                    self.InfixArray.insert(saveindex + 1, abs(ThisToken))

                    result = False



            elif ((self.TokenType(ThisToken) == 'VARIABLE')):
                ThisTokenArray = ThisToken.split("-")
                if (ThisTokenArray[0] == "-"):
                    #// turn -variable into two tokens %,variable
                    saveindex = index;
                    index = -1;
                    self.InfixArray[saveindex] = "-"
                    self.InfixArray.insert(saveindex + 1, ThisTokenArray[1]);
                    result = False;

            index = index + 1

        return result;

    def GetFunctionArgCount(self, functionName):
        FN = functionName.upper()
        if FN in ["POINT", "PERM", "COMB", "FRACTION", "HCF", definitions.tokenColouringFunctionName,"NROOT","DP"]:
            return 2


        elif FN in ["DEFINT", "CIRCDEFINT"]:
            return 4

        elif FN in ["CIRCLOWINT", "DIFFPRIME", "LOWINT", "LIMIT", "DEFSUM", "PDIFF", "DIFF", "BRACKET"]:
            return 3

        elif FN in ["LOGBASE", "CIRCINT", "INT", "LOWSUM", definitions.tokenScientificFunctionName,"INVERSE","SUB","SUP",
                    "SUBSCRIPT","SUPERSCRIPT"]:
            return 2

        elif FN in ["SUM", "FACTORIAL", "CONJUGATE", definitions.tokenfunctioniser,
                    definitions.tokenStringifyFunctionName,
                    definitions.tokenEvaluate, "PICTURE","ROUND",'ANSWERLINES','LATEX','OVERLINE','OVERDOT']:
            return 1

        elif FN in ['BOLD', 'SURD']:
            return 1
        elif FN in ["VECTOR", "ROWVECTOR", "MATRIX", "DET", "SET","COEFF","MAX","MIN"]:
            return -1 #// unknown how many

        # randomisation stuff here
        elif FN in [definitions.tokenRandomiser, definitions.tokenRandomString, definitions.tokenRandomMatch, 'LIST']:
            return -1
        elif FN in [definitions.tokenRandomRange]:
            return 3



        else:
            return 1;

    def HandleFunctions_Evaluate(self, pstrTok, pStack, precedenceStack, pdtFormat, parrVars):
        # evaluates functions
        if not self.IsFunction(pstrTok):
            raise Exception("Unsupported function token [" + pstrTok + "]");

        varTmp = pstrTok.upper()
        arguments = []
        arrPrecedences = []

        while len(pStack) > 0:
            varTerm = definitions.ARG_TERMINAL
            varTerm = pStack.pop()
            varTermPrecedence = precedenceStack.pop()
            if varTerm != definitions.ARG_TERMINAL:
                arguments.insert(0, varTerm)

                arrPrecedences.insert(0, varTermPrecedence)
            else:
                break;

        RequiredArgumentCount = self.GetFunctionArgCount(varTmp)

        if (RequiredArgumentCount != -1) and (len(arguments) != RequiredArgumentCount):
            pStack.append(varTmp + " requires " + RequiredArgumentCount + " argument(s)!")
            return;

        if RequiredArgumentCount == 1:
            varTerm = arguments[0]
            varTermPrecedence = arrPrecedences[0]

        if varTmp == definitions.tokenColouringFunctionName:
            raise Exception('Invalid call to unEvaluable function ' + varTmp)



        elif varTmp == definitions.tokenScientificFunctionName:
            output = arguments[0] * (10 ^ arguments[1])
            pStack.append(output)

        elif varTmp == definitions.tokenStringifyFunctionName:
            #pStack.append(re.sub('\{.\}/g', '\g<1>',arguments[0]))
            pStack.append(re.sub('\{(.+)\}', '\\textrm{\g<1>}', arguments[0]))
#TODO:  Don't have latex in the evaluate function
        elif varTmp == "VECTOR":
            raise Exception('Cannot yet evaluate a vector')
        elif varTmp == 'BOLD':
            raise Exception('Cannot evaluate function ' + varTmp)

        elif varTmp in [tokenRandomiser]: # random
            # The function random.  It's syntax is random(range1;range2;...;rangeN) where rangei is a function range(start,end,step)
            # Rangei have all been evaluated at this point and are stored in the arguments array as RandomRange objects

            # weights holds the arguments sorted by NumOutcomes in descending order
            weights = list(arguments)
            weights.sort(key=lambda x: x.NumOutcomes)
            weights.reverse()

            TotalOutcomes = 0
            OutcomesCtr = 0

            # Calculate the total number of outcomes 
            for OutcomesCtr in range(0, len(weights)):
                TotalOutcomes = TotalOutcomes + weights[OutcomesCtr].NumOutcomes


            # pick a random number between 1 and TotalOutcomes.  This will determine which range we choose to select our random from
            picker = random.randrange(0, TotalOutcomes) + 1

            OutcomesCtr = 0
            OutcomeSubtotal = 0
            while OutcomesCtr in range(0, len(weights)):
                OutcomeSubtotal = OutcomeSubtotal + weights[OutcomesCtr].NumOutcomes
                if OutcomeSubtotal >= picker:
                    # we have selected the correct range - break
                    break
                OutcomesCtr = OutcomesCtr + 1
            SelectedRange = weights[OutcomesCtr]

            output = random.randint(0, int(round((
                                                     SelectedRange.RangeEnd - SelectedRange.RangeStart) / SelectedRange.RangeStep))) * SelectedRange.RangeStep + SelectedRange.RangeStart

            # fix potential floating point rounding errors

            NumDecimalPoints = decimal.Decimal(str(SelectedRange.RangeStep)).as_tuple().exponent
            if NumDecimalPoints > 0:
                output = round(output, -NumDecimalPoints)

            pStack.append(output)


        elif varTmp in [tokenRandomRange]: # range
            #pStack.append( random.randrange(arguments[0],arguments[1]+arguments[2],arguments[2]))
            # adding a range object on the stack.  I do this instead of storing the actual evaluation because I want to keep
            # track of the weights
            pStack.append(
                Randoms.RandomRange(self.convertStringToNumber(arguments[0]), self.convertStringToNumber(arguments[1]),
                                    self.convertStringToNumber(arguments[2])))

        elif varTmp in [tokenRandomString]: # randomstr
            pStack.append(arguments[random.randint(0, len(arguments) - 1)])


        elif varTmp in [tokenEvaluate]: # eval
            pStack.append(arguments[0])

        elif varTmp in [
            definitions.tokenRandomMatch]: #match(condition1,outcome1;condition2,outcome2;.....;defaultoutcome)

            if len(arguments) > 0:
                # if there are an odd number of arguments then the last argument represents the default
                if len(arguments) % 2 != 0:
                    defaultvalue = arguments[-1]
                else:
                    defaultvalue = None
                for argcounter in range(0, len(arguments) - 1):
                    # odd arguments are conditions and even arguments are values.  We pick the first True condition and shortcut to save processing
                    if argcounter % 2 == 0: # conditions
                        if arguments[argcounter]:
                            defaultvalue = arguments[argcounter + 1]
                            break
                if defaultvalue == None:
                    raise Exception('No outcomes selected with use of ' + varTmp + ' function')
                else:
                    if isinstance(defaultvalue, str):
                        pStack.append(defaultvalue)
                    else:
                        pStack.append(defaultvalue)

        elif varTmp == 'MAX':
            pStack.append(max(arguments))

        elif varTmp == 'MIN':
            pStack.append(min(arguments))


        elif varTmp in ["MATRIX", "DET"]:
            raise Exception('cannot yet evaluate ' + varTmp + ' function')


        elif varTmp == "POINT":
            raise Exception('cannot yet evaluate ' + varTmp + ' function')

        elif varTmp in ["ROWVECTOR", "SET"]:
            raise Exception('cannot yet evaluate ' + varTmp + ' function')


            #// calculus functions   we want dy/dx, d^n y/ d^x  but d/dx (complex argument)
        elif varTmp in ["PDIFF", "DIFF"]:
            raise Exception('cannot yet evaluate ' + varTmp + ' function')

        elif varTmp == "DIFFPRIME":
            raise Exception('cannot yet evaluate ' + varTmp + ' function')
        elif varTmp in ["INT", "DEFINT", "LOWINT", "CIRCLOWINT", "CIRCINT", "CIRCDEFINT", "LIMIT", "SUM", "DEFSUM",
                        "LOWSUM"]:
            raise Exception('cannot yet evaluate ' + varTmp + ' function')
        elif varTmp == "CONJUGATE":
            raise Exception('cannot yet evaluate ' + varTmp + ' function')

        elif varTmp == "PERM":
            pStack.append(math.factorial(arguments[0]) / math.factorial(arguments[1]))
        elif varTmp == "COMB":
            pStack.append(math.factorial(arguments[0]) / (
                math.factorial(arguments[1]) * math.factorial(arguments[0] - arguments[1])))

        elif varTmp == "ABS":
            if self.IsInt(str(arguments[0])):
                pStack.append(int(math.fabs(arguments[0])))
            else:
                pStack.append(math.fabs(arguments[0]))

        elif varTmp == 'ROUND':
            pStack.append(int(round(arguments[0])))

        elif varTmp == "FACTORIAL":
            pStack.append(math.factorial(arguments[0]))

        elif varTmp == "FRACTION":
            pStack.append(arguments[0] / arguments[1])

        elif varTmp == "HCF":
            pStack.append(fractions.gcd(arguments[0], arguments[1]))

        elif varTmp == "DP":
            pStack.append( round(arguments[0],arguments[1]))

        elif varTmp == "SQR":
            pStack.append(arguments[0] ** 2)


        elif varTmp == "SQRT":
            pStack.append(math.sqrt(arguments[0]))

        elif varTmp == 'NROOT':
            pStack.append(self.convertStringToNumber( arguments[0]**(1/arguments[1])))

        elif varTmp == "ARCCOS":
            pStack.append(math.acos(arguments[0]))

        elif varTmp == "ARCSIN":
            pStack.append(math.asin(arguments[0]))

        elif varTmp == "ARCTAN":
            pStack.append(math.atan(arguments[0]))

        elif varTmp == "ARCSINH":
            pStack.append(math.asinh(arguments[0]))

        elif varTmp == "ARCCOSH":
            pStack.append(math.acosh(arguments[0]))

        elif varTmp == "ARCCOSECH":
            pStack.append(1 / math.asinh(arguments[0]))
        elif varTmp == "COSECH":
            pStack.append(1 / math.sinh(arguments[0]))
        elif varTmp == "COSEC":
            pStack.append(1 / math.sin(arguments[0]))
        elif varTmp == "LOGBASE":
            pStack.append(math.log(arguments[0], arguments[1]))
        elif varTmp == "SEC":
            pStack.append(1 / math.cos(arguments[0]))
        elif varTmp == "COT":
            pStack.append(1 / math.tan(arguments[0]))
        elif varTmp == "SINH":
            pStack.append(math.sinh(arguments[0]))
        elif varTmp == "COSH":
            pStack.append(math.cosh(arguments[0]))
        elif varTmp == "COS":
            pStack.append(math.cos(arguments[0]))
        elif varTmp == "LOG":
            pStack.append(math.log10(arguments[0]))
        elif varTmp == "SIN":
            pStack.append(math.sin(arguments[0]))
        elif varTmp == "TAN":
            pStack.append(math.tan(arguments[0]))
        elif varTmp == "LN":
            pStack.append(math.log(arguments[0]))
        elif varTmp == "COTH":
            pStack.append(1 / math.tanh(arguments[0]))
        elif varTmp == "TANH":
            pStack.append(math.tanh(arguments[0]))

        elif varTmp == "SECH":
            pStack.append(1 / math.cosh(arguments[0]))
        elif varTmp == "EXP":
            pStack.append(math.exp(arguments[0]))
        else:
            #// must be a user function
            raise Exception('Unable to evaluate the function ' + varTmp)

        #         if varTmp != definitions.tokenColouringFunctionName: #// this is just to use colour and not as precedences
        precedenceStack.append(self.Precedence(varTmp))

    def ReplaceEvalFns(self, inputStr):
        '''Finds the occurrences of eval(expression) and replace expression with its evaluation'''

        evalpos = str(inputStr).find(definitions.tokenEvaluate.lower())
        if evalpos >= 0:
            print('Found evaluation in expression ' + inputStr)
        while evalpos >= 0:

            bracketCount = 1
            if not inputStr[evalpos + 1] != '(':
                raise Exception('Found eval function but no leading (')
            for j in range(evalpos + 1 + len(definitions.tokenEvaluate), len(inputStr)):
                if inputStr[j] == '(':
                    bracketCount = bracketCount + 1
                elif inputStr[j] == ')':
                    bracketCount = bracketCount - 1
                if bracketCount == 0:
                    subExpressionStr = inputStr[evalpos + 1 + len(definitions.tokenEvaluate):j]
                    subExpression = EvalExpression(subExpressionStr, False, self.RandomGenerator)
                    subExpressionEval = subExpression.Evaluate()
                    print('Replaced ' + str(subExpression.ExpressionString) + ' with ' + str(subExpressionEval))
                    inputStr = str(inputStr).replace(definitions.tokenEvaluate.lower() + '(' + subExpressionStr + ')',
                                             str(subExpressionEval))

                    break #from for loop
                    #('Found an eval with subexpression = ' + subExpressionStr)

            evalpos = str(inputStr).find(definitions.tokenEvaluate.lower())
        return inputStr


    def HandleSurd(self, arguments):
        '''re-writes sqrt(a) as a surd - e.g. sqrt(20)=2sqrt(5)'''
        outside_root = 1
        inside_root = arguments[0]
        if self.IsInt(str(arguments[0])):
            inside_root = int(float(inside_root))
            d = 2
            while d * d <= inside_root:
                if (inside_root % (d * d) == 0): # inside_root evenly divisible by d * d
                    inside_root = inside_root / (d * d)
                    outside_root = outside_root * d
                else:
                    d = d + 1

            if outside_root == 1:
                output = '\\sqrt{' + str(int(inside_root)) + '}'
            else:
                output = str(int(outside_root)) + '\\sqrt{' + str(int(inside_root)) + '}'
        else:
            output = '\\sqrt{' + str(int(inside_root)) + '}'
        return output

    def HandleCoefficients(self, theCoeff, theExpr, isLeading=False ):
        theCoeff = eval(str(theCoeff).replace('{','(').replace('}',')'))
        theCoeff = self.convertStringToNumber(theCoeff)
        if theCoeff == 0:
            return ""
        elif theCoeff == 1:
            if isLeading:
                return theExpr
            else:
                return '+' +  theExpr
        elif theCoeff == -1:
            return '-' + theExpr

        elif theCoeff < 0:
            output =  '-' + str(self.convertStringToNumber(math.fabs(theCoeff)))
            if theExpr<>'1':
                return output + theExpr
            else:
                return output
        else: #theCoeff > 0
            if isLeading:
                output = str(theCoeff)
                if theExpr <> '1':
                    return output + theExpr
                else:
                    return output
            else:
                output = '+' + str(theCoeff)
                if theExpr <> '1':
                    return  output + theExpr
                else:
                    return output




    def HandleFunctions_LaTeX(self, pstrTok, pStack, precedenceStack, pdtFormat, parrVars, pictureList=None):

        """

        :param pstrTok:
        :param pStack:
        :param precedenceStack:
        :param pdtFormat:
        :param parrVars:
        :param pictureList:
        :raise:
        """
        if not self.IsFunction(pstrTok):
            raise Exception("Unsupported function token [" + pstrTok + "]")

        varTmp = pstrTok.upper()
        arguments = []
        arrPrecedences = []

        while len(pStack) > 0:
            varTerm = definitions.ARG_TERMINAL
            varTerm = pStack.pop()
            varTermPrecedence = precedenceStack.pop()
            if varTerm != definitions.ARG_TERMINAL:
                arguments.insert(0, varTerm)

                arrPrecedences.insert(0, varTermPrecedence)
            else:
                break;

        RequiredArgumentCount = self.GetFunctionArgCount(varTmp)

        if (RequiredArgumentCount != -1) and (len(arguments) != RequiredArgumentCount):
            if len(arguments) > RequiredArgumentCount: # too many arguments
                arguments = arguments[0:RequiredArgumentCount]
                arrPrecedences = arguments[0:RequiredArgumentCount]
                arguments[-1] = 'Invalid_Argument_Count_For_' + varTmp

            else:
                for argCount in range(0, RequiredArgumentCount - len(arguments)):
                    arguments.append('\\color{red}{?}')
                    arrPrecedences.append(self.Precedence('?'))

        if RequiredArgumentCount == 1:
            varTerm = arguments[0];
            varTermPrecedence = arrPrecedences[0]

        if varTmp == definitions.tokenColouringFunctionName:
            pStack.append(
                "\\color" + arguments[1] + "{" + arguments[0] + "} \\text{   Error: " + self.syntaxError + '}')
            #TODO  something about the precedence of the coloring function needs to be sorted
        elif varTmp == definitions.tokenEvaluate:
            raise Exception(
                'Should not encounter ' + varTmp + ' in LaTeX construction code of expression : ' + self.ExpressionString)
        #             if self.RandomGenerator != None:
        #                 # create a new expression from the argument, removing the superfluous { and }
        #                 newExpressionString = str(arguments[0]).replace('{','(')
        #                 newExpressionString = newExpressionString.replace('}',')')
        #                 newExpressionString = newExpressionString.replace('\\times ','*')
        #                 newExpressionString = newExpressionString.replace('\\times','*')
        #                 newExpressionString = newExpressionString.replace('\\left(','(')
        #                 newExpressionString = newExpressionString.replace('\\left)',')')
        #
        #                 newExpression = EvalExpression(newExpressionString, False, self.RandomGenerator )
        #
        #
        #                 pStack.append( '{' + str(newExpression.Evaluate()) + '}')
        #             else:
        #                 raise Exception('Unassigned Random Generator in call to ' + definitions.tokenEvaluate)

        elif varTmp == 'LATEX':
            # output raw latex
            pStack.append(str(arguments[0]).replace('"',''))



        elif varTmp == definitions.tokenScientificFunctionName:
            if ( arrPrecedences[0] > 0.1 ):
                output = "\\left(" + arguments[0] + "\\right)"
            else:
                output = "{" + arguments[0] + "}"
                pStack.append("{" + output + "}\\times 10^{" + arguments[1] + "}")

        elif varTmp == "COEFF":

            # even arguments are the coefficients,
            output = ""
            if not len(arguments) % 2 == 0:
                raise Exception('Expecting an even number of arguments for function COEFF')
            i = 0
            while i < len(arguments):
                output = output + self.HandleCoefficients(arguments[i], arguments[i+1], len(output)==0)
                i = i + 2

            if output <> '':
                pStack.append(output)
            else: # all the coefficients are 0
                pStack.append('0')


        elif varTmp in ['SUB','SUBSCRIPT']:
            pStack.append('{'+ arguments[0] + '}_{' + arguments[1] + '}')

        elif varTmp in ['SUP','SUPERSCRIPT']:
            pStack.append('{'+ arguments[0] + '}^{' + arguments[1] + '}')

        elif varTmp == 'LIST':
            output = ''
            for listctr in range(0,len(arguments)):
                output = output + arguments[listctr]
                if listctr < len(arguments) - 1:
                    output = output + ','
            pStack.append(output)
        elif varTmp == 'ANSWERLINES':
            # Adds a number of lines to the question to allow space for the student to answer
            try:
                numLines = int(arguments[0])
                output = ''
                for i in range(0,numLines):
                    output = output + '\hbox to \hsize{ \hfil}\\\\'
                    #output = output + '\hbox to \hsize{\dotfill\hfil}\\\\'
                pStack.append(output)
            except:
                raise Exception('The number of lines should be an integer')

        elif varTmp == 'BRACKET':
            # encloses the argument in brackets
            pStack.append('\\left' + str(arguments[1]).replace('"','') + '{' + arguments[0] + '}\\right'
                          + str(arguments[2]).replace('"',''))
        elif varTmp == 'INVERSE':
            # inverse(f,x) is rendered as f^(-1)(x)
            pStack.append(arguments[0]+'^{-1}\\left({' + arguments[1] + '}\\right)')

        elif varTmp == 'BOLD':
            pStack.append('\\mathbf{' + arguments[0] + '}')

        elif varTmp == 'PICTURE':

            # find the right picture in the pictureList
            try:
                picture = pictureList.getPicturefromId(arguments[0])
            except:
                raise NoPictureException('Picture with id=' + arguments[0] + ' does not exist')

            pStack.append(picture.latexCode)

        elif varTmp in [tokenRandomString]: # randomstr
            randomstr = arguments[random.randint(0, len(arguments) - 1)]
            pStack.append('\\mathrm{' + str(randomstr).replace('"', '') + '}')

        elif varTmp == definitions.tokenStringifyFunctionName:
            #pStack.append(re.sub('\{(.+)\}', '\\mathrm{\g<1>}', arguments[0]))
            pStack.append('\\mathrm{' + str(arguments[0]).replace('"','') +'}')
            #pStack.append("\\text{" + re.sub('\{|\}/g', arguments[0]) + "}")

        elif varTmp == 'SURD':
            output = self.HandleSurd(arguments)
            pStack.append(output)


        elif varTmp == 'FRACTION':
            # reduces a fraction a/b to :
            #     a - if b = 1
            #     a/hcf(a,b) / b/hcf(a,b) if both a and b are integer
            #     nothing if b = 0
            #
            if self.TokenType(arguments[0], None) == 'NUMBER' and self.TokenType(arguments[1], None) == "NUMBER":
                numerator = self.convertStringToNumber(arguments[0])
                denominator = self.convertStringToNumber(arguments[1])
                if denominator == 1:
                    # output numerator
                    pStack.append(arguments[0])
                elif denominator == 0:
                    # output the orginal fraction
                    pStack.append("\\frac{" + str(numerator) + "}{" + str(denominator) + "}")
                else:
                    gcd = fractions.gcd(numerator, denominator)
                    numerator = int(numerator / gcd)
                    denominator = int(denominator / gcd)
                    if denominator == 1:
                        pStack.append(str(numerator))
                    else:
                        pStack.append("\\frac{" + str(numerator) + "}{" + str(denominator) + "}")
            else:
                pStack.append("\\frac{" + arguments[0] + "}{" + arguments[1] + "}")
        elif varTmp == "OVERLINE":
            pStack.append('\\overline{' + arguments[0] +'}')

        elif varTmp == "OVERDOT":
            pStack.append('\\dot{' + arguments[0] +'}')

        elif varTmp == "VECTOR":
            if (len(arguments) == 1):
                output = "\\overrightarrow{" + arguments[0] + "}"
                pStack.append(output)

            else:
                output = "\\left(\\array{"
                for argcounter in range(0, len(arguments) - 2):
                    output = output + arguments[argcounter] + "\\cr"

                pStack.append(output + arguments[ - 1] + "}\\right)")


        elif varTmp in ["MATRIX", "DET"]:
            output = ''
            if varTmp == "MATRIX":
                output = "\\left(\\begin{array}{"
            elif varTmp == "DET":
                output = "\\left|\\begin{array}{"
            for argcounter in range(0, int((len(arguments) + 1) / 2)):
                output = output + 'c'
            output = output + '}'

            for argcounter in range(0, len(arguments)):
                matrixElement = arguments[argcounter]
                if matrixElement == "{;}":
                    output = output + "\\\\"
                else:
                    output = output + arguments[argcounter];
                    if argcounter < len(arguments) - 1 and arguments[argcounter + 1] != "{;}":
                        output = output + "&"

            if varTmp == "MATRIX":
                pStack.append(output + "\\end{array}\\right)")
            elif ( varTmp == "DET" ):
                pStack.append(output + "}\\end{array}\\right|")


        elif varTmp == "POINT":
            pStack.append("\\left(" + arguments[0] + "," + arguments[1] + "\\right)")

        elif varTmp in ["ROWVECTOR", "SET"]:
            output = ''
            if varTmp == "ROWVECTOR":
                output = "\\left(\\array{"
            elif varTmp == "SET":
                output = "\\{\\array{"
                output = output + arguments[0]

                for argcounter in range(1, len(arguments) - 2):
                    output = output + ",\\," + arguments[argcounter];

            if varTmp == "ROWVECTOR":
                pStack.append(output + ",\\," + arguments[- 1] + "}\\right)")
            elif varTmp == "SET":
                pStack.append(output + ",\\," + arguments[- 1] + "}\\}")


                #// calculus functions   we want dy/dx, d^n y/ d^x  but d/dx (complex argument)
        elif varTmp in ["PDIFF", "DIFF"]:

            xvariable = arguments[1]
            power = arguments[2]
            yvariable = arguments[0]

            if arguments[2] == "1":
                power = ""
            else:
                if arrPrecedences[2] > 1:
                    power = "^\\left(" + arguments[2] + "\\right)"
                else:
                    power = "^{" + arguments[2] + "}"


            if arrPrecedences[0] > 1:
                yvariable = "\\left(" + arguments[0] + "\\right)"
            else:
                yvariable = "{" + arguments[0] + "}"

            if arrPrecedences[1] > 1:
                xvariable = "\\left(" + arguments[1] + "\\right)"
            else:
                xvariable = "{" + arguments[1] + "}"

            diff = "unknown diff"
            if varTmp == "PDIFF":
                diff = "\\partial"
            elif varTmp == "DIFF":
                diff = "d "

            if arrPrecedences[0] == 0:
                pStack.append("\\frac{" + diff + power + yvariable + "}{" + diff + xvariable + power + "}")
            else:
                pStack.append("\\frac{" + diff + power + "}{" + diff + xvariable + power + "}" + yvariable)



        elif varTmp == "DIFFPRIME":
            fn = arguments[0]
            NumPrimes = ''
            try:
                NumPrimes = self.convertStringToNumber(arguments[2])
                if math.isnan(NumPrimes):
                    raise Exception("Number of primes is not a number in call to " + varTmp)

            except:
                raise Exception("invalid number of primes (" + str(NumPrimes) + ") specified in call to DIFFPRIME")

            primes = ''
            differand = arguments[1]

            if arrPrecedences[0] > 1:
                fn = "\\left(" + fn + "\\right)"

            for primecounter in range(0, NumPrimes):
                primes = primes + "^{\\prime} "

            differand = "\\left(" + differand + "\\right)"

            pStack.append(fn + primes + differand)
        elif varTmp in ["INT", "DEFINT", "LOWINT", "CIRCLOWINT", "CIRCINT", "CIRCDEFINT", "LIMIT", "SUM", "DEFSUM",
                        "LOWSUM"]:
            argument1 = arguments[0]
            argument2 = arguments[1]
            argument3 = ''
            argument4 = ''

            if arrPrecedences[0] == 5:
                argument1 = "\\left(" + argument1 + "\\right)"
            else:
                argument1 = "{" + arguments[0] + "}"

            if arrPrecedences[1] > 1:
                argument2 = "\\left(" + arguments[1] + "\\right)"
            else:
                argument2 = "{" + arguments[1] + "}"

            if RequiredArgumentCount >= 3:
                argument3 = "{" + arguments[2] + "}"
            if RequiredArgumentCount == 4:
                argument4 = "{" + arguments[3] + "}"

            if varTmp == "DEFINT":
                pStack.append(
                    "\\displaystyle\\int_{" + argument3 + "}^" + argument4 + "{ " + argument1 + "}\\, d" + argument2)
            elif varTmp == "DEFSUM":
                pStack.append("\\displaystyle\\sum_{" + argument2 + "}^" + argument3 + "{ " + argument1 + "}")
            elif varTmp == "LIMIT":
                pStack.append("\\displaystyle\\lim_{" + argument2 + "\\to " + argument3 + "}{ " + argument1 + "}")
            elif varTmp == "INT":
                pStack.append("\\displaystyle\\int{ " + argument1 + "}\\, d" + argument2)
            elif varTmp == "SUM":
                pStack.apend("\\displaystyle\\sum{ " + argument1 + "}")
            elif varTmp == "LOWINT":
                pStack.append("\\displaystyle\\int\\limits_{" + argument3 + "}{ " + argument1 + "}\\, d" + argument2)
            elif varTmp == "LOWSUM":
                pStack.append("\\displaystyle\\sum\\limits_{" + argument2 + "}{ " + argument1 + "}")
            elif varTmp == "CIRCDEFINT":
                pStack.append(
                    "\\displaystyle\\oint_{" + argument3 + "}^" + argument4 + "{ " + argument1 + "}\\, d" + argument2)
            elif varTmp == "CIRCLOWINT":
                pStack.append("\\displaystyle\\oint\\limits_{" + argument3 + "}{ " + argument1 + "}\\, d" + argument2)
            elif varTmp == "CIRCINT":
                pStack.append("\\displaystyle\\oint{ " + argument1 + "}\\, d" + argument2)

        elif varTmp == "CONJUGATE":
            pStack.append("\\over{" + arguments[0] + "}")

        elif varTmp == "PERM":
            pStack.append("^{" + arguments[0] + "}\\displaystyle P_{" + arguments[1] + "}")
        elif varTmp == "COMB":
            pStack.append("^{" + arguments[0] + "}\\displaystyle C_{" + arguments[1] + "}")

        elif varTmp == "ABS":
            pStack.append("\\left|" + arguments[0] + "\\right|")

        elif varTmp == "FACTORIAL":
            if arrPrecedences[0] > 1:
                pStack.append("\\left(" + arguments[0] + "\\right)!")
            else:
                pStack.append("{" + arguments[0] + "}!")
        elif varTmp == "SQR":
            if arrPrecedences[0] > 1:
                pStack.append("\\left(" + arguments[0] + "\\right)")
            else:
                pStack.append("{" + arguments[0] + "}^2")

        elif varTmp == "SQRT":
            pStack.append("\\sqrt{" + arguments[0] + "}")
        elif varTmp == "NROOT":
            pStack.append("\\sqrt[" + arguments[1] + "]" + "{" + arguments[0] + "}")

        elif varTmp == "ARCCOS":
            pStack.append("\\cos^{-1}\\left(" + arguments[0] + "\\right)")

        elif varTmp == "ARCSIN":
            pStack.append("\\sin^{-1}\\left(" + arguments[0] + "\\right)")
        elif varTmp == "ARCTAN":
            pStack.append("\\tan^{-1}\\left(" + arguments[0] + "\\right)")

        elif varTmp == "ARCSINH":
            pStack.append("\\sinh^{-1}\\left(" + arguments[0] + "\\right)")

        elif varTmp == "ARCCOSH":
            pStack.append("\\cosh^{-1}\\left(" + arguments[0] + "\\right)")
        elif varTmp == "ARCCOSECH":
            pStack.append("\\mathrm{cosech}^{-1}\\left(" + arguments[0] + "\\right)")
        elif varTmp == "ARCCOSECH":
            pStack.append("\\mathrm{cosech}^{-1}\\left(" + arguments[0] + "\\right)")
        elif varTmp == "ARCCOSEC":
            pStack.append("\\mathrm{cosec}^{-1}\\left(" + arguments[0] + "\\right)")
        elif varTmp == "LOGBASE":
            pStack.append("\\log_" + arguments[1] + "\\left(" + arguments[0] + "\\right)")
        elif varTmp in ["SEC", "COT", "SINH", "COSH", "COS", "LOG", "SIN", "TAN", "LN", "LOG", "COTH", "TANH"]:
            pStack.append("\\" + pstrTok + "\\left(" + arguments[0] + "\\right)")
        elif varTmp == "ARCSECH":
            pStack.append("\\mathrm{sech}^{-1}\\left(" + arguments[0] + "\\right)")
        elif varTmp == "EXP":
            pStack.append("e^{" + arguments[0] + "}")
        else:
            #// must be a user function
            pStack.append(pstrTok + "\\left(" + arguments[0] + "\\right)")

        #         if varTmp != definitions.tokenColouringFunctionName: #// this is just to use colour and not as precedences
        precedenceStack.append(self.Precedence(varTmp))


    def GetLateXMathExpression(self, pictureList=None):
        '''Turns a postfix array into LaTeX - as a string.  pictureObjects hold a list of defined pictures and the latex returned will point to the generated picture'''
        parrExp = self.PostfixArray
        if parrExp == None:
            raise Exception("Invalid postfix expression!")


        if len(parrExp) == 0:
            raise Exception("postfix array does not contain any characters")


        intIndex = 0
        latexStack = []
        precedenceStack = []

        while intIndex < len(parrExp):
            strTok = parrExp[intIndex]
            ThisTokType = self.TokenType(strTok)
            #             switch (TokenType(strTok.toString()))
            #             {
            if ThisTokType == "OPERATOR":

                #switch (strTok.toString()){
                if strTok == definitions.UNARY_NEG or strTok == definitions.UNARY_PM or strTok == definitions.UNARY_MP:
                    if len(latexStack) == 0:
                        raise Exception("No operand to negate!")

                    objOp1 = None
                    objOp1Precedence = None
                    objOp2 = None
                    objOp2Precedence = None

                    objOp1 = latexStack.pop();
                    objOp1Precedence = precedenceStack.pop();


                    #switch (strTok) {
                    if strTok == definitions.UNARY_NEG:
                        opToPush = '-'
                    elif strTok == definitions.UNARY_PM:
                        opToPush = "\\pm"
                    elif strTok == definitions.UNARY_MP:
                        opToPush = "\\mp";

                    else:
                        opToPush = strTok;

                    if objOp1Precedence > 1 and ( objOp1Precedence != 9 ): #TODO: make this fix in inputtool code
                        latexStack.append("{" + opToPush + "\\left(" + objOp1 + "\\right)}")
                    else:
                        latexStack.append("{" + opToPush + "{" + objOp1 + "}}");
                    precedenceStack.append(self.Precedence(strTok));


                else:
                    if (len(latexStack) == 0 or len(latexStack) < 2):
                        raise Exception("Stack is empty, can not perform [" + strTok + "] on expression " + self.ExpressionString)

                    objOp1 = None
                    objOp2 = None
                    objOp1Precedence = None;
                    objOp2Precedence = None

                    objOp2 = latexStack.pop();
                    objOp1 = latexStack.pop();
                    objOp2Precedence = precedenceStack.pop();
                    objOp1Precedence = precedenceStack.pop();
                    ThisPrecedence = self.Precedence(strTok);

                    # if we're raising a trig function to a power then render as fn^(argument)'
                    if (strTok == "^"):


                        regexprpattern = '^\\\((ARCCOSECH)|(ARCCOS)|(ARCSIN)|(ARCTAN)|(ARCSINH)|(ARCCOSH)|(COS)|(SIN)|(TAN)|(COSEC)|(SEC)|(COT)|(SINH)|(COSH)|(COSECH)|(SECH)|(COTH)|(TANH))'

                        functionmatch = re.search(regexprpattern, objOp1, re.I)
                        if (functionmatch == None):
                            Child1Text = objOp1

                            if (((objOp1Precedence <= ThisPrecedence ) and ( objOp1Precedence > 1 )) or
                                    (objOp1Precedence == self.Precedence(definitions.UNARY_NEG))):
                                Child1Text = "\\left(" + Child1Text + "\\right)"

                            Child2Text = objOp2

                            #                                     //                                    if (((objOp2Precedence <= ThisPrecedence ) && ( objOp2Precedence > 1 )) ||
                            #                                     //                                        (objOp2Precedence==Precedence(UNARY_NEG)))
                            #                                     //                                        Child2Text = "\\left(" + Child2Text + "\\right)";

                            latexStack.append("{" + Child1Text + "}" + strTok + "{" + Child2Text + "}")
                            precedenceStack.append(ThisPrecedence)

                        else:
                            functionnamearray = re.match(regexprpattern, objOp1, re.I)
                            functionname = functionnamearray.group(1)

                            functionargument = objOp1[len(functionname) + 1: len(objOp1)]

                            latexStack.append(
                                "\\mathrm{" + functionname + "}^{" + objOp2 + "}{" + functionargument + "}")

                            precedenceStack.append(ThisPrecedence)


                    elif (strTok == "/"):
                        latexStack.append("\\frac{" + objOp1 + "}{" + objOp2 + "}")
                        precedenceStack.append(ThisPrecedence)

                    elif (strTok == "+"):
                        latexStack.append("{" + objOp1 + "}" + strTok + "{" + objOp2 + "}")
                        precedenceStack.append(ThisPrecedence)


                    elif (strTok == "-"):
                        Child1Text = objOp1
                        if (((objOp1Precedence < ThisPrecedence ) and ( objOp1Precedence > 1 )) or
                                (objOp1Precedence == self.Precedence(definitions.UNARY_NEG))):
                            Child1Text = "\\left(" + Child1Text + "\\right)"

                        Child2Text = objOp2

                        if (((objOp2Precedence <= ThisPrecedence ) and ( objOp2Precedence > 1 )) or
                                (objOp2Precedence == self.Precedence(definitions.UNARY_NEG))):
                            Child2Text = "\\left(" + Child2Text + "\\right)"

                        latexStack.append(Child1Text + strTok + Child2Text)

                        precedenceStack.append(ThisPrecedence);

                    else:
                        Child1Text = objOp1;
                        if (((objOp1Precedence < ThisPrecedence ) and ( objOp1Precedence > 1 )) or
                                (objOp1Precedence == self.Precedence(definitions.UNARY_NEG))):
                            Child1Text = "\\left(" + Child1Text + "\\right)"

                        Child2Text = objOp2;

                        if (((objOp2Precedence < ThisPrecedence ) and ( objOp2Precedence > 1 )) or
                                (objOp2Precedence == self.Precedence(definitions.UNARY_NEG))):
                            Child2Text = "\\left(" + Child2Text + "\\right)"

                        if (strTok == "\\times" or strTok == "\\crossprod"):
                            latexStack.append(Child1Text + "\\times" + Child2Text)
                        elif (strTok == "*"):
                            if (objOp2Precedence == 0.1):
                                latexStack.append(Child1Text + "\\times" + Child2Text)
                            else:
                                latexStack.append(Child1Text + " " + Child2Text)

                        elif (strTok == definitions.INVISIBLE_TIMES):
                            if (objOp2Precedence == 0.1):
                                latexStack.append(Child1Text + "\\times" + Child2Text)
                            else:
                                latexStack.append(Child1Text + " " + Child2Text);
                        elif (strTok == '\\invisibletimes'):
                            latexStack.append(Child1Text + " " + Child2Text);

                        elif (strTok == "/"):
                            # TODO: This does not look right
                            if (objOp2Precedence == 0):
                                latexStack.append(Child1Text + "\\times" + Child2Text)
                            else:
                                latexStack.append(Child1Text + " " + Child2Text);

                        elif (strTok == "\\dotprod"):
                            latexStack.append(Child1Text + "\\cdot" + Child2Text)
                        elif (strTok == "\\intersect"):
                            latexStack.append(Child1Text + "\\cap" + Child2Text)
                        elif (strTok == "\\union"):
                            latexStack.append(Child1Text + "\\cup" + Child2Text)
                        elif (strTok == definitions.tokenfunctioniser):
                            latexStack.append(Child1Text + "\\left(" + Child2Text + "\\right)")
                        else:
                            latexStack.append(Child1Text + strTok + Child2Text)

                        precedenceStack.append(ThisPrecedence);

            elif ThisTokType == "FUNCTION":
                self.HandleFunctions_LaTeX(strTok, latexStack, precedenceStack, definitions.dtFormat, None, pictureList)



            elif ThisTokType == "NUMBER":
                latexStack.append(strTok);
                ThisPrecedence = self.Precedence(strTok)
                precedenceStack.append(ThisPrecedence)

            elif ThisTokType == "RELATION":
                if (len(latexStack) == 0 or len(latexStack) < 2):
                    raise Exception("Stack is empty, can not perform [" + strTok + "] on expression " + self.ExpressionString)

                LHS = None;
                RHS = None;
                LHSPrecedence = None;
                RHSPrecedence = None;

                RHS = latexStack.pop()
                LHS = latexStack.pop()
                RHSPrecedence = precedenceStack.pop()
                LHSPrecedence = precedenceStack.pop()
                ThisPrecedence = self.Precedence(strTok)
                precedenceStack.append(ThisPrecedence)

                if strTok == "<=":
                    relationString = "\\leq"
                elif strTok == ">=":
                    relationString = "\\geq"
                elif strTok == "<>":
                    relationString = "\\neq"
                elif strTok == "==":
                    relationString = "\\equiv"
                elif strTok == "==>":
                    relationString = "\\Rightarrow"
                elif strTok == "<==":
                    relationString = "\\Leftarrow"
                elif strTok == "<==>":
                    relationString = "\\Leftrightarrow"
                elif strTok == "<<":
                    relationString = "\\ll"
                elif strTok == ">>":
                    relationString = "\\gg"
                elif strTok == "\\tends":
                    relationString = "\\rightarrow"
                elif strTok == "\\notsubset":
                    relationString = "\\nsubset"
                elif strTok == "\\notsubseteq":
                    relationString = "\\nsubseteq"
                elif strTok == "\\join":
                    relationString = "\\Join"
                else:
                    relationString = strTok

                latexStack.append(LHS + relationString + RHS)

            elif ThisTokType == "VARIABLE":
            #// check for greek Letters
                if self.IsGreekLetter(strTok):
                    latexStack.append("{\\" + strTok + "}")
                else:
                    if self.RandomGenerator.GetVariableByName(strTok) == None:
                        latexStack.append("{" + strTok + "}")
                    else:
                        val = self.RandomGenerator.GetVariableByName(strTok).value
                        if isinstance(val, str):
                            latexStack.append("\\mathrm{" + str(val) + "}")
                        else:
                            latexStack.append("{" + str(val) + "}")

                ThisPrecedence = self.Precedence(strTok);
                precedenceStack.append(ThisPrecedence);
            elif ThisTokType == "STRING":
                latexStack.append("\\mathrm{" + strTok + "}")
                precedenceStack.append(self.Precedence(strTok))

            elif ThisTokType == "TERMINAL":
                latexStack.append(strTok)
                precedenceStack.append(self.Precedence(strTok))

            elif ThisTokType == "SPECIAL":

                if ( strTok.upper() == "PI" ):
                    latexStack.append("\\pi")
                    precedenceStack.append(0)

                elif ( strTok == "FUDGE" ):
                    latexStack.push("")
                    precedenceStack.push(0)
                    #// remove the FUDGE for unary minuses
            else:

            #// Handle functions and operands
            #if self.IsNumber( strTok ) or self.IsBoolean( strTok )  or self.typeof(strTok) == "BOOLEAN" or self.typeof(strTok) == 'object' or self.IsVariable(strTok) or self.IsString(strTok):

                latexStack.append("{" + strTok + "}")

                ThisPrecedence = self.Precedence(strTok)
                precedenceStack.append(ThisPrecedence)

            intIndex = intIndex + 1

        if (len(latexStack) == 0 or len(latexStack) > 1):
            raise Exception("Unable to convert to LaTeX the expression : " + self.ExpressionString)
        else:
            result = latexStack.pop()
            precedenceStack.pop()

        self.LatexCode = result
        return result;



    def IsOperand(self, aStr):
        '''
        
        :param aStr: string to see if it is an operand
        returns True if aStr represents an operand or False otherwise
        '''
        result = self.IsAlpha(aStr) or self.IsNumber(aStr) or self.IsFloat(aStr) or self.IsGreekLetter(
                aStr) or self.IsString(aStr) or self.TokenType(aStr, None) == 'VARIABLE'
        return result

    def GetUnaryOperator(self, strPrev, strThis, strNext):
        '''Returns None if This is NOT a unary operator and the relevant unary operator if it is'''
        if strThis in definitions.listUnaryOps:
            if (strPrev == None or self.IsOperator(strPrev) or strPrev == "(" or self.IsSeparator(
                    strPrev) or self.IsRelation(strPrev)):
                if (strThis == "-"):
                    return definitions.UNARY_NEG
                elif (strThis == "\\pm"):
                    return definitions.UNARY_PM
                elif (strThis == "\\mp"):
                    return definitions.UNARY_MP
                else:
                    return None
            else:
                return None
        else:
            return None


    def IsLeftAssociativeOperator(self, strOperator):
        if not self.IsOperator(strOperator):
            raise Exception('Invalid call to IsLeftAssociative operator since ' + strOperator + ' is not an operator ')
        return strOperator in definitions.listLeftAssociatedOps

    def IsRightAssociativeOperator(self, strOperator):
        if not self.IsOperator(strOperator):
            raise Exception('Invalid call to IsRightAssociative operator since ' + strOperator + ' is not an operator ')
        return strOperator in definitions.listRightAssociatedOps

    def IsParenthesis(self, aToken):
        return aToken in ['(', ')']


    def InFixToPostFix(self):
        stack = []
        del self.PostfixArray[:]
        #Given a string mathematical equation, from left to right, scan for each token.
        for i in range(0, len(self.InfixArray)):
            ThisToken = self.InfixArray[i]
            if i == 0:
                PrevToken = None
            else:
                PrevToken = self.InfixArray[i - 1]
            if i == len(self.InfixArray) - 1:
                NextToken = None
            else:
                NextToken = self.InfixArray[i + 1]
                #If token is an operand, push the token onto the output array.
            if self.IsOperand(ThisToken):
                self.PostfixArray.append(ThisToken)
            #If token is a unary postfix operator, push it onto the output array.
            elif self.GetUnaryOperator(PrevToken, ThisToken, NextToken) != None:
                stack.append(self.GetUnaryOperator(PrevToken, ThisToken, NextToken))
            elif self.IsFunction(ThisToken):
                stack.append(ThisToken)
            elif self.IsOperator(ThisToken):
                if self.IsLeftAssociativeOperator(ThisToken):
                    # if the stack is empty, something is seriously wrong!
                    while len(stack) > 0 and self.IsOperator(stack[-1]) and self.Precedence(
                            stack[-1]) >= self.Precedence(ThisToken):
                        self.PostfixArray.append(stack.pop())
                    stack.append(ThisToken)
                elif self.IsRightAssociativeOperator(ThisToken):

                    while len(stack) > 0 and self.IsOperator(stack[-1]) and self.Precedence(
                            stack[-1]) > self.Precedence(ThisToken):
                        self.PostfixArray.append(stack.pop())
                    stack.append(ThisToken)

                else:
                    raise Exception('The operator ' + ThisToken + ' is not supported on expression ' + self.ExpressionString)
            elif self.IsParenthesis(ThisToken):
                if ThisToken == '(':
                    if len(stack) > 0 and self.IsFunction(stack[-1]):
                        self.PostfixArray.append(definitions.ARG_TERMINAL)
                    stack.append(ThisToken)
                elif ThisToken == ')':
                    while len(stack) > 0 and stack[-1] != '(':
                        self.PostfixArray.append(stack.pop())
                    if len(stack) > 0 and not stack[-1] == '(':
                        raise Exception('Unbalanced parenthesis on expression ' +  self.ExpressionString)
                    else:
                        stack.pop() #not interested in the result which would be a '('
                    if len(stack) > 0 and self.IsFunction(stack[-1]):
                        self.PostfixArray.append(stack.pop())

                else:
                    raise Exception('Parenthesis ' + ThisToken + 'is not yet supported on expression ' + self.ExpressionString)

            elif self.IsSeparator(ThisToken):
                if ThisToken == ',':
                    while len(stack) > 0 and stack[-1] != '(':
                        self.PostfixArray.append(stack.pop())

                elif ThisToken == ";":
                    while len(stack) > 0 and stack[-1] != '(':
                        self.PostfixArray.append(stack.pop())

                    self.PostfixArray.append(";")
            elif self.IsRelation(ThisToken):
                if len(stack) > 0:
                    strTop = stack[-1]
                if (len(stack) == 0 or (len(stack) > 0 and strTop == "(")):
                    stack.append(ThisToken)
                elif (self.Precedence(ThisToken) > self.Precedence(strTop)):
                    stack.append(ThisToken)

                else:

                    #// pop operators with precedence >= operator strTok
                    while (len(stack) > 0):
                        strTop = stack[-1];
                        if (strTop == "(" or self.Precedence(strTop) < self.Precedence(ThisToken)):
                            break

                        else:
                            self.PostfixArray.append(stack.pop())

                    stack.append(ThisToken)


        # pop the remaining tokens on the stack and push into postfix array
        while len(stack) > 0:
            self.PostfixArray.append(stack.pop())

            # evaluate all the variables and store them on the PostFix Array as strings
        if self.RandomGenerator.EvaluatedAll:
            for i in range(0, len(self.PostfixArray)):
                if self.TokenType(self.PostfixArray[i], None) == 'VARIABLE':
                    if self.RandomGenerator.GetVariableIdxByName(self.PostfixArray[i]) >= 0:
                        self.PostfixArray[i] = str(self.RandomGenerator.GetValueByName(self.PostfixArray[i]))


    def InsertTokensFromString(self, aExprString, aInsertPos, automendbrackets=False):

        newtokens = self.Tokanize(aExprString, automendbrackets)

        #if inserting in the middle of the array
        if aInsertPos >= 0 and aInsertPos < len(self.InfixArray):
            for i in xrange(len(newtokens) - 1, -1, -1):
                self.InfixArray.insert(aInsertPos, newtokens[i])
        else:
        #inserting at the end of the array

            for i in range(0, len(newtokens)):
                self.InfixArray.append(newtokens[i])
        result = aInsertPos + len(newtokens)
        return result

    #     /** function FixBracketClosure
    #      *
    #      * Purpose: To ensure that the token array has the correct number of brackets
    #      * in it - inserting the special ? character to ensure that the student is
    #      * aware that their expression is not legal in its current state
    #      *
    #      * @param infixTokenArray - an array of the infix expression
    #      * @param illegalCharacterColour - the colour to paint ?
    #      *
    #      * @output returns true if a fix has been made, false otherwise
    #      */
    def FixBracketClosure(self, illegalCharacterColour):

        openbrackets = 0
        closedbrackets = 0
        result = True

        for i in range(0, len(self.InfixArray)):
            if (self.InfixArray[i] == ")"):
                closedbrackets = closedbrackets + 1
            elif (self.InfixArray[i] == "("):
                openbrackets = openbrackets + 1

        if openbrackets != closedbrackets:
            if openbrackets > closedbrackets:
                result = False
                self.setSyntaxError(definitions.SyntaxErrorMessages[0] % (openbrackets - closedbrackets) + ' for expression ' + self.ExpressionString)

                # add the brackets to the end with a ? inside them

                # if the last token is a ( then add ")?" else add "*?)""

                if self.InfixArray[-1] == "(":
                    self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour),
                                                len(self.InfixArray), False)

                else:
                    self.InsertTokensFromString("*", len(self.InfixArray));
                    self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour),
                                                len(self.InfixArray))

                for j in range(1, openbrackets - closedbrackets + 1):
                    self.InsertTokensFromString(")", len(self.InfixArray))
            else:
                result = False
                self.setSyntaxError(definitions.SyntaxErrorMessages[1] % (closedbrackets - openbrackets)+ ' for expression ' + self.ExpressionString)

                for j in range(1, closedbrackets - openbrackets + 1):
                    self.InsertTokensFromString("(", 0)

        return result;


    def ScientificNotation(self, aStr):
        result = aStr;

        # scientific notation
        result = re.sub('([0-9]*\.?[0-9]+)[Ee]([0-9]*\.?[0-9]+)', tokenScientificFunctionName + '(\g<1>,\g<2>)', result)

        return result;

    def ImpliedMultiplication(self, aStr):

        result = aStr;


        #result = re.sub('([a-zA-Z]+)([0-9]*\.?[0-9]+)','\g<1>\u2062\g<2>',result) #e.g. x6->x*6
        result = re.sub('([0-9]*\.?[0-9]+)([a-zA-Z]+)', '\g<1> \u2062 \g<2>', result) #e.g. 6x->6*x
        result = re.sub('([0-9]*\.?[0-9]+)(\()', '\g<1> \u2062\ g<2>', result) #e.g. // 6( -> 6*(
        result = re.sub('(\))([0-9]*\.?[0-9]+)', '\g<1> \u2062\ g<2>', result) #e.g. )6( -> )*6

        # replace [,],{,} with ( and )
        # result = str(result).replace('{', '(')
        # result = str(result).replace('}', '}')
        # result = str(result).replace('[', '(')
        # result = str(result).replace(']', ')')

        return result;


    def ColourTokenAsToken(self, tokenArray, index, aColour):
        '''
        
        :param tokenArray: The token array in which to find the token to colour
        :param index: The index of the token to colour
        :param aColour: The colour to use to do the colouring e.g. red
        '''

        tokenArray[index] = self.ColourTokenAsString(tokenArray[index], aColour);

    def ColourTokenAsString(self, tokenstring, aColour):
        return definitions.tokenColouringFunctionName + "(" + tokenstring + ',' + aColour + ")"


    def GetFunctionArgumentsMakeLegalString(self, functionStr, includestartbracket, includeendbracket,
                                            illegalCharacterColour):
        stringtoadd = ""
        numarguments = self.GetFunctionArgCount(functionStr)
        if (includestartbracket):
            stringtoadd = "("

        for j in range(0, numarguments):
            if j == 0:
                stringtoadd = stringtoadd + self.ColourTokenAsString("?", illegalCharacterColour)
            else:
                stringtoadd = stringtoadd + "," + self.ColourTokenAsString("?", illegalCharacterColour)
        if includeendbracket:
            stringtoadd = stringtoadd + ")"
        return stringtoadd;


    def MakeLegal(self, rangeFrom, rangeTo, illegalCharacterColour):
        i = rangeFrom;
        ThisTok = None
        NextTok = None
        PrevTok = None
        ThisTokType = None
        NextTokType = None
        PrevTokType = None

        stringtoadd = ""

        if (len(self.InfixArray) == 0):
            if self.InsertTokensFromString("?", 0):
                self.setSyntaxError('The expression should not be blank')
                return False

        while i <= len(self.InfixArray) - 1:
            ThisTok = self.InfixArray[i];

            if i < len(self.InfixArray) - 1:
                NextTok = self.InfixArray[i + 1]
            else:
                NextTok = None;

            if i > 0:
                PrevTok = self.InfixArray[i - 1]
            else:
                PrevTok = None;

            #Check the type of ThisTok

            ThisTokType = self.TokenType(ThisTok, NextTok);
            PrevTokType = self.TokenType(PrevTok, ThisTok);
            NextTokType = self.TokenType(NextTok, None);

            if ThisTokType == 'VARIABLE':
                if NextTok == "(" and ThisTok != tokenScientificFunctionName and self.RandomGenerator.GetVariableIdxByName(
                        ThisTok) < 0:  # taking care of scientific notation aEb
                    # We actually have a user-defined function - add the functioniser operator

                    self.InsertTokensFromString(definitions.tokenfunctioniser, i + 1, False)
                    return False


            elif ThisTokType == "RELATION":
                if NextTok == None:
                    if self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour), i + 1):
                        self.setSyntaxError(definitions.SyntaxErrorMessages[15] % (ThisTok)+ ' for expression ' + self.ExpressionString)
                        return False


                elif (PrevTok == None):

                    if self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour), i):
                        self.setSyntaxError(definitions.SyntaxErrorMessages[15] % (ThisTok)+ ' for expression ' + self.ExpressionString)
                        return False

            elif ThisTokType == "DELIMITER":
                if (ThisTok == "(" and NextTok == ")"): # () --> (?)
                    if self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour), i + 1):
                        self.setSyntaxError(definitions.SyntaxErrorMessages[3]+ ' for expression ' + self.ExpressionString)
                        return False

                elif (ThisTok == ")" and NextTok == "("): #{ // )( --> )*(}
                    # note that this isn't an error - editor just using implied multiplication
                    if self.InsertTokensFromString("*", i + 1, False):
                        print('inserted an implied multiplicaion between ) and ( on expression ' + self.ExpressionString)
                        return False


                elif ThisTok == ")":
                    # note that this isn't an error - we are just using implied multiplication
                    if NextTokType == "VARIABLE" or NextTokType == "FUNCTION" or NextTokType == "NUMBER" or NextTokType == "SPECIAL":
                        if self.InsertTokensFromString("*", i + 1, False):
                            print('converted )' + NextTok + 'to )*' + NextTok + ' on expression ' + self.ExpressionString)
                            return False



            elif ThisTokType == "FUNCTION":  #// e.g. sin
                if NextTokType == "FUNCTION":
                    stringtoadd = self.GetFunctionArgumentsMakeLegalString(PrevTok, True, True, illegalCharacterColour)
                    numarguments = self.GetFunctionArgCount(PrevTok);
                    if self.InsertTokensFromString(stringtoadd, i):
                        self.setSyntaxError(definitions.SyntaxErrorMessages[4] % (ThisTok, numarguments) + ' for expression ' + self.ExpressionString)
                        return False


                elif NextTokType == "":#fn with no argument
                    stringtoadd = self.GetFunctionArgumentsMakeLegalString(ThisTok, True, True, illegalCharacterColour)
                    numarguments = self.GetFunctionArgCount(ThisTok)
                    if self.InsertTokensFromString(stringtoadd, i + 1):
                        self.setSyntaxError(definitions.SyntaxErrorMessages[4] % (ThisTok, numarguments)+ ' for expression ' + self.ExpressionString)
                        return False

                elif NextTokType == "OPERATOR": # e.g. sin* --> sin(?)*
                    stringtoadd = self.GetFunctionArgumentsMakeLegalString(ThisTok, True, True, illegalCharacterColour)
                    numarguments = self.GetFunctionArgCount(ThisTok)
                    if self.InsertTokensFromString(stringtoadd, i + 1):
                        self.setSyntaxError(definitions.SyntaxErrorMessages[4] % (ThisTok, numarguments)+ ' for expression ' + self.ExpressionString)
                        return False

                elif NextTokType == "NUMBER": # e.g. sin4 --> sin(?)*4
                    stringtoadd = self.GetFunctionArgumentsMakeLegalString(ThisTok, True, True, illegalCharacterColour);
                    numarguments = self.GetFunctionArgCount(ThisTok);
                    if self.InsertTokensFromString(stringtoadd + "*", i + 1):
                        self.setSyntaxError(definitions.SyntaxErrorMessages[4] % (ThisTok, numarguments)+ ' for expression ' + self.ExpressionString)
                        return False

                elif NextTokType == "VARIABLE": # e.g. sinx --> sin(?)*x
                    stringtoadd = self.GetFunctionArgumentsMakeLegalString(ThisTok, True, True, illegalCharacterColour);
                    numarguments = self.GetFunctionArgCount(ThisTok);
                    if self.InsertTokensFromString(stringtoadd + "*", i + 1):
                        self.setSyntaxError(definitions.SyntaxErrorMessages[4] % (ThisTok, numarguments)+ ' for expression ' + self.ExpressionString)
                        return False

                elif NextTokType == "RELATION": #e.g. sin= --> sin(?)=
                    stringtoadd = self.GetFunctionArgumentsMakeLegalString(ThisTok, True, True, illegalCharacterColour);
                    numarguments = self.GetFunctionArgCount(ThisTok);
                    if self.InsertTokensFromString(stringtoadd + "*", i + 1):
                        self.setSyntaxError(definitions.SyntaxErrorMessages[4] % (ThisTok, numarguments)+ ' for expression ' + self.ExpressionString)
                        return False



                elif NextTokType == "DELIMITER":
                    if (NextTok == ")"):# sin) --> sin(?):
                        stringtoadd = self.GetFunctionArgumentsMakeLegalString(ThisTok, True, False,
                                                                               illegalCharacterColour);
                        numarguments = self.GetFunctionArgCount(ThisTok);
                        if self.InsertTokensFromString(stringtoadd, i + 1, False):
                            self.setSyntaxError(definitions.SyntaxErrorMessages[4] % (ThisTok, numarguments)+ ' for expression ' + self.ExpressionString)
                            return False



            elif ThisTokType == "OPERATOR": # This is an operator
                if PrevTokType == "":
                    if ThisTok == '/':
                        if self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour), i):
                            self.setSyntaxError(definitions.SyntaxErrorMessages[5]+ ' for expression ' + self.ExpressionString)
                            return False

                    elif ThisTok in ["*", definitions.INVISIBLE_TIMES]:
                        if self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour), i):
                            self.setSyntaxError(definitions.SyntaxErrorMessages[6]+ ' for expression ' + self.ExpressionString)
                            return False

                    elif ThisTok == "^": # e.g. ++ --> +?+
                        if self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour), i):
                            self.setSyntaxError(definitions.SyntaxErrorMessages[7]+ ' for expression ' + self.ExpressionString)
                            return False

                    elif ThisTok == "-":
                        # check to see if the next token is also blank - in which case it's only a -
                        if NextTok == None:
                            self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour), i)
                            self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour),
                                                        len(self.InfixArray))
                            self.setSyntaxError(definitions.SyntaxErrorMessages[8]+ ' for expression ' + self.ExpressionString)
                            return False

                if NextTokType == "":
                    if ThisTok == "/": # / into /?

                        if self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour), i + 1):
                            self.setSyntaxError(definitions.SyntaxErrorMessages[9]+ ' for expression ' + self.ExpressionString)
                            return False

                    elif ThisTok == "^": # ^ into ^?

                        if self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour), i + 1):
                            self.setSyntaxError(definitions.SyntaxErrorMessages[10]+ ' for expression ' + self.ExpressionString)
                            return False

                    elif ThisTok in ['-', '%']: # - into -?

                        if self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour), i + 1):
                            self.setSyntaxError(definitions.SyntaxErrorMessages[11]+ ' for expression ' + self.ExpressionString)
                            return False

                    elif ThisTok in ['*', '\u2062']:
                        if self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour), i + 1):
                            self.setSyntaxError(definitions.SyntaxErrorMessages[12]+ ' for expression ' + self.ExpressionString)
                            return False

                    elif ThisTok == "+": # + into +?
                        if self.InsertTokensFromString(self.ColourTokenAsString("?", illegalCharacterColour), i + 1):
                            self.setSyntaxError(definitions.SyntaxErrorMessages[13]+ ' for expression ' + self.ExpressionString)
                            return False

                            #                 elif NextTokType == "OPERATOR":
                            #                     if NextTok in ['-']:
                            #                         if self.InsertTokensFromString(self.ColourTokenAsString('?',illegalCharacterColour), i+1):
                            #                             self.setSyntaxError(definitions.SyntaxErrorMessages[14]%(ThisTok))
                            #                             return False


                elif NextTokType == "DELIMITER":
                    if NextTok == ")":
                        if self.InsertTokensFromString(self.ColourTokenAsString('?', illegalCharacterColour), i + 1):
                            self.setSyntaxError(definitions.SyntaxErrorMessages[14] % (ThisTok)+ ' for expression ' + self.ExpressionString)
                            return False

            i = i + 1
        return self.FixBracketClosure(illegalCharacterColour)



class EvalExpression(Expression):
    def __init__(self, ExpressionString, MakeLegal, aRandomGenerator):
        Expression.__init__(self, ExpressionString, MakeLegal, aRandomGenerator)

        self.variables = []


    def UpdateVariables(self):
        del self.variables[:]
        for i in range(0, len(self.PostfixArray)):
            if self.TokenType(self.PostfixArray[i], None) == "VARIABLE":
                try:
                    self.variables.index(self.PostfixArray[i])
                except:
                    # only add if it isn't already there
                    self.variables.append(self.PostfixArray[i])


    def Evaluate(self):
        '''Evaluates a postfix array '''
        parrExp = self.PostfixArray
        if parrExp == None:
            raise Exception("Invalid postfix expression!")

        if len(parrExp) == 0:
            raise Exception("postfix array does not contain any characters")

        intIndex = 0
        myStack = []
        precedenceStack = []

        while intIndex < len(parrExp):
            strTok = parrExp[intIndex]
            ThisTokType = self.TokenType(strTok)
            #             switch (TokenType(strTok.toString()))
            #             {
            if ThisTokType == "OPERATOR":

                if strTok == definitions.UNARY_NEG or strTok == definitions.UNARY_PM or strTok == definitions.UNARY_MP:
                    if len(myStack) == 0:
                        raise Exception("No operand to negate!")

                    objOp1 = None
                    objOp1Precedence = None
                    objOp2 = None
                    objOp2Precedence = None

                    objOp1 = myStack.pop()
                    objOp1Precedence = precedenceStack.pop()

                    myStack.append(-objOp1)
                    #
                    precedenceStack.append(self.Precedence(objOp1Precedence))


                else:
                    if (len(myStack) == 0 or len(myStack) < 2):
                        raise Exception("Stack is empty, can not perform [" + strTok + "] on expression " + self.ExpressionString)

                    objOp1 = None
                    objOp2 = None
                    objOp1Precedence = None;
                    objOp2Precedence = None

                    objOp2 = myStack.pop();
                    objOp1 = myStack.pop();
                    objOp2Precedence = precedenceStack.pop();
                    objOp1Precedence = precedenceStack.pop();
                    ThisPrecedence = self.Precedence(strTok);

                    if (strTok == "^"):
                        myStack.append(objOp1 ** objOp2)
                        precedenceStack.append(ThisPrecedence)
                    elif (strTok == "/"):
                        myStack.append( self.convertStringToNumber( objOp1 / objOp2))
                        precedenceStack.append(ThisPrecedence)

                    elif (strTok == "+"):
                        myStack.append(objOp1 + objOp2)
                        precedenceStack.append(ThisPrecedence)

                    elif (strTok == "-"):
                        myStack.append(objOp1 - objOp2)
                        precedenceStack.append(ThisPrecedence)
                    elif (strTok in ["*","\\times"]):
                        myStack.append(objOp1 * objOp2)
                        precedenceStack.append(ThisPrecedence)

                    else:
                        precedenceStack.append(ThisPrecedence)
                        raise Exception('You cannot use the operation ' + strTok + ' inside an "eval" function.  You have done on expression ' + self.ExpressionString)


            elif ThisTokType == "FUNCTION":
                self.HandleFunctions_Evaluate(strTok, myStack, precedenceStack, definitions.dtFormat, None)

            elif ThisTokType == "NUMBER":
                myStack.append(self.convertStringToNumber(strTok))
                # Consider what happens if the answer is not a float but integer, etc.
                ThisPrecedence = self.Precedence(strTok)
                precedenceStack.append(ThisPrecedence)

            elif ThisTokType == "RELATION":
                if (len(myStack) == 0 or len(myStack) < 2):
                    raise Exception("Stack is empty, can not perform [" + strTok + "] on expression " + self.ExpressionString )

                LHS = None
                RHS = None
                #                     LHSPrecedence = None
                #                     RHSPrecedence = None

                RHS = myStack.pop()
                LHS = myStack.pop()
                #                     RHSPrecedence = precedenceStack.Pop()
                #                     LHSPrecedence = precedenceStack.Pop()
                ThisPrecedence = self.Precedence(strTok)
                precedenceStack.append(ThisPrecedence)

                if strTok == '<=':
                    myStack.append(LHS <= RHS)
                elif strTok == '>=':
                    myStack.append(LHS >= RHS)
                elif strTok == '<>':
                    myStack.append(LHS != RHS)
                elif strTok in ['==', '=']:
                    myStack.append(LHS == RHS)
                elif strTok in ['<']:
                    myStack.append(LHS < RHS)
                elif strTok in ['>']:
                    myStack.append(LHS > RHS)
                elif strTok in ['<>']:
                    myStack.append(LHS <> RHS)
                else:
                    raise Exception('Unable to evaluate relation ' + strTok)




            elif ThisTokType == "VARIABLE":
                '''we have to use the variable's value'''
                #// check for greek Letters
                if strTok == "FUDGE":
                    myStack.append(0)
                else:
                    if self.RandomGenerator == None:
                        myStack.append(strTok)
                    else:
                        myStack.append(self.RandomGenerator.GetValueByName(strTok))

                ThisPrecedence = self.Precedence(strTok)
                precedenceStack.append(ThisPrecedence)
            elif ThisTokType == "STRING":
                myStack.append(strTok[1:len(strTok) - 1])
                precedenceStack.append(self.Precedence(strTok))


            elif ThisTokType == "TERMINAL":
                myStack.append(strTok)
                precedenceStack.append(self.Precedence(strTok))

            elif ThisTokType == "SPECIAL":

                if ( strTok.upper() == "PI" ):
                    myStack.append(math.pi)
                    precedenceStack.append(0)

                elif ( strTok == "FUDGE" ):
                    myStack.push(0)
                    precedenceStack.push(0) #// remove the FUDGE for unary minuses
            else:

                #// Handle functions and operands
                if self.IsNumber(strTok) or self.IsBoolean(strTok) or self.TokenType(
                        strTok) == "FLOAT" or self.TokenType(strTok) == 'INT' or self.TokenType(
                        strTok) == "BOOLEAN" or self.TokenType(strTok) == 'OBJECT' or self.TokenType(
                        strTok) == 'VARIABLE':
                    myStack.append(strTok)

                    ThisPrecedence = self.Precedence(strTok)
                    precedenceStack.append(ThisPrecedence)

            intIndex = intIndex + 1

        if (len(myStack) == 0 or len(myStack) > 1):
            raise Exception("Unable to evaluate expression " + str(self.ExpressionString))
        else:
            result = myStack.pop()
            precedenceStack.pop()

        return result


    def InsertRandoms(self):
        'Inserts randoms into the array'
        for i in range(0, len(self.PostfixArray)):
            if self.TokenType(self.PostfixArray[i]) == 'VARIABLE':
                'Look up the variable in the self.RandomGenerator - if we find it then replace it with its value'
                if self.RandomGenerator.GetVariableByName(self.PostfixArray[i]).EvaluatedAll:
                    self.PostfixArray[i] = self.RandomGenerator.GetValueByName(self.PostfixArray[i])
                else:
                    raise Exception('Call to InsertRandoms with unevaluated variable ' + self.PostfixArray[i])


if __name__ == '__main__':
    #testcases=['eval(3+4)','3+4','5+eval(6+7)','2^(4-3)','eval(2^(4-3))','random(range(1,1,1))', 'eval(-1)','6E7','6x','x6']
    #testcases = ['-sin(x)']
    testcases = ['a \\given b']
    for i in range(0, len(testcases)):
        myexpression = EvalExpression(testcases[i], True, Randoms.RandomGenerator())
        #expressionvalue = myexpression.Evaluate()
        print('Test case ' + str(i) + ' [' + testcases[i] + '] :')
        #print('evaluated : ' + str(expressionvalue) )
        print('LaTeX : ' + myexpression.GetLateXMathExpression())
        if myexpression.syntaxError != '':
            print('Syntax Error ' + myexpression.syntaxError)

#     myexpression = Expression('1.234',False)
#     myexpression = Expression('1.234*234-x',False)  
#     myexpression = Expression('1E4-x',False)  
#     myexpression = Expression('sin((x+y)/(z+h))',False)
    
     
    
    
    
