'''
Created on Aug 13, 2013

@author: david_g_wild
'''
from locale import str


from django.contrib import admin

from django.contrib.admin import helpers
from django.template.response import TemplateResponse
from datetime import datetime

from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin

from Intelligent_Exam_Paper_Generator import settings
from models import Test, Image, Board, Qualification, Unit, Subject, PDF_link,Rubric,Question, Question_Group

from models import NumberEntryPart, NumberEntryPartAnswer, AlgebraPart, AlgebraAnswer
from models import MultipleChoiceChoice, MultipleChoicePart
from models import Author, Book
from TestParser import TestGenerator
from definitions import unique_filename
from mptt.admin import MPTTModelAdmin
from nested_inlines.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline




import definitions






def make_complete(modeladmin, request, queryset):
    queryset.update(DevStatus=3)

class RubricAdmin(ImportExportModelAdmin):
    list_display = ('name', 'text', 'description')
    search_fields = ('name', 'text', 'description')
    list_filter = ('name',)
    pass

admin.site.register(Rubric,RubricAdmin)

class FilterPDFAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def queryset(self, request):
        qs = admin.ModelAdmin.queryset(self, request)
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            # the changelist itself
            return True
        return obj.user == request.user

    list_display = ('name', 'createddate')
    search_fields = ('user_first_name', 'user_last_name', 'createddate')
    list_filter = ('createddate',)
    ordering = ('-createddate',)
    #readonly_fields=('name','user','createddate',)

class RubricAdmin(ImportExportModelAdmin):
    pass

class ImageAdmin(ImportExportModelAdmin):
    pass

class BoardAdmin(ImportExportModelAdmin):
    pass

class QualificationAdmin(ImportExportModelAdmin):
    pass

class SubjectAdmin(ImportExportModelAdmin):
    pass

class UnitAdmin(ImportExportModelAdmin):
    pass


class CustomUserAdmin(UserAdmin):
    filter_horizontal = ('user_permissions', 'groups')
    save_on_top = True
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')

class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('Name', 'Head_of_Department')
    search_fields = ('Name', )



class AssignmentAdmin(ImportExportModelAdmin):
    list_display = ('Name', 'Teacher' )
    search_fields = ('Name',  )
    list_filter = ('Name', )



class TeacherAdmin(ImportExportModelAdmin):
    list_display = ('user', )
    search_fields = ('user', )
    list_filter = ('user',)


class QuestionGroupAdmin(MPTTModelAdmin):
    filter_horizontal = ['Questions']


admin.site.register(Question_Group, QuestionGroupAdmin)














class MyPDFAdmin(FilterPDFAdmin):
    pass   # (replace this with anything else you need)


admin.site.register(PDF_link, MyPDFAdmin)



class QuestionAdmin(ImportExportModelAdmin):


    def Test_Out_Question(modeladmin, request, queryset):

        testxml = '<exampaper>'
        # create a test
        gen = TestGenerator(settings.PDFLOCATION, '', 'gfx')
        for question in queryset:



            # Generate the textXML from each of the questions and construct the xml for the test
            if question.questions_can_span_pages:
                qcsp = "questionscanspanpages = 'yes'"
            else:
                qcsp = "questionscanspanpages = 'no'"

            if question.solutions_can_span_pages:
                scsp = "solutionscanspanpages = 'yes'"
            else:
                scsp = "solutionscanspanpages = 'no'"



            # Get the list of questions
            testxml = testxml + '<question ' + qcsp + ' ' + scsp + '>' \
                                    '   <questiontext>' \
                                        '       <![CDATA[' +\
                                                    question.question_text.encode('utf-8') + \
                                                ']]>' +\
                                        '</questiontext>' + \
                                    '   <solution>' \
                                    '       <![CDATA[' +\
                                                question.solution_text.encode('utf-8') + \
                                            ']]>' \
                                        '</solution>' + \
                                        '<randoms>' +\
                                                 definitions.XMLfromRandoms(question.randoms_text.encode('utf-8')) + \
                                        '</randoms>' + \
                                        '<pictures>' + question.pictures_text.encode('utf-8') + '</pictures>' +\
                                    '</question>'

            # Add all of the question images that are required for the test
            staticimages = question.questionStaticImages.all()
            for animage in staticimages:
                #print('image url = ' + settings.MEDIA_ROOT +  str(animage.image.name).replace('./',''))
                gen.AddAdditionalGraphicFile(settings.MEDIA_ROOT + animage.image.name.replace('./',''))

        testxml = testxml + '</exampaper>'




        # update the test xml on the generator
        gen.TestTemplateXMLString = testxml

        gen.SetLicenceName(request.user)

        gen.SetTestDate(datetime.now())

        genresult = gen.GenerateTest(1)
        if genresult:


            afilename = settings.PDFURL + gen.GeneratedPDF_URL
            #print(str(afilename))
            newPDF = PDF_link.create(afilename, unique_filename('testquestion',''), request.user)
            #newPDF.save()
            #print('created a new PDF : ' + str(newPDF))

            context = {
                'title': "Here's the link to test your question",
                'queryset' : queryset,
                'pdfurl' : afilename,
            }
            return TemplateResponse( request, 'link_to_pdf.html',
                                     context, current_app=modeladmin.admin_site)


        else:
            context = {
                'title': ("Unable to generate test"),
                'queryset': queryset,
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
            }
            return TemplateResponse(request, 'cannot_generate_test.html',
                                    context, current_app=modeladmin.admin_site)


    actions = [Test_Out_Question]
    list_display = ('question_name', 'question_text', 'createddate','modified_date',)

    search_fields = ('question_name', 'question_text', 'solution_text', 'tags__slug','randoms_text')
    list_filter = ('tags','createddate','modified_date',)
    ordering = ('-modified_date',)
    filter_horizontal = ['questionStaticImages']
    pass




class TestAdmin(ImportExportModelAdmin):

    # Action to request  randomised PDF


    def download_pdf(modeladmin, request, queryset):

        if request.POST.get('quantity'):
            #print('Inside download_Pdf')
            for test in queryset:


                numberoftests = request.POST['quantity']
                #print('Requested : ' + str(numberoftests) + ' tests to be printed')

                # create a test
                gen = TestGenerator(settings.PDFLOCATION, test.testXML, 'gfx')

                # Generate the textXML from each of the questions and construct the xml for the test

                # Get the list of questions
                testxml = '<exampaper>'
                for questiongroup in test.QuestionGroup.get_descendants(True):
                    for question in questiongroup.Questions.all().order_by('question_name'):
                        #print('Found question text :' + question.question_text)
                        #print('Found question solution :' + question.solution_text)
                        #print('Found question randoms : ' + question.randoms_text)

                        if question.questions_can_span_pages:
                            qcsp = "questionscanspanpages='yes'"
                        else:
                            qcsp = "questionscanspanpages='no'"

                        if question.solutions_can_span_pages:
                            scsp = "solutionscanspanpages='yes'"
                        else:
                            scsp = "solutionscanspanpages='no'"

                        testxml = testxml + '<question ' + qcsp + ' ' + scsp + '>' \
                                            '   <questiontext>' \
                                                '       <![CDATA[' +\
                                                            question.question_text.encode('utf-8') + \
                                                        ']]>' +\
                                                '</questiontext>' + \
                                            '   <solution>' \
                                            '       <![CDATA[' +\
                                                        question.solution_text.encode('utf-8') + \
                                                    ']]>' \
                                                '</solution>' + \
                                                '<randoms>' +\
                                                        definitions.XMLfromRandoms(question.randoms_text.encode('utf-8')) + \
                                                '</randoms>' + \
                                                '<pictures>' + question.pictures_text.encode('utf-8') + '</pictures>' +\
                                            '</question>'

                        # Add all of the question images that are required for the test
                        staticimages = question.questionStaticImages.all()
                        for animage in staticimages:
                            #print('image url = ' + settings.MEDIA_ROOT +  str(animage.image.name).replace('./',''))
                            gen.AddAdditionalGraphicFile(settings.MEDIA_ROOT + animage.image.name.replace('./',''))

                testxml = testxml + '</exampaper>'

                # update the test xml on the generator
                #print('This is the final test XML : ' + testxml)
                gen.TestTemplateXMLString = testxml
                #print('Test XML looks like this:' + testxml )
                # Make sure we include the logo of the board in question
                #print('test.board.logo='+str(test.board.logo.image.name))
                logofile = settings.MEDIA_ROOT +  test.board.logo.image.name.replace('./','')
                #print('Logofile = ' + str(logofile))
                logofileforlatex = test.board.logo.image.name.replace('./','')


                gen.AddAdditionalGraphicFile(logofile)

                gen.logofile = logofileforlatex
                gen.SetLicenceName(request.user)
                rubrics = test.rubric.all()
                rubricString = ''
                for rubric in rubrics:
                    rubricString = rubricString + rubric.text
                #print('found rubrics : ' + str(rubricString))

                gen.SetRubric(rubricString)
                gen.SetTestDate(test.date)

                genresult = gen.GenerateTest(int(numberoftests))
                if genresult:


                    afilename = settings.PDFURL + gen.GeneratedPDF_URL
                    #print(str(afilename))
                    newPDF = PDF_link.create(afilename, test.__str__(), request.user)
                    newPDF.save()
                    #print('created a new PDF : ' + str(newPDF))

                    context = {
                        'title': ("Here's the link to your test"),
                        'queryset' : queryset,
                        'pdfurl' : afilename,
                    }
                    return TemplateResponse( request, 'link_to_pdf.html',
                                             context, current_app=modeladmin.admin_site)


                else:
                    context = {
                        'title': ("Unable to generate test"),
                        'queryset': queryset,
                        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                    }
                    return TemplateResponse(request, 'cannot_generate_test.html',
                                            context, current_app=modeladmin.admin_site)

        else:
            context = {
                'title': ("How many tests?"),
                'queryset': queryset,
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
            }
            return TemplateResponse(request, 'how_many_tests.html',
                                    context, current_app=modeladmin.admin_site)

    list_display = ['board', 'DevStatus', 'qualification', 'subject', 'unit', 'date']
    ordering = ['board', 'qualification', 'subject', 'unit']
    list_filter = ('board',)
    search_fields = ('board__name', 'qualification__name', 'subject__name', 'unit__name', 'DevStatus','tags__slug')
    actions = [make_complete, download_pdf]




class ScreenQuestionAdmin(ImportExportModelAdmin):
    pass

class MultipleChoiceChoiceAdmin(NestedTabularInline):
    model = MultipleChoiceChoice
    extra = 0


class MultipleChoicePartAdmin(NestedModelAdmin):
    inlines = [MultipleChoiceChoiceAdmin, ]
    pass

class NumberEntryPartAnswerAdmin(NestedTabularInline):
    model = NumberEntryPartAnswer
    extra = 0

class NumberEntryPartAdmin(NestedModelAdmin):
    inlines = [NumberEntryPartAnswerAdmin,]

class AlgebraAnswerAdmin(NestedTabularInline):
    model = AlgebraAnswer

class AlgebraPartAdmin(NestedModelAdmin):
    inlines = [AlgebraAnswerAdmin,]
    pass

class BookInline(admin.TabularInline):
    model = Book
    extra = 1

class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        BookInline,
    ]



make_complete.short_description = "Mark selected tests as Complete"

admin.site.register(Test, TestAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Image,ImageAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Author, AuthorAdmin)








