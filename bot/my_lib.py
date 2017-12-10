#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import csv
import sys
from random import *
 
 
import os

directory = "cav"
'''
id	link	parsed	valid	infobox	infovalue	date_parsed	html	text_only	history_col	version_col	release_col	page_last_updated	category	latest_version	type	release_info	title

'''

con = lite.connect('final_master_modified.db')
cur = con.cursor()

list_notfound=['I am not able to find any such information', 'I can not find anything on the subject.','sorry i dont have such information now, Please try again Later','No such info found ']




def wiki_final(query):
    print query
    s=query
    q=""
    try:
        s_split=s.split()
        #print "s_split",s_split
        
        if(len(s_split)>1):
            print "len>1",str(s_split)#,s_split
            s_query=""
            #select * from master where link like '%microsoft%' or  link like '%visu%'
            like_quer=""
            for s_ in s_split:
                like_quer=like_quer+" title like '%"+s_+"%' and "
            q="select * from master where "+like_quer
            q= q[:-4]+" ;"
            print q,"\n"
            
        else:
            print "len one"
            q="select * from master where "+"title like '%"+s+"%';"
            #print q
        cur.execute(q)
        #print dir(cur)
        """
    ['__class__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__iter__', '__new__',
    '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'arraysize', 'close',
    'connection', 'description', 'execute', 'executemany', 'executescript', 'fetchall', 'fetchmany', 'fetchone', 'lastrowid', 'next',
    'row_factory', 'rowcount', 'setinputsizes', 'setoutputsize']
        """
        data = cur.fetchall()
        '''['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__', '__doc__', '__eq__', '__format__', '__ge__',
    '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__iter__', '__le__', '__len__',
    '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__',
    '__setslice__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
    '''
        print "---",len(data)
        res_len=len(data)
        
        if(res_len<=3):
            count=0
            for x in data:
                count=count+1
                str_x=str(x[1]).replace("_"," ")
                print str(count)," ",str_x[5:]
                if(count>15):
                    break            


    ##        if(res_len>=7):
    ##            print " Disambuigation found please be more specific"
        
        if(res_len==0):
            print  list_notfound[randint(0, len(list_notfound)-1)]

        if(res_len==1):
            #data = cur.fetchall()
            #print  "print one ",
            data=data[0]
            stable_rel_one=data[17]
            stable_rel_one=stable_rel_one.replace("[b1]","")
            type1=data[14]
            if(stable_rel_one):
                print "Stable release is :- ",stable_rel_one
            else:
                print "No stable release found"
            ################################
                platform=data[18]
                if(platform):
                    print "Tageted platform is :- ",platform
                if(type1):
                    like_quer=""
                    type1_split=type1.split()
                    if(type1_split>1):
                        for splt in type1_split:
                            like_quer=like_quer+" type like '%"+splt+"%' and "
                        #print type1_split
                        #print "similar apps :- ",type1
                        q_sim="select * from master where "+like_quer
                        q_sim=q_sim[:-4]+" ;"
                    else:
                        #print "len one"
                        q="select * from master where "+"type like '%"+type1_split+"%';"

                    #print q_sim
                    cur.execute(q_sim)
                    data_sim = cur.fetchall()
                    res_sim_len=len(data_sim)
                    print "I would like to recommend following products:- "
                    if(res_sim_len):
                        count_sim=0
                        for x in data_sim:
                            count_sim=count_sim+1
                            rec_version=x[17]
                            if(count_sim>5):
                                break
                            if(rec_version):
                                rec_ver_split=rec_version.split("/")
                                rec_ver_split=rec_ver_split[0]
                                rec_ver_split=rec_ver_split.replace("[b1]","")
                                rec_ver_split=rec_ver_split.replace("[b2]","")                                    
                                print x[16]," Stable Release ",rec_ver_split
                            else:
                                print x[16]            
            ################################

        if(res_len>1 and res_len!=0):
            
            #print "Do you mean:- "
            count=0
            print "i have more results please use proper keywords"
            count=0
            for x in data:
                
                str_x=str(x[1]).replace("_"," ")
                print str(count)," ",str_x[5:] #5: is to remove wiki
                count=count+1
                if(count>15):
                    break
            print " reply the number you wish to know information about."
            
            ret_q=raw_input()
            
            
            print "ret_q >>>",ret_q,"-",len(data)
            list1=[]
            max1=0
            if(len(data)<15):
                max1=len(data)
            else:
                max1=16

            for x in range(0,max1):
                list1.append(str(x))
            print list1

            while(True):
                if(ret_q not in list1):
                    print "Invalid Input Try again. Press q or e to exit"
                
                    
                if(ret_q in list1):
                    data_val=data[int(ret_q)]
                    stable_rel=data_val[17]
                    type1=data_val[14]
                    print type1
                    if(stable_rel):
                        print "Stable release is :- ",stable_rel
                    else:
                        print "No stable release found"

                    if(type1):
                        like_quer=""
                        type1_split=type1.split()
                        if(type1_split>1):
                            for splt in type1_split:
                                like_quer=like_quer+" type like '%"+splt+"%' and "
                            #print type1_split
                            #print "similar apps :- ",type1
                            q_sim="select * from master where "+like_quer
                            q_sim=q_sim[:-4]+" ;"
                        else:
                            q_sim="select * from master where "+"type like '%"+type1_split+"%';"

                        cur.execute(q_sim)
                        data_sim = cur.fetchall()
                        res_sim_len=len(data_sim)
                        print "I would like to recommend following products:- "
                        if(res_sim_len):
                            count_sim=0
                            for x in data_sim:
                                count_sim=count_sim+1
                                rec_version=x[17]
                                if(count_sim>5):
                                    break
                                if(rec_version):
                                    rec_ver_split=rec_version.split("/")
                                    rec_ver_split=rec_ver_split[0]
                                    rec_ver_split=rec_ver_split.replace("[b1]","")
                                    rec_ver_split=rec_ver_split.replace("[b2]","")                                    
                                    print x[16]," Stable Release ",rec_ver_split
                                else:
                                    print x[16]

                            
                     
                    break
                elif(ret_q=='q' or ret_q=='e'):
                    print ""
                    break
                else:
                    print "you have not entered a valid input please enter valid input or q,e to exit"
                    ret_q=raw_input()
                    print ret_q
                    if (int(ret_q)>len(data)):
                        print " invalid input try again"
                        break
                    
                if(ret_q =='e' or ret_q=='q'):
                    break
                
                ret_q=raw_input()        
    except lite.Error, e:            
        print "Error %s:" % e.args[0]
        #sys.exit

    con.commit()
    con.close()



##print wiki_final("wiki")







