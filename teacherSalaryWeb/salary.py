#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:02:54 2017

@author: biqiao
"""


from .db import DB
from .countSalary import TeacherInfo, SalarySheet, AnswerSalary


CSV_FILE = 'salary.csv' 
HTML_FILE = 'salary_table.html' 

       

def get_answers(date_from, date_to):
    get_answer_sql = '''
        SELECT
        a.teacher_id,
        a.teacher_rating,
        g.grade_id,
        a.FIXED_ANSWER_TIME,
        a.answer_type

    FROM
        ozing_answer a,
        ozing_grade g
    WHERE
        a.grade_id = g.grade_id
            AND a.PREAPPOINTMENT_ID IS NULL
            AND a.begin_time < a.end_time
            AND (a.answer_time >= 30
            OR a.fixed_answer_time >= 30)
            AND a.teacher_rating > 2
            AND a.date_added > "{}"
            AND a.date_added < "{}"
            AND a.TEACHER_ID IN (SELECT
                teacher_id
            FROM
                ozing_teacher)
            and (a.answer_type = 'free' or a.answer_type = 'charge')
            '''.format(date_from, date_to)

    result = DB().select(get_answer_sql)
    if result:
        answers = [list(item) for item in result]
        return answers
        

    
def salary_sheet(date_from, date_to):
    answers = get_answers(date_from, date_to)
    all_answer_salary = AnswerSalary(answers).free_answers_salary() + \
                        AnswerSalary(answers).charged_answers_salary()
    
    teacher_ids = ','.join('{}'.format(item[0]) for item in answers)
    teacher_infos = TeacherInfo(teacher_ids).get_teacher_info
    
    SalarySheet(all_answer_salary, teacher_infos, CSV_FILE, HTML_FILE)

    

#
#class Salary():
#
#    def __init__(self, date_from, date_to ):
#        self.date_from = date_from
#        self.date_to = date_to
#
#    def get_answers(self):
#        get_answer_sql = '''
#            SELECT
#            a.teacher_id,
#            a.teacher_rating,
#            g.grade_id,
#            a.FIXED_ANSWER_TIME,
#            a.answer_type
#
#        FROM
#            ozing_answer a,
#            ozing_grade g
#        WHERE
#            a.grade_id = g.grade_id
#                AND a.PREAPPOINTMENT_ID IS NULL
#                AND a.begin_time < a.end_time
#                AND (a.answer_time >= 30
#                OR a.fixed_answer_time >= 30)
#                AND a.teacher_rating > 2
#                AND a.date_added > "{}"
#                AND a.date_added < "{}"
#                AND a.TEACHER_ID IN (SELECT
#                    teacher_id
#                FROM
#                    ozing_teacher)
#                and (a.answer_type = 'free' or a.answer_type = 'charge')
#                '''.format(self.date_from, self.date_to)
#
#        result = DB().select(get_answer_sql)
#        if result:
#            self.answers = [list(item) for item in result]
#
#    def salary_counting(self):
#        self.free_answer_salary = AnswerSalary(self.answers).free_answers_salary()
#        self.charge_answer_salary = AnswerSalary(self.answers).charged_answers_salary()
#        self.all_answer_salary = self.free_answer_salary + self.charge_answer_salary
#        
#        
#    def salary_sheet(self, csvfile=None):
#        teacher_ids = ','.join('{}'.format(item[0]) for item in self.answers)
#        
#        
#        self.teacher_infos = TeacherInfo(teacher_ids).get_teacher_info
#        SalarySheet(self.all_answer_salary, self.teacher_infos, csvfile)
        
        
       



