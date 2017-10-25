'''
Created on Jun 13, 2013

Contains global constant definitions

@author: david_g_wild
'''

import uuid
import base64
import unicodedata
import xml.etree.ElementTree  as etree

tokenColouringFunctionName = "COLOURTOKEN"
tokenStringifyFunctionName = 'STRINGIFY'
tokenScientificFunctionName = 'SCIENTFIC'

#// used to make userfunction(argument) appear properly
tokenfunctioniser ="\\functioniser"
tokenEvaluate = 'EVAL'
tokenRandomiser = 'RANDOM'
tokenRandomRange = 'RANGE'
tokenRandomString = 'RANDOMSTR'
tokenRandomMatch = 'MATCH'

listAlpha    = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","_","?"]
listDigits   = ["0","1","2","3","4","5","6","7","8","9"]
# listArithOps = [tokenfunctioniser,"^","*","/","+","-","\u2062","%","\\pm","\\pm_unary","\\mp_unary","\\mp","\\times","\\ast","\\star","\\circ","\\bullet","" 
#                     ,"\\diamond","\\cap","\\intersect","\\cup","\\union","\\uplus","\\sqcap",""
#                     ,"\\sqcup","\\vee","\\wedge","\\setminus","\\wr","\\bigtriangleup","\\bigtriangledown",""
#                     ,"\\triangleleft","\\triangleright","\\lhd","\\rhd","\\unlhd","\\unrhd","\\oplus","\\ominus"
#                     ,"\\otimes","\\oslash","\\odot","\\bigcirc","\\dagger","\\ddagger","\\amalg","\\mod","\\dotprod"
#                     ,"\\crossprod"]


listLeftAssociatedOps = [tokenfunctioniser,"*","/","+","-","\u2062","\\pm","\\mp","\\times","\\ast","\\star","\\circ","\\bullet","" 
                    ,"\\diamond","\\cap","\\intersect","\\cup","\\union","\\uplus","\\sqcap",""
                    ,"\\sqcup","\\vee","\\wedge","\\setminus","\\wr","\\bigtriangleup","\\bigtriangledown",""
                    ,"\\triangleleft","\\triangleright","\\lhd","\\rhd","\\unlhd","\\unrhd","\\oplus","\\ominus"
                    ,"\\otimes","\\oslash","\\odot","\\bigcirc","\\dagger","\\ddagger","\\amalg","\\mod","\\dotprod"
                    ,"\\crossprod","\\invisibletimes","\\div"]
listRightAssociatedOps = ["^"]
listUnaryOps = ["%","\\pm_unary","\\mp_unary","\\mp","\\pm","-"]
listArithOps = list(set(listLeftAssociatedOps + listRightAssociatedOps + listUnaryOps))

listLogicOps = ["!,&,|"]
listCompaOps = ["=","<>",">","<","<=",">=","==","==>","<==","<==>","\\tends","\\prec","\\preceq",""
                    ,"\\subset","\\subseteq","\\notsubset","\\notsubseteq","\\sqsubset",""
                    ,"\\sqsubseteq","\\in","\\notin","\\vdash","\\succ","\\succeq","\\ll",""
                    ,"<<",">>","\\supset","\\ni","\\dashv","\\sim","\\simeq","\\asymp","\\approx",""
                    ,"\\cong","\\doteq","\\propto","\\models","\\perp","\\mid","\\parallel",""
                    ,"\\bowtie","\\join","\\smile","\\frown"]
                
listFuncOps  = ["ARCCOSECH","ABS","ARCCOS","ARCSIN","ARCTAN","ARCSINH","ARCCOSH",
                    "COS","LOG","SIN","SQRT","TAN","SQR","LN","LOG","LOGBASE","COSEC","SEC","COT","SINH",
                    "COSH","COSECH","SECH","COTH","TANH","EXP","PDIFF", "DIFF", "INT", 
                    "DIFFPRIME", "DEFINT","LOWINT","CIRCLOWINT","CIRCINT","CIRCDEFINT",
                    "LIMIT", "SUM","DEFSUM","LOWSUM", "FACTORIAL",tokenColouringFunctionName,"POINT","VECTOR",
                    "ROWVECTOR","MATRIX","DET","SET",tokenStringifyFunctionName,"PERM", "COMB", "CONJUGATE",tokenScientificFunctionName,
                    tokenEvaluate,tokenRandomiser,tokenRandomRange,tokenRandomString,tokenRandomMatch,"BOLD","FRACTION",
                    "HCF","SURD","PICTURE","ROUND","INVERSE",'ANSWERLINES','BRACKET','LIST','LATEX','ACC','NROOT','DP',
                    'COEFF','MAX','MIN','SUB','SUP', 'SUBSCRIPT','SUPERSCRIPT','OVERLINE','OVERDOT']
                    
listSeparators = [";",","]
special_cases = ["PI"]

listGreekLetters = ["alpha","beta","gamma","delta","epsilon","varepsilon","zeta","eta","theta",
                        "vartheta","kappa","lambda","mu","nu","xi","pi","varpi","rho","varrho",
                        "sigma","varsigma","tau","upsilon","phi","varphi","chi","psi","omega",
                        "Gamma","Delta","Theta","Lambda","Xi","Pi","Sigma","Upsilon","Phi","Psi","Omega"] 
       
       
# provides a list of the token types available 
TOKTYPES = ["blank", "relation","unknown", "function","operator", "delimiter", "variable", "number","special","string" ]

UNARY_NEG    = "%"
UNARY_PM     = "\\pm_unary"
UNARY_MP     = "\\mp_unary"
ARG_TERMINAL = "\\phantom{}"
LESS_THAN    = "<"
GREATER_THAN = ">"
NOT_EQUAL    = "<>"
INVISIBLE_TIMES = "\u2062"
DEBUG_ON     = False
NUMARIC_OP   = "*,/,%,^,"+INVISIBLE_TIMES
dtFormat = 'yyyymmdd'

SyntaxErrorMessages = ["Error 0: Missing %d closed bracket(s)",
                       'Error 1: Missing %d open bracket(s)',
                       "Error 2: String contains a character that is not supported in answers (%s)",
                       'Error 3: Missing expression inside brackets ()',
                       'Error 4: The function %s requires its %d argument(s) in brackets',
                       'Error 5: A fraction is missing a numerator',
                       'Error 6: A multiplication needs a left-hand operand',
                       "Error 7: The power operator needs a base",
                       "Error 8: A minus is requiring a left operand",
                       "Error 9: A divide is missing a denominator",
                       "Error 10: A power operator is missing a power",
                       "Error 11: A minus is missing an operand",
                       "Error 12: A multiplication is missing an operand",
                       "Error 13: A plus is missing an operand",
                       "Error 14: The operator %s is missing an operand",
                       "Error 15: The relation %s requires a left and right hand side"]

def unique_filename(prefix=None, suffix=None):
    fn = []
    if prefix: fn.extend([prefix, '-'])
    fn.append(str(uuid.uuid4()))
    if suffix: fn.extend(['.', suffix.lstrip('.')])
    result = ''.join(fn)
    return result.replace('-','')


def XMLfromRandoms(randomstext):
    textlines = randomstext.split('\n')
    output = ''
    root = etree.Element('randoms')

    for i in range(0,len(textlines)):
        if textlines[i]<>'':
            splitline = textlines[i].split('=',1)
            randomnode = etree.SubElement(root,"random")
            randomnode.set("name", splitline[0])
            randomnode.set("issystem", "false")
            randomnode.set("expression", splitline[1])

            output = output + etree.tostring(randomnode)
    return output
