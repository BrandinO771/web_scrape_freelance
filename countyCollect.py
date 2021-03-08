from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import os
import csv

##################################################################
# DEV NOTES: 
##################################################################
# -SUMMARY-
# THIS WAS FOR AN UPWORK PROPOSAL WHERE THE CLIENT WANTED TO SCRAPE REAL ESTATE PARCEL INFORMATION BY COUNTY, THIS COUNTY HAD
# A PRETTY OPEN WEBSITE WHICH ALLOW FOR SEARCHING WITH A WILDCARD CHARACTER TO RETURN ALL PARCEL RESULTS, YET THEY PLACED LIMITATIONS ON 
# PAGE VIEW PER MINUTE (15) AND PER TOKEN USAGE WHICH I ESTIMATE WAS 150 - 300 PAGE VIEWS, PLUS  HUMAN OR BOT VERIFICATION WALLS. 
# ULTIMATELY THIS JOB WAS UNFEASABLE FOR ONE COMPUTER FOR COUNTYS ANY LARGER AS THEY WOULD HAVE 250K ENTRIES AT 15 PAGE VIEW PER MINUTE 
# WOULD HAVE TAKEN MORE TIME THAN POSSIBLE WITHOUT A MULTI BOT APPROACH OFFERED BY LARGER WEB SCRAPE COMPANIES   

#-ABOUT THE CODE-
# IT TOOK ME ABOUT [ 27 HOURS  OR 1.2 WEEKS PART TIME] TO COMPLETE THIS SCRIPT, THERE WAS AN UNCONVENTIONAL LAYOUT TO EACH HTML PAGE
# THE WEB DEVELOPER MADE SOME INTERESTING CHOICES IN POPULATING CONTENT, WHICH LED TO MANY UNIQUE ALGORITHMS TO FIND, AND UNPACK THE DATA,
# IN THESE CASES BEAUTIFUL SOUP WAS ABLE TO GET ME CLOSE BUT THEN CUSTOM ALGORITHMS WERE NEEDED TO GO ALL THE WAY!
# DO TO NATURE OF THE WORK I DESIGNED THE SCRAPPING FUNCTION IN A WHILE LOOP BELOW , 
# EACH STATE BELOW FOR EACH CATEGORY UNPACK PER PAGE, IE,  GENRAL_INFO, BUILDING_DESCRIPTION, ROOMS, BASEMENT....

# MESSAGE FROM THE  SERVER OVERLORDS AFTER PER PAGE COUNT EXCEEDED :
# "If you think this page is in error, please call tech support at .....Appraisals at ...-...-....   or email support@......com"

# BELOW I KEPT TRACK OF MY HOURS: 
# FRIDAY WAS 3 HOURS : 3
# MONDAY WAS 2 HOURS      : 2
# TUESDAY WAS 5-6 HOURS     :5 
# WED WAS 11:00 - 5:30  (HOUR LUNCH) 5.5
# THUR  11:00 -5:00 1hr lunch  5
# FRI  10:30 - 3:00 no lunch   5.5
# Sat 30 min 
# Mon 2 hour  


# LIMITATION : 
  # A BROWSER WINDOW OR TOKEN WILL ONLY ALLOW 300 PAGE VISITS 
  # SO FOR EVERY 250 PAGE VIEWS RESET THE TOKEN AND START OVER>?

def doThatScrape(url, browser, record_number):
    soup = ''
    browser.visit(url)
    time.sleep(2.5)
    html = browser.html
    soup = bs(html, "html.parser")
    counter = 0
    state = -5
    final_list = []
    final_header =[]


    # '======================================================'
    while ( state < 99 ) :
        temp1=[]
        temp2=[]
        temp3=[]
        temp4=[]
        generalInfo=[]
        header_label = ''
        headtemp1 =[]
        headtemp2 =[] 
        labeltemp1=[]
        labeltemp2=[]
        tax_dist = False


    #NOTES WE HAVE TO ACCOUNT FOR UP TO 3 ADDITIONS : AND IF PARCEL DOES NOT HAVE 
    #OCCUPANCY DETAIL WE NEED TO FILL ALL THE FINAL LIST WITH  "N/A" OR   "DATA_NOT_REPORTED"

    ##############################################
    ##   SET SCRAPE CRITERIA
    ##############################################

        ################################################
        ### THESE GENERATE PLUG DATA WHEN MISSING  #####
        def na_generator( na_data_count ):
            fdata=[]
            for num in range(int(na_data_count)):
                fdata.append("NA")
            return fdata


        if state == -5 : # ADD LINK TO SOURCE PAGE
            final_list.append(record_number)
            final_list.append(url)
            state = -4


        if state == -4 : # IMAGE LINK:
            temp1 = soup.find('div', class_='ad-image')
            if(  temp1 is not None  and temp1 != []):
                temp2 = temp1.find('img')
                if(  temp2 is not None  and temp2 != []):
                    final_header.append("Lot_Image")
                    image_link = temp2.get('src')
                    final_link = 'http:'+str(image_link)
                    final_list.append(final_link)

            if( temp1 is None ) :
                final_list.append("No_Image_Availabe")

            temp1=[]; temp2=[]
            state = -3


        if state == -3 : # MAP LINK:
       
            temp1 = soup.find('div', id='pclGeneralInfo')
            temp2 = temp1.find_all('td')
            map_found = False

            for m in temp2 :

                temp3 = m.find('a', href=True)
                if( temp3 is not None  and temp3 != []):
                    
                    temp3=str(temp3)
                    temp3=temp3.split('<a href=')
                    temp4=temp3[1].split('"')
                    final_list.append(temp4[1])
                    map_found = True
                    break

            if map_found == False :  final_list.append('No_Map_Link_Avail')

            temp1=[]; temp2=[]; temp3=[]; temp4=[]
      
            state = 0


        if state == 0 : # GENERAL INFO
            temp1 = soup.find('div', id='pclGeneralInfo')
            temp3 = temp1.find_all('td')
            state = 20


        if state == 1 : # TAXING DISTRICTS 
            temp1 = soup.find('div', class_='taxdist')
            temp3 = temp1.find_all('td')
            state = 20


        if state == 2 : # CURR VALUE INFO
            temp1 = soup.find_all('div', class_='MOcolumns')
            state = 22


        if state == 3 : # LAND / LOTS 
            temp1 = soup.find('div', class_='land')

            if(  temp1 is not None  and temp1 != []):
                state = 23
            else :
                final_list  +=na_generator(9)
                state = 40


        if state == 4 : # RESIDENTIAL DATA 4 data pts 
            temp1 = soup.find('div', class_='residentialData')
            if (  temp1 is not None  and temp1 != []):
                state = 24
            else :  final_list+=na_generator(4);    state = 40


        if state == 5 : # STRUCTURE 
            temp1 = soup.find('div', id="structure")
            if (  temp1 is not None  and temp1 != []):
                temp2 = temp1.find('div', class_='r_header')
                header_label = temp2.text
                temp3 = temp1.find_all('div', class_='r_label')
                temp4 = temp1.find_all('div', class_='r_data')
                state = 25

            else :  final_list+=na_generator(10);   state = 40

        
        if state == 6 : # ROOMS 
            temp1 = soup.find('div', id="rmCount")
            if (  temp1 is not None  and temp1 != []):
                temp2 = temp1.find('div', class_='r_header')
                header_label = temp2.text
                temp3 = temp1.find_all('div', class_='r_labelrb')
                temp4 = temp1.find_all('div', class_='r_datarb')
                state = 25

            else :  final_list+=na_generator(4);   state = 40


        if state == 7 :  # BUILDING DESCRIPTIONS 
            temp1 = soup.find('div', id="bldgDesc")
            if (  temp1 is not None  and temp1 != []):
                temp2 = temp1.find('div', class_='r_header')
                header_label = temp2.text
                temp3 = temp1.find_all('div', class_='r_labelrb')
                temp4 = temp1.find_all('div', class_='r_datarb')
                state = 25

            else :  final_list+=na_generator(7);   state = 40


        if state == 8 :  #BASEMENT 
            temp1 = soup.find('div', id="bsmtFin")
            if (  temp1 is not None  and temp1 != [] ):
                temp2 = temp1.find('div', class_='r_header')
                header_label = temp2.text
                temp3 = temp1.find_all('th')
                temp4 = temp1.find_all('td')
                state = 25

            else :  final_list+=na_generator(4);   state = 40


        if state == 9 :  #PlUMBING
            temp1 = soup.find('div', id="plumbing")
            if (  temp1 is not None  and temp1 != [] ): 
                temp2 = temp1.find('div', class_='r_header')
                header_label = temp2.text
                state = 26

            else :  final_list+=na_generator(2);   state = 40


        if state == 10 :  #PORCHES 
            temp1 = soup.find_all('div', id="porches", class_="mobileShow")
            if (  temp1 is not None  and temp1 != [] ):
                state = 27

            else :  final_list+=na_generator(12);   state = 40


        if state == 11 : #DECK
            temp1 = soup.find('div', class_='decks_ven')
            # print('state', state , 'temp1', temp1)
            
            if (  temp1 is not None  and temp1 != [] ):
                state = 28   

            else :  final_list+=na_generator(6);   state = 40
    

        if state == 12 : #ADDITIONS 
            temp1 = soup.find_all('div', class_='addn_garages')
            if (  temp1 is not None  and temp1 != []):
                state = 29  

            else :  final_list+=na_generator(27);   state = 40


        if state == 13 : #SALES 
            temp1 = soup.find_all('div', class_='generalSale')
            if (  temp1 is not None  and temp1 != []):
                state = 30          

            else :  final_list+=na_generator(20);   state = 40


    #####################################################
    ##    U N P A C K                                  ##
    #####################################################
        if state == 20 : # TAXING DISTRICTS

            for data_a in temp3 :
                generalInfo.append(data_a.text) 
            state = 21


        if state == 21 : # CONTINUE ETL TAXING DIST ABOVE
            dataText =''
            tempList =[]
            tempList1 =[]
            incrmt = 0
            temp_parcels=[]

            for items in generalInfo :
                tempList = items.split()
                for x in tempList :
                    dataText +=x + ' '
                tempList1.append(dataText) #DO NOT INDENT THESE UNDER SECOND FOR WE ARE BUILDING A STRING FROM ALL LINE ELEMENTS
                dataText =''

            # if ( tax_dist == false ):
            for i in tempList1 :

                if ( 'Map this address' in i ) :
                    i = i.replace( 'Map this address', '')
                if i == '':
                    i = 'NA'

                incrmt +=1

                if counter == 0  :
                    if ( ":" not in i ) :
                        temp_parcels.append(i)

                if counter == 1  :
                    if ( incrmt % 2 == 0 ) :
                        final_list.append(i)

            if counter == 0  : # some parcels have an extra field for Deed Holder - we want to look for and eliminate
                if( len ( temp_parcels) > 15 ) : 
                    temp_parcels[1] = temp_parcels[1] + ' ' + temp_parcels[2]
                    del temp_parcels[2]

                final_list += temp_parcels

            state = 40


        if state == 22 :# CURR VALUE INFO

            for  t in temp1  :
                t_text = str(t) 
                if ( "$" in t_text ) :
                    final_list.append(t.text)

            state = 40


        if state == 23 : # LAND - LIMIT 3
            temp2 = temp1.find_all('th')
            temp3 = temp1.find_all('td')

            lot_data_ct = 0

            for q in temp3 : ## make me headers for each td 
                if( lot_data_ct < 9 ):
                    final_list.append(q.text)
                lot_data_ct+=1

            if ( lot_data_ct < 9):
                final_list  +=na_generator((9 - lot_data_ct))

            state = 40    


        if state == 24 :  # RESIDENTIAL DATA
            temp2 = temp1.find_all('div', class_='resColumn1')# DATA IS SPLIT THESE 2 CLASSES 
            temp3 = temp1.find_all('div', class_='resColumn2')

            for p in temp2 :
                final_list.append(p.text)
            
            for t in temp3 :
                final_list.append(t.text)
    
            state = 40       


        if state == 25 : # STRUCTURE - #ROOMS - #BUILDING DESCRIPTIONS 16 data pts 
            # WHEN WE GET TO FIRST TABLE IN THIS SECTION : Building ELIMINATE EXTRA FIELDS : Length - Width

            build_temp=[]

            if ( counter > 5 ):
                for x in temp4 :
                    final_list.append(x.text)

            if ( counter == 5):

                for z in temp4 :
                    build_temp.append(z.text)

                if ( len(build_temp) > 10 ) :
                    del build_temp[5:7] # remove positions 5 & 6 and pop the last 2 

                final_list += build_temp ## do not indent further right

            state = 40       


        if state == 26 :  # Plumbing 

            headtemp1 =[]
            headtemp2 =[] 
            labeltemp1=[]
            labeltemp2=[] 

            labeltemp1 = temp1.find_all('div', class_='r_rowdatapa')# DATA IS SPLIT THESE 2 CLASSES
            labeltemp2 = temp1.find_all('div', class_='r_rowdatapa1')# DATA IS SPLIT THESE 2 CLASSES
            labeltemp1 += labeltemp2
        
            for datas in labeltemp1 :
                final_list.append(datas.text)
    
            state = 40  


        if state == 27 :   # PORCHES UNPACK LIMIT 3 PORCHES EACH PORCH GRP IS 6 DATA PTS 
            porch_ct = 0

            for x in temp1 : # HERE WE CAN RECEIVE MULTI DIV CONTAINERS WITH IDENTICAL CLASSES SO ITERATE THROUGH THEM
                porch_ct+=1
                labeltemp1 = x.find_all('div', class_='r_datag')

                if ( porch_ct < 3):
                        
                    for datas in labeltemp1 :
                        final_list.append(datas.text)

            
            porches_data_missing = 0
            porches_data_missing = ((2 - porch_ct) * 6)
     
            if ( porch_ct < 2 ):
                final_list+=na_generator(porches_data_missing)
            state = 40


        if state == 28 : # DECKS  LIMIT 3, EACH HAS 2 DATA POINTS 
            headtemp1 =[]
            headtemp2 =[] 
            labeltemp1=[]
            labeltemp2=[]
            labeltemp3=[]

            num_of_decks=0
            # NEED TO INTERLACE THESE LIST X Y X Y THEY ARE NOW XX YY
            labeltemp1 = temp1.find_all('div', class_='r_rowdatadv')
            labeltemp2 = temp1.find_all('div', class_='r_rowdatadv1')
            labeltemp3 += labeltemp1
            labeltemp3 += labeltemp2

            num_data_pts = len(labeltemp1)

            for i in range(num_data_pts):
                final_list.append(labeltemp1[i].text)   
                final_list.append(labeltemp2[i].text)    

            num_of_decks = int(len(labeltemp3)/2)
            
            if (num_of_decks < 3 ):
                missing_decks = (3-num_of_decks)*2
                final_list+=na_generator(missing_decks)  
            
            state = 40
            

        if state == 29 : # ADDITIONS # LIMIT 3 ADDITIONS : EACH GRP IS 9 DATA POINTS 

            reno_counter=0
            missing_renos=0
            garage_list   =['NA','NA','NA','NA','NA','NA','NA','NA','NA' ]
            addition1_list=['NA','NA','NA','NA','NA','NA','NA','NA','NA' ]
            addition2_list =['NA','NA','NA','NA','NA','NA','NA','NA','NA' ]

            for x in temp1 : # HERE WE CAN RECEIVE MULTI DIV CONTAINERS WITH IDENTICAL CLASSES SO ITERATE THROUGH THEM
                headtemp1  = x.find_all('div', class_='r_labelg')
                labeltemp1 = x.find_all('div', class_='r_datag')
                temp2      = x.find('div', class_='r_header')
                header_label = temp2.text
                category_split = header_label.split()

                if (category_split[0] == 'Garage' ):
                    garage_list=[]
                    for datas in labeltemp1 :
                        garage_list.append(datas.text)
                        reno_counter+=1

                if (category_split[0] == 'Addition' and category_split[1] == '1'):
                    addition1_list=[]
                    for datas in labeltemp1 :
                        addition1_list.append(datas.text)
                        reno_counter+=1

                if (category_split[0] == 'Addition' and category_split[1] == '2'):
                    addition2_list=[]
                    for datas in labeltemp1 :
                        addition2_list.append(datas.text)
                        reno_counter+=1

            final_list += garage_list
            final_list += addition1_list
            final_list += addition2_list
            
            state = 40
            
    # THIS HAS 4 SALES 
        if state == 30: # SALES  LIMIT 4 SALES  EACH 5 DATA POINTS 
            sales_ct = 1
            missing_sales = 0
            for x in temp1 : # HERE WE CAN RECEIVE MULTI DIV CONTAINERS WITH IDENTICAL CLASSES SO ITERATE THROUGH THEM
                headtemp1  = x.find_all('div', class_='sls_label')
                labeltemp1 = x.find_all('div', class_='sls_data')
                    
                for datas in labeltemp1 :
                    if ( datas.text != '') :
                        final_list.append(datas.text)
                    else:
                        final_list.append('NA')

                sales_ct+=1

            if ( int(sales_ct) < 5 ) : 
                missing_sales = 25 - ( 5 * sales_ct)
                final_list+=na_generator(missing_sales) 

            state = 40
                    

        ##############################################
        ##-- ROUTE TO TOP OR FINISH     
        ##############################################
        if state == 40 :
            counter+=1
            # record_number+=1
            if counter < 14: 
                state = counter 
        
            if counter == 14 :
                state = 50
            # print('++++++++++++++++ header list ++++++++++++++++++', tempList)  
            # print('++++++++++++++++ header list ++++++++++++++++++', final_header)  
            # print('++++++++++++++++ final list  ++++++++++++++++++', final_list )  
            # print('state', state, 'counter', counter, 'the url' , url)
        ##############################################




        if state == 50 : 
            # browser.quit()
            print('the record', record_number,  'the url' , url)
            print()
            print('++++++++++++++++ final list  ++++++++++++++++++', final_list )  
            # time.sleep(1)
            state = 100
            return final_list










