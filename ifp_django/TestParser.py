'''
Created on Jul 29, 2013

@author: david_g_wild
'''
import xml.etree.ElementTree  as etree
import os
from tempfile import mkdtemp, mkstemp
import ntpath
import subprocess
import datetime
import Intelligent_Exam_Paper_Generator.settings


from QuestionParser import IQQuestion
import definitions
#from memprof import *


class IQTest:
    def __init__(self, HeaderText, FooterText, QuestionTemplateText, graphicsfolder, printheader=True,
                 printfooter=True):
        self.QuestionList = []
        if printheader:
            self.LatexOutput = HeaderText
        else:
            self.LatexOutput = ''


        # tree = etree.XML(QuestionTemplateText)

        ExamPaperNode = etree.fromstring(QuestionTemplateText)

        # get all the <question> tags and process them appropriately
        for QuestionNode in ExamPaperNode.findall('question'):
            self.QuestionList.append(IQQuestion(QuestionNode, graphicsfolder))

        self.LatexOutput = self.LatexOutput + "\\setcounter{page}{1}\\begin{enumerate}[1]"
        for i in range(0, len(self.QuestionList)):
            self.LatexOutput = self.LatexOutput + '\\item ' + self.QuestionList[i].questionTexts[0]

        self.LatexOutput = self.LatexOutput + '\\end{enumerate}'

        self.LatexOutput = self.LatexOutput + '\\cleartoleftpage\\setcounter{page}{1}\n\n\\section*{Solutions}\\begin{enumerate}[1]'

        for i in range(0, len(self.QuestionList)):

            if len(self.QuestionList[i].questionSolutions) > 0:
                self.LatexOutput = self.LatexOutput + '\\item ' + self.QuestionList[i].questionSolutions[0]
        self.LatexOutput = self.LatexOutput + '\\end{enumerate}'

        if printfooter:
            self.LatexOutput = self.LatexOutput + FooterText


class TestGenerator:
    def __init__(self, output_destination_folder, TestTemplateXMLString, gfxFolderName='gfx'):
        self.output_destination_folder = output_destination_folder
        self.TestTemplateXMLString = TestTemplateXMLString
        self.gfxFolderName = gfxFolderName
        self.AdditionalGraphics = []
        self.GeneratedPDF_URL = ''
        self.Error = ''
        self.testdate = datetime.datetime.now
        self.logofile = None
        self.licencename = 'Intelligent Exam Papers Ltd'
        self.rubric = None

    def copyfile(self, source, dest, buffer_size=1024 * 1024):
        """
        Copy a file from source to dest. source and dest
        can either be strings or any object with a read or
        write method, like StringIO for example.
        """
        if not hasattr(source, 'read'):
            source = open(source, 'rb')
        if not hasattr(dest, 'write'):
            dest = open(dest, 'wb')

        while 1:
            copy_buffer = source.read(buffer_size)
            if copy_buffer:
                dest.write(copy_buffer)
            else:
                break

        source.close()
        dest.close()

    def AddAdditionalGraphicFile(self, aFile):
        print('Adding additional file : ' + aFile)
        self.AdditionalGraphics.append(aFile)

    def SetLogoFile(self, alogofile):
        self.logofile = alogofile

    def SetRubric(self, arubric):
        self.rubric = arubric

    def SetLicenceName(self, alicenceName):
        self.licencename = alicenceName

    def SetTestDate(self, atestdate):
        self.testdate = atestdate

    #@memprof(plot=True)
    def GenerateTest(self, NumCopies=1):
        # In a temporary folder, make a temporary file
        result = True

        #try:
        tmp_folder = mkdtemp()
        print('created temp folder ' + tmp_folder)

        os.chdir(tmp_folder)

        os.mkdir(self.gfxFolderName)

        texfile, texfilename = mkstemp(dir=tmp_folder)

        for i in range(0, len(self.AdditionalGraphics)):
            source = self.AdditionalGraphics[i]
            dest = tmp_folder + '/' + self.gfxFolderName + '/' + ntpath.basename(source)
            self.copyfile(source, dest)

        astart = 0
        aend = NumCopies
        arange = range(astart, aend)
        TotalOutput = ''
        absolutelynopagebreak = r'\usepackage{lipsum}' \
                                r'\newenvironment{absolutelynopagebreak}' \
                                r'{\par\nobreak\vfill\penalty0\vfilneg' \
                                r'\vtop\bgroup}' \
                                r'{\par\xdef\tpd{\the\prevdepth}\egroup' \
                                r'\prevdepth=\tpd}'
        IQTestHeaderText = "\n\
                                \\documentclass[12pt]{paper}\n\
                                \\usepackage{enumerate}\n\
                                \\usepackage[margin=1in]{geometry}\n\
                                \\usepackage{amssymb}\n\
                                \\usepackage{eurosym}\n\
                                \\usepackage{amsmath}\n\
                                \\usepackage{graphicx}\n\
                                \\usepackage{color}\n\
                                \\usepackage{fancyhdr} \n\
                                \\pagestyle{fancy}" + absolutelynopagebreak + " \n\
                                \\renewcommand{\\headrulewidth}{0.4pt}\n\
                                \\renewcommand{\\footrulewidth}{0.4pt}\n\
                                \\def\\dashfill{\\cleaders\\hbox to 1em{-}\\hfill} \n\
                                \\newcommand*\\cleartoleftpage{% \n\
                                \\clearpage \n\
                                \\ifodd\\value{page}\hbox{}\\newpage \\fi } \n\
                                \\begin{document}"


        if self.logofile != None:
            IQTestHeaderText = IQTestHeaderText + "\n\
                                \\begin{center}\\includegraphics[scale=1.0]{gfx/%s}\\end{center}\n\
                                \\begin{center}\\textbf{Date %s} \\end{center} \n\
                                \n\
                                " % (self.logofile, self.testdate)
        if self.rubric != None:
            IQTestHeaderText = IQTestHeaderText + self.rubric + "\n\
                                \\newpage"

        IQFooterText = '\\ \\  Produced by Intelligent Exam Papers \\end{document}'
        for i in arange:
            print('Generating Test paper number : ' + str(i + 1) + '/' + str(aend))

            myIQTest = IQTest(IQTestHeaderText, IQFooterText, self.TestTemplateXMLString,
                              tmp_folder + '/' + self.gfxFolderName, i == astart, i == aend - 1)
            TotalOutput = TotalOutput + myIQTest.LatexOutput
            if i < aend - 1:
                TotalOutput = TotalOutput + '\n\n\\newpage\n\n'

            print('Latex output is ' + TotalOutput)
                #             pyperclip.setcb(TotalOutput)
                #             print('LaTeX has been copied to the clipboard')

        os.write(texfile, TotalOutput.encode('utf-8'))
        os.close(texfile)
        # Compile the TeX file with PDFLaTeX
        print('about to call the pdflatex command with texfilename='+texfilename)
        print('========================================')
        # Webfaction command.  Enable below and remove cmd following.
        if Intelligent_Exam_Paper_Generator.settings.IS_WEBFACTION:
            print('About to set CMD for webfaction')
            cmd = ["/home/davidgwild/texlive/bin/x86_64-linux/pdflatex", '-interaction=nonstopmode', texfilename]
        else:
            print('About to set CMD for local development')
            cmd = ["/usr/local/texlive/2012/bin/x86_64-darwin/pdflatex", '-interaction=nonstopmode', texfilename]
        print('About to open the subprocess')
        p = subprocess.Popen(cmd, shell=False).communicate()



        #             # Double compilation because of table of content and indexes
        #             p = Popen(cmd, stdout=PIPE, cwd=tmp_folder)
        #             p.wait()

        print('completed pdflatex')

        # Move resulting PDF to a more permanent location
        UniqueFilename = definitions.unique_filename()
        print('UniqueFilename=' + UniqueFilename)
        outputfilename = self.output_destination_folder + UniqueFilename
        print('outputfilename='+outputfilename)

        #             cmd = "cp " + texfilename + ".pdf " + outputfilename + ".pdf" #
        #             print('executing command :' + str(cmd))
        #             subprocess.call( str(cmd) ,shell=False)

        #         cmd = ['cp', texfilename, '.pdf /Applications/MAMP/htdocs/IFP_static/' + UniqueFilename  + '.pdf']
        #         print(' about to copy files with cmd : ' + str(cmd))
        #         p = subprocess.check_call( cmd, shell=False)
        self.copyfile(texfilename + '.pdf', outputfilename + '.pdf')

        self.GeneratedPDF_URL = UniqueFilename + '.pdf'
        print('GeneratedPDF_URL is : ' + self.GeneratedPDF_URL)

        print('about to remove temporary files')
        os.remove(texfilename)
        os.remove(texfilename + '.aux')
        os.remove(texfilename + '.log')
        os.chdir(tmp_folder + '/' + self.gfxFolderName)
        filelist = [f for f in os.listdir(".")]
        for f in filelist:
            os.remove(f)
        os.chdir(tmp_folder)
        os.rmdir(tmp_folder + '/gfx')
        os.remove(texfilename + '.pdf')
        os.rmdir(tmp_folder)

        return True
        # except:
        # return False


if __name__ == '__main__':
    f = open("testpaper.xml", "r")

    #Read whole file into data
    data = f.read()

    gen = TestGenerator('/Applications/MAMP/htdocs/IFP_static/', data, 'gfx')
    gen.AddAdditionalGraphicFile('/Users/david_g_wild/Documents/Intelligent Qualifications/gfx/q5.png')
    gen.AddAdditionalGraphicFile('/Users/david_g_wild/Documents/Intelligent Qualifications/gfx/top.jpg')
    if gen.GenerateTest(1):
        print('Successfully file :' + gen.GeneratedPDF_URL)
    print('Generated file : ' + gen.GeneratedPDF_URL)

    # Close the file
    f.close()
