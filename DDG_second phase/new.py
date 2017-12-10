import requests
from lxml import html
import time
import csv
#Agency,Application name,Primary domain,Number of users,Number of licenses,Number of government support staff,Number of contractors,
#Start of use date,End of use date,is-custom,is-service,Manufacturer,Product/service name,Estimated replacement cost
###################################################################################################################################

def search(keywords, max_results=None):
	url = 'https://duckduckgo.com/html/'
	params = {
		'q': keywords,
		's': '0',
	}

	yielded = 0
	while True:
		res = requests.post(url, data=params)
		doc = html.fromstring(res.text)

		results = [a.get('href') for a in doc.cssselect('#links .links_main a')]
		for result in results:
			yield result
			time.sleep(0.1)
			yielded += 1
			if max_results and yielded >= max_results:
				return

		try:
			form = doc.cssselect('.results_links_more form')[-1]
		except IndexError:
			return
		params = dict(form.fields)
######################################################################################
		

with open('app.csv') as csvfile:

    reader = csv.DictReader(csvfile)
    for row in reader:
        app_name=row['Application name']
        manu_name=row['Manufacturer']
        print app_name,manu_name
    
        ###########################query 1
        print ("#############query1##########")
        q1=app_name
        links=search(q1,4)
        for l in links:
            print l
        ############################query 2
            print ("#############query2##########")
        q2=manu_name+":"+app_name
        links=search(q2,4)
        for l in links:
            print l
        ############################query3
        print ("#############query3##########")
        q3=app_name +str("version")
        links=search(q3,4)
        for l in links:
            print l
        















        
