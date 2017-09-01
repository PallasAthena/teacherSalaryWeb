#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:02:54 2017

@author: biqiao
"""

import datetime
import numpy as np
import pandas as pd



class AnswerSalary():

    RANK_PRICE_CHARGE_JUNIOR = {3: 0.35, 4: 0.40, 10: 0.45, 25: 0.50}
    RANK_PRICE_CHARGE_MIDDLE = {3: 0.45, 4: 0.50, 10: 0.55, 16: 0.60}
    RANK_PRICE_CHARGE_HIGH = {3: 0.60, 6: 0.65, 10: 0.70, 16: 0.75, 25: 0.80}

    RANK_PRICE_FREE_JUNIOR_1 = {3: 0.35, 4: 0.40, 6: 0.40, 10: 0.45, 16: 0.45, 25: 0.50}
    RANK_PRICE_FREE_MIDDLE_1 = {3: 0.45, 4: 0.50, 6: 0.50, 10: 0.55, 16: 0.55, 25: 0.60}

    RANK_PRICE_FREE_JUNIOR_2 = {3: 0.20, 4: 0.20, 6: 0.25, 10: 0.25, 16: 0.3, 25: 0.30}
    RANK_PRICE_FREE_MIDDLE_2 = {3: 0.20, 4: 0.20, 6: 0.25, 10: 0.25, 16: 0.3, 25: 0.30}
    RANK_PRICE_FREE_HIGH = {3: 0.60, 6: 0.65, 10: 0.70, 16: 0.75, 25: 0.80}

    def __init__(self,answers):
        keys = ['teacher_id', 'rating', 'grade', 'answer_time', 'answer_type']
        free_answers_d = {}
        charge_answers_d = {}
        one2one_answers_d = {}
        # separste answer(list) to different groups by its type
        # change list to dict
        for answer in answers:
            if answer[-1] == 'free':
                free_answers_d = {key: value for key, value in zip(keys, answer)}
                self.free_answers.append(free_answers_d)
            elif answer[-1] == 'charge':
                charge_answers_d = {key: value for key, value in zip(keys, answer)}
                self.charge_answers.append(charge_answers_d)
            else:
                one2one_answers_d = {key: value for key, value in zip(keys, answer)}
                self.one2one_answers.append(one2one_answers_d)
                              
    
    def charged_answers_salary(self):
        for charge_answer in self.charge_answers:
        charge_answer.update({'salary':__charged_salary(charge_answer)})
        

    def __charged_salary(self, charge_answer):
        # charged answer, only cares rank
        # 1-6 charged answer
        salary = 0
        if charge_answer['grade'] <= 6:
            # rank3
            if charge_answer['rating'] == 3:
                salary = charge_answer['answer_time'] / 60 * self.RANK_PRICE_CHARGE_JUNIOR[3]
            elif 4 <= charge_answer['rating'] <= 9:
                salary = charge_answer['answer_time'] / 60 * self.RANK_PRICE_CHARGE_JUNIOR[4]
            elif 10 <= charge_answer['rating'] <= 24:
                salary = charge_answer['answer_time'] / 60 * self.RANK_PRICE_CHARGE_JUNIOR[10]
            else:
                salary = charge_answer['answer_time'] / 60 * self.RANK_PRICE_CHARGE_JUNIOR[25]

        # 7-9 charged answer
        elif 7 <= charge_answer['grade'] <= 9:
            if charge_answer['rating'] == 3:
                salary = charge_answer['answer_time'] / 60 * self.RANK_PRICE_CHARGE_MIDDLE[3]
            elif 4 <= charge_answer['rating'] <= 9:
                salary = charge_answer['answer_time'] / 60 * self.RANK_PRICE_CHARGE_MIDDLE[4]
            elif 10 <= charge_answer['rating'] <= 15:
                salary = charge_answer['answer_time'] / 60 * self.RANK_PRICE_CHARGE_MIDDLE[10]
            else:
                salary = charge_answer['answer_time'] / 60 * self.RANK_PRICE_CHARGE_MIDDLE[16]
        # 9-12 charged answer
        else:
            if 3 <= charge_answer['rating'] <= 5:
                salary = charge_answer['answer_time'] / 60 * self.RANK_PRICE_CHARGE_HIGH[3]
            elif 6 <= charge_answer['rating'] <= 9:
                salary = charge_answer['answer_time'] / 60 * self.RANK_PRICE_CHARGE_HIGH[6]
            elif 10 <= charge_answer['rating'] <= 15:
                salary = charge_answer['answer_time'] / 60 * self.RANK_PRICE_CHARGE_HIGH[10]
            elif 16 <= charge_answer['rating'] <= 24:
                salary = charge_answer['answer_time'] / 60 * self.RANK_PRICE_CHARGE_HIGH[16]
            else:
                salary = charge_answer['answer_time'] / 60 * self.RANK_PRICE_CHARGE_HIGH[25]
        return salary
    
    
    
    def free_answers_salary(self):
        #split answers to less than 10 minutes
        self.__free_answers_split(self.free_answers)
        for free_answer in self.free_answers:
        free_answer.update({'salary':__free_salary(free_answer)})
        
        
        
    def __free_answers_split(self,free_answers):
        answers_split = []
        for free_answer in free_answers:
            # when answer_time > 600, split it to several records, answer_time in each one should <= 600
            # remove the old item ,add splited ones
            if free_answer['answer_time'] > 600:
                answers_split.extend(self.__split_to_10(free_answer))
                free_answers.remove(free_answer)

        free_answers.extend(answers_split)

    

    # when answer_time > 600, split it to several records, answer_time in each one should <= 600
    def __split_to_10(self,answer):
        out = []
        n = 0
        while n < int(answer['answer_time']) // 600:
            out.append(answer.copy())
            out[-1]['answer_time'] = '600'
            n += 1

        out.append(answer.copy())
        out[-1]['answer_time'] = str(int(answer['answer_time']) % 600)
        return out
    
        
    def __free_salary(self, free_answer):
        salary = 0
        # grade 1~6
        if free_answer['grade'] <= 6:
            # rank3
            if free_answer['rating'] == 3:
                # longer than 4min
                if int(free_answer['answer_time']) > 240:
                    salary = 4 * self.RANK_PRICE_FREE_JUNIOR_1[3]
                    salary += (int(free_answer['answer_time']) - 240) / 60 * self.RANK_PRICE_FREE_JUNIOR_2[3]
                else:
                    salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_JUNIOR_1[3]

            elif 4 <= free_answer['rating'] <= 5:
                if int(free_answer['answer_time']) > 240:
                    salary = 4 * self.RANK_PRICE_FREE_JUNIOR_1[4]
                    salary += (int(free_answer['answer_time']) - 240) / 60 * self.RANK_PRICE_FREE_JUNIOR_2[4]
                else:
                    salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_JUNIOR_1[4]

            elif 6 <= free_answer['rating'] <= 9:
                if int(free_answer['answer_time']) > 240:
                    salary = 4 * self.RANK_PRICE_FREE_JUNIOR_1[6]
                    salary += (int(free_answer['answer_time']) - 240) / 60 * self.RANK_PRICE_FREE_JUNIOR_2[6]
                else:
                    salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_JUNIOR_1[6]
            elif 10 <= free_answer['rating'] <= 15:
                if int(free_answer['answer_time']) > 240:
                    salary = 4 * self.RANK_PRICE_FREE_JUNIOR_1[10]
                    salary += (int(free_answer['answer_time']) - 240) / 60 * self.RANK_PRICE_FREE_JUNIOR_2[10]
                else:
                    salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_JUNIOR_1[10]
            elif 16 <= free_answer['rating'] <= 24:
                if int(free_answer['answer_time']) > 240:
                    salary = 4 * self.RANK_PRICE_FREE_JUNIOR_1[16]
                    salary += (int(free_answer['answer_time']) - 240) / 60 * self.RANK_PRICE_FREE_JUNIOR_2[16]
                else:
                    salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_JUNIOR_1[16]
            else:
                if int(free_answer['answer_time']) > 240:
                    salary = 4 * self.RANK_PRICE_FREE_JUNIOR_1[25]
                    salary += (int(free_answer['answer_time']) - 240) / 60 * self.RANK_PRICE_FREE_JUNIOR_2[25]
                else:
                    salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_JUNIOR_1[25]

        elif 7 <= free_answer['grade'] <= 9:
            # rank3
            if free_answer['rating'] == 3:
                # longer than 6min
                if int(free_answer['answer_time']) > 360:
                    salary = 6 * self.RANK_PRICE_FREE_MIDDLE_1[3]
                    salary += (int(free_answer['answer_time']) - 360) / 60 * self.RANK_PRICE_FREE_MIDDLE_2[3]
                else:
                    salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_MIDDLE_1[3]

            elif 4 <= free_answer['rating'] <= 5:
                if int(free_answer['answer_time']) > 360:
                    salary = 6 * self.RANK_PRICE_FREE_MIDDLE_1[4]
                    salary += (int(free_answer['answer_time']) - 360) / 60 * self.RANK_PRICE_FREE_MIDDLE_2[4]
                else:
                    salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_MIDDLE_1[4]

            elif 6 <= free_answer['rating'] <= 9:
                if int(free_answer['answer_time']) > 360:
                    salary = 6 * self.RANK_PRICE_FREE_MIDDLE_1[6]
                    salary += (int(free_answer['answer_time']) - 360) / 60 * self.RANK_PRICE_FREE_MIDDLE_2[6]
                else:
                    salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_MIDDLE_1[6]
            elif 10 <= free_answer['rating'] <= 15:
                if int(free_answer['answer_time']) > 360:
                    salary = 6 * self.RANK_PRICE_FREE_MIDDLE_1[10]
                    salary += (int(free_answer['answer_time']) - 360) / 60 * self.RANK_PRICE_FREE_MIDDLE_2[10]
                else:
                    salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_MIDDLE_1[10]
            elif 16 <= free_answer['rating'] <= 24:
                if int(free_answer['answer_time']) > 360:
                    salary = 6 * self.RANK_PRICE_FREE_MIDDLE_1[16]
                    salary += int(free_answer['answer_time']) - 360 / 60 * self.RANK_PRICE_FREE_MIDDLE_2[16]
                else:
                    salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_MIDDLE_1[16]
            else:
                if int(free_answer['answer_time']) > 360:
                    salary = 6 * self.RANK_PRICE_FREE_MIDDLE_1[25]
                    salary += (int(free_answer['answer_time']) - 360) / 60 * self.RANK_PRICE_FREE_MIDDLE_2[25]
                else:
                    salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_MIDDLE_1[25]
        else:
            if 3 <= free_answer['rating'] <= 5:
                salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_HIGH[3]
            elif 6 <= free_answer['rating'] <= 9:
                salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_HIGH[6]
            elif 10 <= free_answer['rating'] <= 15:
                salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_HIGH[10]
            elif 16 <= free_answer['rating'] <= 24:
                salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_HIGH[16]
            else:
                salary = int(free_answer['answer_time']) / 60 * self.RANK_PRICE_FREE_HIGH[25]

        return salary
        

class SalarySheet():
    
    def __init__(self, answers, teacher_infos, csv_file, html_file):
        self.answers = answers
        self.teacher_infos = teacher_infos
        self.csv = csv_file
        self.html = html_file
        

    def salary_sheet(self):
        all_answers_df = to_dataFrame(self.answers)
        #counting answer_time, salary per answer_type
        all_answers_df['answer_time'] = all_answers_df['answer_time'].astype(int)
        all_answers_df['salary'] = all_answers_df['salary'].astype(float)
        salary_per_type = all_answers_df.groupby(['teacher_id', 'rating', 'answer_type']).sum()
        salary_per_type2 = salary_per_type.reset_index() 
        salary_per_type2['teacher_id'] = salary_per_type2['teacher_id'].astype(int) #'teacher_id','rating','answer_type','answer_time','salary'
        #salarysum per teacher
        salary_per_teacher = all_answers_df.groupby('teacher_id').sum().reset_index().loc[:, ['teacher_id', 'salary']] 
        salary_per_teacher = salary_per_teacher.rename(columns = {'salary':'salarySum'})
        salary_per_teacher['teacher_id'] = salary_per_teacher['teacher_id'].astype(int) #'teacher_id', 'salarySum'
        #
        teacher_infos_df = pd.DataFrame(self.teacher_infos, columns=['teacher_id','name','username'])
        teacher_infos_df['teacher_id'] = teacher_infos_df['teacher_id'].astype(int) #'teacher_id','name','username'
        ####
        df = pd.merge(teacher_infos_df, salary_per_teacher, on='teacher_id')
        df['cc'] = df.groupby('teacher_id').cumcount()
        salary_per_type2['cc'] = salary_per_type2.groupby('teacher_id').cumcount()
        teacher_info_salary = pd.merge(salary_per_type2, df, on=('teacher_id', 'cc'), how='outer')
        teacher_info_salary = teacher_info_salary.loc[:, ['teacher_id','name','username','rating','answer_type','answer_time','salary','salarySum']]
        ##
        teacher_info_salary.to_csv(self.csv, encoding='utf-8-sig')
        teacher_info_salary.to_html(self.html, encoding='utf-8-sig')
        


class TeacherInfo():
    
    def __init__(self, teacher_ids):
        self.teacher_ids = teacher_ids
                   
    def get_teacher_info(self):
        sql = '''select  ot.teacher_id, COALESCE(au.first_name, au.last_name) as name, 
                              au.username 
                              from  acornuser.acorn_user au
                              inner join acornuser.ozing_teacher ot 
                              on ot.user_id = au.id
                              where ot.teacher_id in ({})'''.format(self.teacher_ids)
                              
        result =  DB().select(sql)
        if result:
            teacher_info_lst = [list(x) for x in result]
        return teacher_info_lst    

    
    
            
    

    
