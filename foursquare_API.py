#encoding:UTF-8

#import libraries
import urllib2
import json
import psycopg2
import time

# Connect to an existing database
conn = psycopg2.connect("dbname=<NAME OF THE DB> user=postgres password=")

# Open a cursor to perform database operations
cur = conn.cursor()

#Seattle coordinates xMin,yMin -122.417,47.4851 : xMax,yMax -122.088,47.7395
#Greate a grid and split the Seattle area in small boxes
for nlat in range (0, 260):#nlat =130
    print nlat 
    ne_lat = "%0.10f" % (47.486 + nlat *0.001,) 
    sw_lat ="%0.10f" % (47.485 + nlat *0.001,)
    for nlng in range (0, 330): # nlng = 165
        time.sleep(1)
        ne_lng= "%0.10f" % (-122.415+ nlng *0.001,)
        sw_lng= "%0.10f" % (-122.416 + nlng*0.001,)
        Url = (https://api.foursquare.com/v2/venues/search?ne=%s,%s&sw=%s,%s&client_id=Q12NIQRN3A32J1W1GOC54B1XPCE4Y5LGPDH1U44WXQB5GCAG&client_secret=<CLIENT_SECRET_HERE>&v=20160308&limit=50&intent=browse"%(ne_lat, ne_lng, sw_lat, sw_lng))
        print Url
        try:
		    #call the Foursquare API
            j = json.load(urllib2.urlopen(Url))
        except:
			#wait 60s
            time.sleep(60)
			#Re- call the Foursquare API
            j = json.load(urllib2.urlopen(Url))
        meta_code =  j['meta'].get('code') 
        if meta_code == 200:
            i = 0
            length_ven = len(j['response']['venues'])
            print  'the length of the object venues is', length_ven
            # We now decode the json response
			for i in range (0, length_ven): 
				idfq = j['response']['venues'][i].get('id')
				print idfq, type(idfq)
				name = j['response']['venues'][i].get('name')
				print name
				#contact details
				phone = j['response']['venues'][i]['contact'].get('phone')
				print phone
				formattedPhone = j['response']['venues'][i]['contact'].get('formattedPhone')
				print formattedPhone
				twitter = j['response']['venues'][i]['contact'].get('twitter')
				print twitter
				#location
				address = j['response']['venues'][i]['location'].get('address')
				print address
				crossStreet = j['response']['venues'][i]['location'].get('crossStreet')
				print crossStreet
				lat = j['response']['venues'][i]['location'].get('lat')
				print lat
				lng = j['response']['venues'][i]['location'].get('lng')
				print lng
				distance = j['response']['venues'][i]['location'].get('distance')
				print distance
				postalCode = j['response']['venues'][i]['location'].get('postalCode')
				print postalCode
				city = j['response']['venues'][i]['location'].get('city')
				print city
				state = j['response']['venues'][i]['location'].get('state')
				print state
				country = j['response']['venues'][i]['location'].get('country')
				print country
				cc = j['response']['venues'][i]['location'].get('cc')
				print cc
				# get the cateogory of each place
				if j['response']['venues'][i]['categories'] != []:
					cat_id = j['response']['venues'][i]['categories'][0].get('id')
					print cat_id
					cat_name = j['response']['venues'][i]['categories'][0].get('name')
					print cat_name
					cat_plural_name = j['response']['venues'][i]['categories'][0].get('pluralName')
					print cat_plural_name
					cat_short_name = j['response']['venues'][i]['categories'][0].get('shortName')
					print cat_short_name
					cat_icon_prefix = j['response']['venues'][i]['categories'][0]['icon'].get('prefix')
					print cat_icon_prefix
					cat_icon_suffix = j['response']['venues'][i]['categories'][0]['icon'].get('suffix')
					print cat_icon_suffix
					cat_primary = j['response']['venues'][i]['categories'][0].get('primary')
					print cat_primary
				else:
					cat_id = None
					cat_name = None
					cat_plural_name = None
					cat_short_name = None
					cat_icon_prefix = None
					cat_icon_suffix = None
					cat_primary = None
		
				checkinsCount = j['response']['venues'][i]['stats'].get('checkinsCount')
				print checkinsCount
				usersCount = j['response']['venues'][i]['stats'].get('usersCoun
				print usersCount
				tipCount = j['response']['venues'][i]['stats'].get('tipCount')
				print tipCount
				specials = j['response']['venues'][i]['specials'].get('count')
				print specials
				hereNow_count = j['response']['venues'][i]['hereNow'].get('count')
				print hereNow_count
				print i
				i = i+1
				SQL = "INSERT INTO seattle (idfq, name, phone, formattedPhone,twitter,address,crossStreet,distance, postalCode, city, state, country, cc, cat_id, cat_name, cat_plural_name, cat_short_name, cat_icon_prefix, cat_icon_suffix, cat_primary, checkinsCount, usersCount, tipCount,  specials, hereNow_count,lat, lng, nlat, nlng, length_ven) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s);" # Note: no quotes
				data = (idfq,name, phone, formattedPhone,twitter,address,crossStreet,distance, postalCode, city, state, country, cc, cat_id, cat_name, cat_plural_name, cat_short_name, cat_icon_prefix, cat_icon_suffix, cat_primary, checkinsCount, usersCount, tipCount, specials, hereNow_count,lat, lng, nlat, nlng, length_ven)
				cur.execute(SQL, data)        
				# Make the changes to the database persistent  
				conn.commit()
# Close communication with the database
cur.close()
conn.close()