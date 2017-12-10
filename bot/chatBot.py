#!/usr/bin/python

import time
from  PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
import sys

import sqlite3 as lite
import csv
import sys
from random import *
 
 

try:
    import aiml
except ImportError:
    print "Error importing PyAIML module."
    exit()
##################################################################3

con = lite.connect('final_master_modified.db')
cur = con.cursor()

list_notfound=['I am not able to find any such information', 'I can not find anything on the subject.','sorry i dont have such information now, Please try again Later','No such info found ']


def def_ret_bot(string):
    return QString("""<style>
                                    .cll{background-color: #fffbea;color: #000000;float: right;font-family: Trebuchet; font-size: 15px;margin-left:60px;font-weight: lighter;text-align: right; }
                                   .time{font-size: 11px ;vertical-align:bottom;color: #999999;}
                                   </style>  
                               <table  class="cll">
                               <tr>
                                    <td>
                                        Bot: """+string+""" <td class="time" > """+time.strftime('%I:%M %p' )+"""</td>           </td>
                               </tr>
                                 </table>
        <table><tr>
    <td><br><br></td></tr></table>""")

class chatBot(QDialog):

    def __init__(self, parent = None):
        super(chatBot, self).__init__(parent)
        self.browser = QTextBrowser()
        self.infield = QLineEdit()
        self.button =  QPushButton("Send");
        
        self.button.setFixedWidth(110)
        self.infield.selectAll()
        
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.infield)
        layout.addWidget(self.button)
        
        self.setLayout(layout)
        self.infield.setFocus()
        self.connect(self.infield, SIGNAL("returnPressed()"), self.updateUi)
        self.setWindowTitle("Chat Bot")
        self.setObjectName("chat_window")
        self.resize(1000, 700)
        self.setMinimumSize(QtCore.QSize(800, 600))
        self.setMaximumSize(QtCore.QSize(900, 900))
        self.browser.setHtml("""     <!DOCTYPE html>
                                <html>
                                <style>
                                body {
                               background-color: #E2F3DB;
                                }
                                </style>
                                <body></body>
                                </html>
                                """)
        self.setGeometry(QtCore.QRect(400, 200,419, 420))

        self.block_brain=0
        
    def updateUi(self):
        text = unicode(self.infield.text())
        #self.browser.setLayoutDirection(QtCore.Qt.RightToLeft)
        #textString = QString("<span style='color:red'> Me %s </span>" %text)
        
        textString = QString("""<style>
                                .container {background-color: #F0F9ED;width: 100%;color: #000000;float: left;margin-right:40px;font-family:Trebuchet;font-size: 15px ;
                                font-weight: lighter;text-align: left; }
                           .time{font-size: 11px ;vertical-align:bottom;color: #999999;}
                           </style>
                    <table  class="container">
                       <tr>
                        <td>
                         Me :  """+text+""" <td class="time" >"""+time.strftime('%I:%M %p' )+"""</td>
                        </td>
                       </tr>   
                    </table>
                    <table><tr><td><br></td></tr></table>""")
        self.browser.append(textString)
        
        ######################Catching the ctach phrase##################

        if((text[:4]=="scan")):
            
            print "text",text
            print self.block_brain
            self.block_brain=1
            #print text
            print self.block_brain
            self.block_brain=1
            s=text.split(' ', 1)[1]
            #split version 
            print "splitted str is ",s
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
                data = cur.fetchall()
                print "---",len(data)
                res_len=len(data)
                print "re_len",res_len
                if(res_len<=3):
                    count=0
                    for x in data:
                        count=count+1
                        str_x=str(x[1]).replace("_"," ")
                        print str(count)," ",str_x[5:]
                        if(count>15):
                            break
                if(res_len==0):
                    resultString = def_ret_bot(str(list_notfound[randint(0, len(list_notfound)-1)]))

                    self.browser.append(resultString) 

                if(res_len==1):
                    data=data[0]
                    stable_rel_one=data[17]
                    stable_rel_one=stable_rel_one.replace("[b1]","")
                    type1=data[14]
                    print "stable_rel_one",stable_rel_one
                    if(stable_rel_one):
                        #print "Stable release is :- ",stable_rel_one
                        resultString = def_ret_bot("Stable release is :- "+stable_rel_one)
                        self.browser.append(resultString)
                    else:
                        #print "No stable release found"
                        resultString = def_ret_bot("No stable release found")
                        self.browser.append(resultString)
                if(res_len>1 and res_len!=0):
                    #print "Do you mean:- "
                    count=0
                    print "I have more results please use proper keywords"
                    resultString = def_ret_bot("I have more results please use proper keywords")
                    self.browser.append(resultString)
                    count=0
                    str_opt="<br>"
                    for x in data:
                        
                        str_x=str(x[1]).replace("_"," ")
                        str_opt=str_opt+str(count)+" "+str_x[5:]+"<br>" #5: is to remove wiki
                        count=count+1
                        if(count>15):
                            break
                    resultString = def_ret_bot(str_opt)
                    self.browser.append(resultString)
        
                    resultString = def_ret_bot("Reply the number you wish to know information about.")
                    self.browser.append(resultString)

                    list1=[]
                    max1=0
                    if(len(data)<15):
                        max1=len(data)
                    else:
                        max1=16

                    #text = unicode(self.infield.text())
                    ret_q=text
                    print "ret_q====",text

                    for x in range(0,max1):
                        list1.append(str(x))
                    print list1
                    while(True):
                        print ret_q
                        if(ret_q not in list1):
                            #print "Invalid Input Try again. Press q or e to exit"
                            resultString = def_ret_bot("Invalid Input Try again. Press q or e to exit")
                            self.browser.append(resultString)
                        
                            
                        if(ret_q in list1):
                            data_val=data[int(ret_q)]
                            stable_rel=data_val[17]
                            type1=data_val[14]
                            print type1
                            if(stable_rel):
                                print "Stable release is :- ",stable_rel
                                resultString = def_ret_bot("Stable release is :- "+stable_rel)
                                self.browser.append(resultString)
                            else:
                                print "No stable release found"
                                resultString = def_ret_bot("No stable release found")
                                self.browser.append(resultString)
                                

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
                                resultString = def_ret_bot("I would like to recommend following products:- ")
                                self.browser.append(resultString)
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
                            resultString = def_ret_bot("you have not entered a valid input please enter valid input or q,e to exit")
                            self.browser.append(resultString)                            
                            ret_q=raw_input()
                            print ret_q
                            if (int(ret_q)>len(data)):
                                print " invalid input try again"
                                resultString = def_ret_bot(" invalid input try again")
                                self.browser.append(resultString)
                                break
                            
                        if(ret_q =='e' or ret_q=='q'):
                            break
                        
                        ret_q=raw_input() 



                
            except Exception as e:
                print "Error %s:" % e.args[0]
        else:
            result = brain.respond("%s" %text)
            #resultString = QString("<span align='right' style='color:green'> iTSYSTEM  %s</span> " %result)
            resultString = def_ret_bot(result)
            
            self.browser.append(resultString)
            self.infield.clear()

def main():
    app = QApplication(sys.argv)
    bot = chatBot()
    bot.show()
    app.exec_()

if __name__ == '__main__':
    brain = aiml.Kernel()
    brain.learn('brain/std-startup.xml')
    brain.respond("load aiml b")
    main()
