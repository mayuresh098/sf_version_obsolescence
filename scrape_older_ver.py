# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
from bs4 import BeautifulSoup
import unidecode
import sqlite3
import re
import csv
import wikipedia
import requests
import re
import csv
import time
import datetime
import csv
import time
import datetime

ts = time.time()
from bs4 import BeautifulSoup
#

pages=['http://www.oldversion.com/windows/software/utilities/']

pages=['http://www.oldversion.com/windows/software/file-sharing/','http://www.oldversion.com/android/software/n-a/','http://www.oldversion.com/android/software/business/',
       'http://www.oldversion.com/android/software/comics/','http://www.oldversion.com/android/software/communication/','http://www.oldversion.com/android/software/health-fitness/',
       'http://www.oldversion.com/android/software/finance/','http://www.oldversion.com/android/software/news-magazines/',
       'http://www.oldversion.com/android/software/personalization/','http://www.oldversion.com/android/software/photography/',
       'http://www.oldversion.com/android/software/productivity/','http://www.oldversion.com/android/software/tools/',
       'http://www.oldversion.com/android/software/social/','http://www.oldversion.com/android/software/sports/',
       'http://www.oldversion.com/android/software/social/','http://www.oldversion.com/android/software/shopping/',
       'http://www.oldversion.com/android/software/transportation/','http://www.oldversion.com/android/software/travel-local/',
       'http://www.oldversion.com/android/software/weather/','http://www.oldversion.com/linux/software/utilities/',
       'http://www.oldversion.com/linux/software/security/','http://www.oldversion.com/linux/software/graphics/','http://www.oldversion.com/linux/software/ftp/',
       'http://www.oldversion.com/linux/software/drivers/','http://www.oldversion.com/linux/software/communication/','http://www.oldversion.com/linux/software/internet/'
       ,'http://www.oldversion.com/linux/software/multimedia/','http://www.oldversion.com/windows/software/drivers/','http://www.oldversion.com/windows/software/development/'
       ,'http://www.oldversion.com/windows/software/communication/','http://www.oldversion.com/windows/software/ftp/','http://www.oldversion.com/windows/software/graphics/',
       'http://www.oldversion.com/windows/software/internet/','http://www.oldversion.com/windows/software/multimedia/','http://www.oldversion.com/windows/software/networking/'
       ,'http://www.oldversion.com/windows/software/office/','http://www.oldversion.com/windows/software/security/','http://www.oldversion.com/windows/software/utilities/',
       'http://www.oldversion.com/mac/software/file-sharing/','http://www.oldversion.com/mac/software/drivers/','http://www.oldversion.com/mac/software/development/'
       ,'http://www.oldversion.com/mac/software/communication/','http://www.oldversion.com/mac/software/ftp/','http://www.oldversion.com/mac/software/graphics/',
       'http://www.oldversion.com/mac/software/internet/','http://www.oldversion.com/mac/software/multimedia/','http://www.oldversion.com/mac/software/networking/',
       'http://www.oldversion.com/mac/software/office/','http://www.oldversion.com/mac/software/security/','http://www.oldversion.com/mac/software/utilities/',
       'http://www.oldversion.com/games/software/strategy/','http://www.oldversion.com/games/software/simulation/','http://www.oldversion.com/games/software/rpg/',
       'http://www.oldversion.com/games/software/puzzle/','http://www.oldversion.com/games/software/platform/','http://www.oldversion.com/games/software/arcade/',
       'http://www.oldversion.com/games/software/adventure/','http://www.oldversion.com/games/software/action/']

conn = sqlite3.connect('master_oldversion.db')
c = conn.cursor()
#print pages
p_count=0
for p  in pages:
    print p
    try:
        
        p_count=p_count+1
        page_no="?page="
        for l in range(1,40):
            
            print p+page_no+str(l)
            soup = BeautifulSoup(requests.get(p+page_no+str(l)).content, "html.parser")
            div = soup.find('div', id='container')
            find_error= (div.text)
            #print find_error
            a=find_error.find('The server returned a "500 Internal Server Error"')
            b=find_error.find("Server Error")
            print a,b
            if( a!=-1):
                print "error in ",str(p),"<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
                break
            else:
                print "no error ",str(p),">>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                # parse the  div id ="all"
                
                print "############################################"
              
            div1=soup.find('div', id='all')
            #print dir(div1)
            children = div1.findChildren()
            for child in children:
                #print type(child),dir(child)
                #print child
                all_div=child.find_all(('div',{'class':'heading2'}))
                all_div=str(all_div)
                soup1 = BeautifulSoup(all_div, "html.parser")
                dict1=dict()
                for link in soup1.findAll('a',rel='nofollow'):
                    #############################################visiting
                    inn_url="http://www.oldversion.com"+link['href']
                    print "going to the site------------------- ",inn_url
                    
                    soup2 = BeautifulSoup(requests.get(inn_url).content, 'html.parser') # Parse the HTML as a string
    ##                print soup2
                    table = soup2.find_all('table',{'class':'table1'})[0] # Grab the first table
                    new_table = pd.DataFrame(columns=range(0,3), index = [0]) # I know the size
                    row_marker = 0
                    
                    for row in table.find_all('tr'):
                        columns = row.find_all('td')
                        #print columns
                        k=row.find_all('td',{'class':'version'})
                        v= row.find_all('td',{'class':'rdate'})
                        
                        for i in range(0,len(k)):
                            #print k[i].get_text().encode('"utf-8"'),v[i].get_text().encode('"utf-8"')

                            k1=k[i].get_text()
                            #k1=k1.encode('"utf-8"')
                            #k1=k1.replace('Â','')
                            k1 = unidecode.unidecode(k1)
                            
                            v1=v[i].get_text()
                            v1 = unidecode.unidecode(v1)
                            #v1=v1.encode('"utf-8"')
                            #v1=v1.replace('Â','')
                            
                            if(v1==" Add info"):
                                v1=""
                                
                            #print k1,v1
                            dict1[k1]=v1
                            
                    str_dict1=str(dict1)
                    str_dict1=str_dict1.replace("'","!")
                    #print str_dict1
                    desc = soup2.find_all('div',{'class':'description'})[0]
                    

                    if(desc):
                        desc= desc.get_text()
                        desc= unidecode.unidecode(desc)
                        desc=desc.replace("'","")
                    else:
                        desc=""
                    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            
                    ins_q="insert into master3 (id,url,name,desc,version,date_parsed,'url2')values('"+str(p_count)+"','"+str(p)+"','"+str(l)+"','"+desc+"','"+str_dict1+"','"+str(timestamp)+"','"+str(inn_url)+"')"
                    #print ins_q
                    dict1={}
                    try: 
                        c.execute(ins_q)
                        print "row inserted"
                        conn.commit()
                    except  Exception as ein:
                        print "errreor found at ",str(ein)
                        pass
    except Exception as e:
        print "error found breaking",str(e)
        print "***********************************************************"
        print "#######################################################"

conn.close()
























































        
            

##                    count_col=0
##                    col_val=""
##                    for column in columns:
##                        print type(column),dir(column)
##                        for c in column.findChildren():
##                            print c
##                        k=column.findChild('td',{'class':'version'}).get_text().encode('"utf-8"')
##                        v= column.findChild('td',{'class':'rdate'}).get_text().encode('"utf-8"')
##                        print k,"-",v
##                        if(v!="Add info"):
##                            dict1[k]=""
##                        else:
##                            dict1[k]=v
##                        if(count_col==0):
##                            dict1[column.get_text()]=""
##                            col_val=column.get_text()
##                        count_col=count_col+1
##                        if(count_col==1):
##                            val_col=column.get_text()
##                            if (val_col=="Add info"):
##                                val_col=" "
##                            else:
##                                dict1[col_val]=val_col
                
 





  #print dir(div1)
'''['HTML_FORMATTERS', 'XML_FORMATTERS', '__call__', '__class__', '__contains__', '__copy__', '__delattr__', '__delitem__', '__dict__',
'__doc__', '__eq__', '__format__', '__getattr__', '__getattribute__', '__getitem__', '__hash__', '__init__', '__iter__', '__len__', '__module__', '__ne__',
'__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__',
'__weakref__', '_all_strings', '_attr_value_as_string', '_attribute_checker', '_find_all', '_find_one', '_formatter_for_name', '_is_xml', '_lastRecursiveChild',
'_last_descendant', '_select_debug', '_selector_combinators', '_should_pretty_print', '_tag_name_matches_and', 'append', 'attribselect_re', 'attrs', 'can_be_empty_element',
'childGenerator', 'children', 'clear', 'contents', 'decode', 'decode_contents', 'decompose', 'descendants', 'encode', 'encode_contents', 'extract', 'fetchNextSiblings',
'fetchParents', 'fetchPrevious', 'fetchPreviousSiblings', 'find', 'findAll', 'findAllNext', 'findAllPrevious', 'findChild', 'findChildren', 'findNext', 'findNextSibling',
'findNextSiblings', 'findParent', 'findParents', 'findPrevious', 'findPreviousSibling', 'findPreviousSiblings', 'find_all', 'find_all_next', 'find_all_previous', 'find_next',
'find_next_sibling', 'find_next_siblings', 'find_parent', 'find_parents', 'find_previous', 'find_previous_sibling', 'find_previous_siblings', 'format_string', 'get', 'getText',
'get_text', 'has_attr', 'has_key', 'hidden', 'index', 'insert', 'insert_after', 'insert_before', 'isSelfClosing', 'is_empty_element', 'known_xml', 'name', 'namespace',
'next', 'nextGenerator', 'nextSibling', 'nextSiblingGenerator', 'next_element', 'next_elements', 'next_sibling', 'next_siblings', 'parent', 'parentGenerator', 'parents',
'parserClass', 'parser_class', 'prefix', 'preserve_whitespace_tags', 'prettify', 'previous', 'previousGenerator', 'previousSibling', 'previousSiblingGenerator',
'previous_element', 'previous_elements', 'previous_sibling', 'previous_siblings', 'quoted_colon', 'recursiveChildGenerator', 'renderContents', 'replaceWith',
'replaceWithChildren', 'replace_with', 'replace_with_children', 'select', 'select_one', 'setup', 'string', 'strings', 'stripped_strings', 'tag_name_re', 'text', 'unwrap', 'wrap']
'''

