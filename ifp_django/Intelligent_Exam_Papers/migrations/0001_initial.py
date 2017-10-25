# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Image'
        db.create_table(u'Intelligent_Exam_Papers_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('createddate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Image'])

        # Adding model 'PDF_link'
        db.create_table(u'Intelligent_Exam_Papers_pdf_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('createddate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['PDF_link'])

        # Adding model 'Rubric'
        db.create_table(u'Intelligent_Exam_Papers_rubric', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Rubric'])

        # Adding model 'Board'
        db.create_table(u'Intelligent_Exam_Papers_board', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('logo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Image'])),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Board'])

        # Adding model 'Qualification'
        db.create_table(u'Intelligent_Exam_Papers_qualification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Qualification'])

        # Adding model 'Subject'
        db.create_table(u'Intelligent_Exam_Papers_subject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Subject'])

        # Adding model 'Unit'
        db.create_table(u'Intelligent_Exam_Papers_unit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Unit'])

        # Adding model 'Question'
        db.create_table(u'Intelligent_Exam_Papers_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createddate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('question_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('question_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('questions_can_span_pages', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('solution_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('solutions_can_span_pages', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('randoms_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pictures_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Question'])

        # Adding M2M table for field questionStaticImages on 'Question'
        m2m_table_name = db.shorten_name(u'Intelligent_Exam_Papers_question_questionStaticImages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'Intelligent_Exam_Papers.question'], null=False)),
            ('image', models.ForeignKey(orm[u'Intelligent_Exam_Papers.image'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'image_id'])

        # Adding model 'Question_Group'
        db.create_table(u'Intelligent_Exam_Papers_question_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('createddate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['Intelligent_Exam_Papers.Question_Group'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Question_Group'])

        # Adding M2M table for field Questions on 'Question_Group'
        m2m_table_name = db.shorten_name(u'Intelligent_Exam_Papers_question_group_Questions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question_group', models.ForeignKey(orm[u'Intelligent_Exam_Papers.question_group'], null=False)),
            ('question', models.ForeignKey(orm[u'Intelligent_Exam_Papers.question'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_group_id', 'question_id'])

        # Adding model 'Test'
        db.create_table(u'Intelligent_Exam_Papers_test', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Board'])),
            ('DevStatus', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('qualification', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Qualification'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Subject'])),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Unit'])),
            ('testXML', self.gf('django.db.models.fields.TextField')()),
            ('QuestionGroup', self.gf('mptt.fields.TreeForeignKey')(related_name='Question Group', to=orm['Intelligent_Exam_Papers.Question_Group'])),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Test'])

        # Adding M2M table for field rubric on 'Test'
        m2m_table_name = db.shorten_name(u'Intelligent_Exam_Papers_test_rubric')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('test', models.ForeignKey(orm[u'Intelligent_Exam_Papers.test'], null=False)),
            ('rubric', models.ForeignKey(orm[u'Intelligent_Exam_Papers.rubric'], null=False))
        ))
        db.create_unique(m2m_table_name, ['test_id', 'rubric_id'])

        # Adding M2M table for field GeneratedPDFs on 'Test'
        m2m_table_name = db.shorten_name(u'Intelligent_Exam_Papers_test_GeneratedPDFs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('test', models.ForeignKey(orm[u'Intelligent_Exam_Papers.test'], null=False)),
            ('pdf_link', models.ForeignKey(orm[u'Intelligent_Exam_Papers.pdf_link'], null=False))
        ))
        db.create_unique(m2m_table_name, ['test_id', 'pdf_link_id'])

        # Adding model 'Teacher'
        db.create_table(u'Intelligent_Exam_Papers_teacher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, blank=True)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Teacher'])

        # Adding model 'Department'
        db.create_table(u'Intelligent_Exam_Papers_department', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('Head_of_Department', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Department_HOD', to=orm['Intelligent_Exam_Papers.Teacher'])),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Department'])

        # Adding M2M table for field Teachers on 'Department'
        m2m_table_name = db.shorten_name(u'Intelligent_Exam_Papers_department_Teachers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('department', models.ForeignKey(orm[u'Intelligent_Exam_Papers.department'], null=False)),
            ('teacher', models.ForeignKey(orm[u'Intelligent_Exam_Papers.teacher'], null=False))
        ))
        db.create_unique(m2m_table_name, ['department_id', 'teacher_id'])

        # Adding model 'Student'
        db.create_table(u'Intelligent_Exam_Papers_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, blank=True)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Student'])

        # Adding model 'Class'
        db.create_table(u'Intelligent_Exam_Papers_class', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('Teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Teacher'])),
            ('Department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Department'])),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Class'])

        # Adding M2M table for field Students on 'Class'
        m2m_table_name = db.shorten_name(u'Intelligent_Exam_Papers_class_Students')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'Intelligent_Exam_Papers.class'], null=False)),
            ('student', models.ForeignKey(orm[u'Intelligent_Exam_Papers.student'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'student_id'])

        # Adding model 'Reference'
        db.create_table(u'Intelligent_Exam_Papers_reference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('URL', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('Description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Reference'])

        # Adding model 'Assignment'
        db.create_table(u'Intelligent_Exam_Papers_assignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('Teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Teacher'])),
            ('Class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Class'])),
            ('Description', self.gf('django.db.models.fields.TextField')()),
            ('PDF_Link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.PDF_link'], null=True, blank=True)),
            ('Reference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Reference'], null=True, blank=True)),
            ('Date_Start', self.gf('django.db.models.fields.DateField')()),
            ('Date_Finish', self.gf('django.db.models.fields.DateField')()),
            ('Max_Score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=20)),
            ('Merit_Score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=19)),
            ('Green_Score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=15)),
            ('Amber_score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=12)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Assignment'])

        # Adding model 'Result'
        db.create_table(u'Intelligent_Exam_Papers_result', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Class'])),
            ('Assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Assignment'])),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Result'])

        # Adding model 'Membership'
        db.create_table(u'Intelligent_Exam_Papers_membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Student'])),
            ('Result', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Result'])),
            ('Score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('Status', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('Comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('Flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('Late', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Membership'])

        # Adding model 'PartBase'
        db.create_table(u'Intelligent_Exam_Papers_partbase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['Intelligent_Exam_Papers.PartBase'])),
            ('MaxMarks', self.gf('django.db.models.fields.FloatField')()),
            ('MinMarks', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('TotalMarks', self.gf('django.db.models.fields.FloatField')()),
            ('Part_Text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('StepsSeenPenalty', self.gf('django.db.models.fields.SmallIntegerField')(default=0, null=True, blank=True)),
            ('Question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.ScreenQuestion'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['PartBase'])

        # Adding model 'RandomVariable'
        db.create_table(u'Intelligent_Exam_Papers_randomvariable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('definition', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['RandomVariable'])

        # Adding model 'ScreenQuestion'
        db.create_table(u'Intelligent_Exam_Papers_screenquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('createddate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('Question_Text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('DevStatus', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['ScreenQuestion'])

        # Adding M2M table for field part on 'ScreenQuestion'
        m2m_table_name = db.shorten_name(u'Intelligent_Exam_Papers_screenquestion_part')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('screenquestion', models.ForeignKey(orm[u'Intelligent_Exam_Papers.screenquestion'], null=False)),
            ('partbase', models.ForeignKey(orm[u'Intelligent_Exam_Papers.partbase'], null=False))
        ))
        db.create_unique(m2m_table_name, ['screenquestion_id', 'partbase_id'])

        # Adding M2M table for field variable on 'ScreenQuestion'
        m2m_table_name = db.shorten_name(u'Intelligent_Exam_Papers_screenquestion_variable')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('screenquestion', models.ForeignKey(orm[u'Intelligent_Exam_Papers.screenquestion'], null=False)),
            ('randomvariable', models.ForeignKey(orm[u'Intelligent_Exam_Papers.randomvariable'], null=False))
        ))
        db.create_unique(m2m_table_name, ['screenquestion_id', 'randomvariable_id'])

        # Adding model 'AlgebraAnswer'
        db.create_table(u'Intelligent_Exam_Papers_algebraanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('marks', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.AlgebraPart'], null=True, blank=True)),
            ('feedback', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['AlgebraAnswer'])

        # Adding model 'variable'
        db.create_table(u'Intelligent_Exam_Papers_variable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('domain_start', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('domain_end', self.gf('django.db.models.fields.FloatField')(default=5)),
            ('domain_step', self.gf('django.db.models.fields.FloatField')(default=0.1)),
            ('failure_rate', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['variable'])

        # Adding model 'AlgebraPart'
        db.create_table(u'Intelligent_Exam_Papers_algebrapart', (
            (u'partbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Intelligent_Exam_Papers.PartBase'], unique=True, primary_key=True)),
            ('must_have_strings', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('not_allowed_strings', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('max_fraction_depth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('min_fraction_depth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_power_depth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('min_power_depth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['AlgebraPart'])

        # Adding M2M table for field answer on 'AlgebraPart'
        m2m_table_name = db.shorten_name(u'Intelligent_Exam_Papers_algebrapart_answer')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('algebrapart', models.ForeignKey(orm[u'Intelligent_Exam_Papers.algebrapart'], null=False)),
            ('algebraanswer', models.ForeignKey(orm[u'Intelligent_Exam_Papers.algebraanswer'], null=False))
        ))
        db.create_unique(m2m_table_name, ['algebrapart_id', 'algebraanswer_id'])

        # Adding M2M table for field variables on 'AlgebraPart'
        m2m_table_name = db.shorten_name(u'Intelligent_Exam_Papers_algebrapart_variables')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('algebrapart', models.ForeignKey(orm[u'Intelligent_Exam_Papers.algebrapart'], null=False)),
            ('variable', models.ForeignKey(orm[u'Intelligent_Exam_Papers.variable'], null=False))
        ))
        db.create_unique(m2m_table_name, ['algebrapart_id', 'variable_id'])

        # Adding model 'NumberEntryPartAnswer'
        db.create_table(u'Intelligent_Exam_Papers_numberentrypartanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer_from', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('answer_to', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('score', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('feedback', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('Part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.NumberEntryPart'])),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['NumberEntryPartAnswer'])

        # Adding model 'NumberEntryPart'
        db.create_table(u'Intelligent_Exam_Papers_numberentrypart', (
            (u'partbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Intelligent_Exam_Papers.PartBase'], unique=True, primary_key=True)),
            ('text_before_answer_prompt', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('text_after_answer_prompt', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('accept_account_negatives', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['NumberEntryPart'])

        # Adding M2M table for field answers on 'NumberEntryPart'
        m2m_table_name = db.shorten_name(u'Intelligent_Exam_Papers_numberentrypart_answers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('numberentrypart', models.ForeignKey(orm[u'Intelligent_Exam_Papers.numberentrypart'], null=False)),
            ('numberentrypartanswer', models.ForeignKey(orm[u'Intelligent_Exam_Papers.numberentrypartanswer'], null=False))
        ))
        db.create_unique(m2m_table_name, ['numberentrypart_id', 'numberentrypartanswer_id'])

        # Adding model 'MultipleChoiceChoice'
        db.create_table(u'Intelligent_Exam_Papers_multiplechoicechoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('marks', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('Part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.MultipleChoicePart'])),
            ('feedback', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['MultipleChoiceChoice'])

        # Adding model 'MultipleChoicePart'
        db.create_table(u'Intelligent_Exam_Papers_multiplechoicepart', (
            (u'partbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Intelligent_Exam_Papers.PartBase'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['MultipleChoicePart'])

        # Adding M2M table for field choices on 'MultipleChoicePart'
        m2m_table_name = db.shorten_name(u'Intelligent_Exam_Papers_multiplechoicepart_choices')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('multiplechoicepart', models.ForeignKey(orm[u'Intelligent_Exam_Papers.multiplechoicepart'], null=False)),
            ('multiplechoicechoice', models.ForeignKey(orm[u'Intelligent_Exam_Papers.multiplechoicechoice'], null=False))
        ))
        db.create_unique(m2m_table_name, ['multiplechoicepart_id', 'multiplechoicechoice_id'])

        # Adding model 'Author'
        db.create_table(u'Intelligent_Exam_Papers_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Author'])

        # Adding model 'Book'
        db.create_table(u'Intelligent_Exam_Papers_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Intelligent_Exam_Papers.Author'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'Intelligent_Exam_Papers', ['Book'])


    def backwards(self, orm):
        # Deleting model 'Image'
        db.delete_table(u'Intelligent_Exam_Papers_image')

        # Deleting model 'PDF_link'
        db.delete_table(u'Intelligent_Exam_Papers_pdf_link')

        # Deleting model 'Rubric'
        db.delete_table(u'Intelligent_Exam_Papers_rubric')

        # Deleting model 'Board'
        db.delete_table(u'Intelligent_Exam_Papers_board')

        # Deleting model 'Qualification'
        db.delete_table(u'Intelligent_Exam_Papers_qualification')

        # Deleting model 'Subject'
        db.delete_table(u'Intelligent_Exam_Papers_subject')

        # Deleting model 'Unit'
        db.delete_table(u'Intelligent_Exam_Papers_unit')

        # Deleting model 'Question'
        db.delete_table(u'Intelligent_Exam_Papers_question')

        # Removing M2M table for field questionStaticImages on 'Question'
        db.delete_table(db.shorten_name(u'Intelligent_Exam_Papers_question_questionStaticImages'))

        # Deleting model 'Question_Group'
        db.delete_table(u'Intelligent_Exam_Papers_question_group')

        # Removing M2M table for field Questions on 'Question_Group'
        db.delete_table(db.shorten_name(u'Intelligent_Exam_Papers_question_group_Questions'))

        # Deleting model 'Test'
        db.delete_table(u'Intelligent_Exam_Papers_test')

        # Removing M2M table for field rubric on 'Test'
        db.delete_table(db.shorten_name(u'Intelligent_Exam_Papers_test_rubric'))

        # Removing M2M table for field GeneratedPDFs on 'Test'
        db.delete_table(db.shorten_name(u'Intelligent_Exam_Papers_test_GeneratedPDFs'))

        # Deleting model 'Teacher'
        db.delete_table(u'Intelligent_Exam_Papers_teacher')

        # Deleting model 'Department'
        db.delete_table(u'Intelligent_Exam_Papers_department')

        # Removing M2M table for field Teachers on 'Department'
        db.delete_table(db.shorten_name(u'Intelligent_Exam_Papers_department_Teachers'))

        # Deleting model 'Student'
        db.delete_table(u'Intelligent_Exam_Papers_student')

        # Deleting model 'Class'
        db.delete_table(u'Intelligent_Exam_Papers_class')

        # Removing M2M table for field Students on 'Class'
        db.delete_table(db.shorten_name(u'Intelligent_Exam_Papers_class_Students'))

        # Deleting model 'Reference'
        db.delete_table(u'Intelligent_Exam_Papers_reference')

        # Deleting model 'Assignment'
        db.delete_table(u'Intelligent_Exam_Papers_assignment')

        # Deleting model 'Result'
        db.delete_table(u'Intelligent_Exam_Papers_result')

        # Deleting model 'Membership'
        db.delete_table(u'Intelligent_Exam_Papers_membership')

        # Deleting model 'PartBase'
        db.delete_table(u'Intelligent_Exam_Papers_partbase')

        # Deleting model 'RandomVariable'
        db.delete_table(u'Intelligent_Exam_Papers_randomvariable')

        # Deleting model 'ScreenQuestion'
        db.delete_table(u'Intelligent_Exam_Papers_screenquestion')

        # Removing M2M table for field part on 'ScreenQuestion'
        db.delete_table(db.shorten_name(u'Intelligent_Exam_Papers_screenquestion_part'))

        # Removing M2M table for field variable on 'ScreenQuestion'
        db.delete_table(db.shorten_name(u'Intelligent_Exam_Papers_screenquestion_variable'))

        # Deleting model 'AlgebraAnswer'
        db.delete_table(u'Intelligent_Exam_Papers_algebraanswer')

        # Deleting model 'variable'
        db.delete_table(u'Intelligent_Exam_Papers_variable')

        # Deleting model 'AlgebraPart'
        db.delete_table(u'Intelligent_Exam_Papers_algebrapart')

        # Removing M2M table for field answer on 'AlgebraPart'
        db.delete_table(db.shorten_name(u'Intelligent_Exam_Papers_algebrapart_answer'))

        # Removing M2M table for field variables on 'AlgebraPart'
        db.delete_table(db.shorten_name(u'Intelligent_Exam_Papers_algebrapart_variables'))

        # Deleting model 'NumberEntryPartAnswer'
        db.delete_table(u'Intelligent_Exam_Papers_numberentrypartanswer')

        # Deleting model 'NumberEntryPart'
        db.delete_table(u'Intelligent_Exam_Papers_numberentrypart')

        # Removing M2M table for field answers on 'NumberEntryPart'
        db.delete_table(db.shorten_name(u'Intelligent_Exam_Papers_numberentrypart_answers'))

        # Deleting model 'MultipleChoiceChoice'
        db.delete_table(u'Intelligent_Exam_Papers_multiplechoicechoice')

        # Deleting model 'MultipleChoicePart'
        db.delete_table(u'Intelligent_Exam_Papers_multiplechoicepart')

        # Removing M2M table for field choices on 'MultipleChoicePart'
        db.delete_table(db.shorten_name(u'Intelligent_Exam_Papers_multiplechoicepart_choices'))

        # Deleting model 'Author'
        db.delete_table(u'Intelligent_Exam_Papers_author')

        # Deleting model 'Book'
        db.delete_table(u'Intelligent_Exam_Papers_book')


    models = {
        u'Intelligent_Exam_Papers.algebraanswer': {
            'Meta': {'object_name': 'AlgebraAnswer'},
            'feedback': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marks': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'part': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.AlgebraPart']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'Intelligent_Exam_Papers.algebrapart': {
            'Meta': {'object_name': 'AlgebraPart', '_ormbases': [u'Intelligent_Exam_Papers.PartBase']},
            'answer': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'algebra_incorrect_answer'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['Intelligent_Exam_Papers.AlgebraAnswer']"}),
            'max_fraction_depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_power_depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_fraction_depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_power_depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'must_have_strings': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'not_allowed_strings': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'partbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['Intelligent_Exam_Papers.PartBase']", 'unique': 'True', 'primary_key': 'True'}),
            'variables': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['Intelligent_Exam_Papers.variable']", 'null': 'True', 'blank': 'True'})
        },
        u'Intelligent_Exam_Papers.assignment': {
            'Amber_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '12'}),
            'Class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Class']"}),
            'Date_Finish': ('django.db.models.fields.DateField', [], {}),
            'Date_Start': ('django.db.models.fields.DateField', [], {}),
            'Description': ('django.db.models.fields.TextField', [], {}),
            'Green_Score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '15'}),
            'Max_Score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '20'}),
            'Merit_Score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '19'}),
            'Meta': {'object_name': 'Assignment'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'PDF_Link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.PDF_link']", 'null': 'True', 'blank': 'True'}),
            'Reference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Reference']", 'null': 'True', 'blank': 'True'}),
            'Teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Teacher']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Intelligent_Exam_Papers.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'Intelligent_Exam_Papers.board': {
            'Meta': {'object_name': 'Board'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'Intelligent_Exam_Papers.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Author']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'Intelligent_Exam_Papers.class': {
            'Department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Department']"}),
            'Meta': {'object_name': 'Class'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'Students': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Intelligent_Exam_Papers.Student']", 'symmetrical': 'False'}),
            'Teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Teacher']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Intelligent_Exam_Papers.department': {
            'Head_of_Department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Department_HOD'", 'to': u"orm['Intelligent_Exam_Papers.Teacher']"}),
            'Meta': {'object_name': 'Department'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'Teachers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'Department_Teachers'", 'symmetrical': 'False', 'to': u"orm['Intelligent_Exam_Papers.Teacher']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Intelligent_Exam_Papers.image': {
            'Meta': {'object_name': 'Image'},
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'Intelligent_Exam_Papers.membership': {
            'Comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'Late': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'Meta': {'object_name': 'Membership'},
            'Result': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Result']"}),
            'Score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'Status': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'Student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Student']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Intelligent_Exam_Papers.multiplechoicechoice': {
            'Meta': {'object_name': 'MultipleChoiceChoice'},
            'Part': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.MultipleChoicePart']"}),
            'Text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'feedback': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marks': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'Intelligent_Exam_Papers.multiplechoicepart': {
            'Meta': {'object_name': 'MultipleChoicePart', '_ormbases': [u'Intelligent_Exam_Papers.PartBase']},
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['Intelligent_Exam_Papers.MultipleChoiceChoice']", 'null': 'True', 'blank': 'True'}),
            u'partbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['Intelligent_Exam_Papers.PartBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'Intelligent_Exam_Papers.numberentrypart': {
            'Meta': {'object_name': 'NumberEntryPart', '_ormbases': [u'Intelligent_Exam_Papers.PartBase']},
            'accept_account_negatives': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['Intelligent_Exam_Papers.NumberEntryPartAnswer']", 'null': 'True', 'blank': 'True'}),
            u'partbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['Intelligent_Exam_Papers.PartBase']", 'unique': 'True', 'primary_key': 'True'}),
            'text_after_answer_prompt': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'text_before_answer_prompt': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'})
        },
        u'Intelligent_Exam_Papers.numberentrypartanswer': {
            'Meta': {'object_name': 'NumberEntryPartAnswer'},
            'Part': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.NumberEntryPart']"}),
            'answer_from': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'answer_to': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'feedback': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'})
        },
        u'Intelligent_Exam_Papers.partbase': {
            'Description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'MaxMarks': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'object_name': 'PartBase'},
            'MinMarks': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'Part_Text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.ScreenQuestion']"}),
            'StepsSeenPenalty': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'TotalMarks': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['Intelligent_Exam_Papers.PartBase']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'Intelligent_Exam_Papers.pdf_link': {
            'Meta': {'object_name': 'PDF_link'},
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'Intelligent_Exam_Papers.qualification': {
            'Meta': {'object_name': 'Qualification'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'Intelligent_Exam_Papers.question': {
            'Meta': {'object_name': 'Question'},
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'pictures_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'questionStaticImages': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'images'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['Intelligent_Exam_Papers.Image']"}),
            'question_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'question_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'questions_can_span_pages': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'randoms_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'solution_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'solutions_can_span_pages': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'Intelligent_Exam_Papers.question_group': {
            'Meta': {'object_name': 'Question_Group'},
            'Questions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['Intelligent_Exam_Papers.Question']", 'null': 'True', 'blank': 'True'}),
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['Intelligent_Exam_Papers.Question_Group']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'Intelligent_Exam_Papers.randomvariable': {
            'Meta': {'object_name': 'RandomVariable'},
            'definition': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'Intelligent_Exam_Papers.reference': {
            'Description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'Meta': {'object_name': 'Reference'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'URL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Intelligent_Exam_Papers.result': {
            'Assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Assignment']"}),
            'Class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Class']"}),
            'Meta': {'object_name': 'Result'},
            'StudentResults': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Intelligent_Exam_Papers.Student']", 'through': u"orm['Intelligent_Exam_Papers.Membership']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Intelligent_Exam_Papers.rubric': {
            'Meta': {'object_name': 'Rubric'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'Intelligent_Exam_Papers.screenquestion': {
            'Description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'DevStatus': ('django.db.models.fields.IntegerField', [], {}),
            'Meta': {'object_name': 'ScreenQuestion'},
            'Question_Text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'part': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'question_part'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['Intelligent_Exam_Papers.PartBase']"}),
            'variable': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['Intelligent_Exam_Papers.RandomVariable']", 'null': 'True', 'blank': 'True'})
        },
        u'Intelligent_Exam_Papers.student': {
            'Meta': {'object_name': 'Student'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'blank': 'True'})
        },
        u'Intelligent_Exam_Papers.subject': {
            'Meta': {'object_name': 'Subject'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'Intelligent_Exam_Papers.teacher': {
            'Meta': {'object_name': 'Teacher'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'blank': 'True'})
        },
        u'Intelligent_Exam_Papers.test': {
            'DevStatus': ('django.db.models.fields.IntegerField', [], {}),
            'GeneratedPDFs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'generated_PDFs'", 'blank': 'True', 'to': u"orm['Intelligent_Exam_Papers.PDF_link']"}),
            'Meta': {'object_name': 'Test'},
            'QuestionGroup': ('mptt.fields.TreeForeignKey', [], {'related_name': "'Question Group'", 'to': u"orm['Intelligent_Exam_Papers.Question_Group']"}),
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Board']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qualification': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Qualification']"}),
            'rubric': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'Rubrics'", 'symmetrical': 'False', 'to': u"orm['Intelligent_Exam_Papers.Rubric']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Subject']"}),
            'testXML': ('django.db.models.fields.TextField', [], {}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Intelligent_Exam_Papers.Unit']"})
        },
        u'Intelligent_Exam_Papers.unit': {
            'Meta': {'object_name': 'Unit'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'Intelligent_Exam_Papers.variable': {
            'Meta': {'object_name': 'variable'},
            'domain_end': ('django.db.models.fields.FloatField', [], {'default': '5'}),
            'domain_start': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'domain_step': ('django.db.models.fields.FloatField', [], {'default': '0.1'}),
            'failure_rate': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['Intelligent_Exam_Papers']