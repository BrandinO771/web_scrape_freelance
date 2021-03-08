

# THIS IS THE MAIN ROUTER SCRIPT THAT CONTROLS PAGE COUNTS, URL, URL REFRESH, AND CSV WRITTING AND ACCESSES THE
# county COLLECT.PY FILE WHICH DOES THE ACTUAL SCRAPING OF ALL DATA FROM PAGES 



from splinter import Browser
from selenium import webdriver
# from selenium import webdriver as driver

from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time
import os
import csv

import countyCollect as scrape_page




page_scrape_ct =0 # total pages scraped, each page has 20 page links 
scrape_max = 20 # max pages to scrape
scrape_group_ct=0 # batch number calc when to write csv and restart process 
page_num = 58  # current url page containing 20 links
round_trip_ct = 0
temp_query1=[]
temp_query2=[]
temp_query3=[]
final_data=[]
sent_record_num =1021
state = 0
task_done = False
api_key =''
process_initialized = False



print("initializing page number", page_num , 'record_num', sent_record_num)

while ( state < 100  ) :

    print("TOP OF LOOP initializing page number", page_num , 'record_num', sent_record_num, 'the state is :', state )


    if ( state == 0 ):

        def init_browser():
            # NOTES: Replace the path with your actual path to the chromedriver
            executable_path = {"executable_path": "chromedriver.exe"}
            return Browser("chrome", **executable_path, headless=False )
        
        browser = init_browser()
        time.sleep(2)
        process_initialized = True 
        state = 1 


    if ( state == 1 ):

        if ( process_initialized == False   ) : time.sleep(2)
        if ( process_initialized == True    ) : time.sleep(30)
        
        first_site = "http://url_1_is_masked_for_git_publish'
        # '//// INITATION CODE ////'
        browser.visit(first_site)
        time.sleep(3)
        html = browser.html
        soup = bs(html, "html.parser")
        api_search1 = []
        api_search2 = []
        api_search1 = soup.find( "div", id="navButtons")
        api_search2 = api_search1.find_all('a', href=True)
        api_key_split1 = str(api_search2)
        api_key_split2 = api_key_split1.split('ts=')
        api_key_split3 = api_key_split2[2].split('">')

        # print('master_url_text', master_url_text )
        print('api_key_split2', api_key_split2 )
        print('api_key_split3', api_key_split3[0] )
        api_key = str(api_key_split3[0])
        time.sleep(2)

        state = 2

       
    if ( state == 2 ):
        base_page_url1 = 'http://url_2_is_masked_for_git_publish'
        base_page_url2 = '&ts='
        master_url = ''
        page_url =''
        master_parcel_links =[]
        temp_parcel_query=[]
        master_url = base_page_url1 + str(page_num) +  base_page_url2 + api_key

        soup = ''
        browser.visit(master_url)
        time.sleep(2)
        html = browser.html
        soup = bs( html, "html.parser")

        temp_query1 = soup.find_all('tr', class_='even' )

        h_links=[]
        for a in temp_query1 :
            b = a.find('a', href=True)
            if ( b is not None ):
                c= b.get('href')
                h_links.append(c)
        
        temp_query2 = soup.find_all('tr', class_='odd' )
        for a in temp_query2 :
            b = a.find('a', href=True)
            if ( b is not None ):
                c= b.get('href')
                h_links.append(c)

        state = 3


    if ( state == 3 ):

        url1_ = 'http://url_is_masked_for_git_publish'
        counts = 0
        for link in h_links :
            
            temp_data_list = []
            sent_record_num +=1
            temp_data_list = scrape_page.doThatScrape(url1_+link, browser, sent_record_num )
            final_data.append(temp_data_list)
            time.sleep(3.3)

        state = 4


    ##############################################
    ##-- OUTPUT TO CSV :
    ##############################################
    the_headers = ['Record_Num', 'Source_Page', 'Image_Link', 'Map_Link', 'Parcel Number:', 'Deed Holder:', 'Property Address:', 'Mailing Address:', 'Location:', 'Class:', 'Map Area:', 
    'Tax District:', 'Zoning:', 'Subdivision:', 'Sec-Twp-Rng:', 'Lot-Block:', 'Deeded Acres:', 'Legal Description:', 'Land Use:',
    'Ambulance', 'CHB District', 'City', 'County', 'Fire District', 'Health District', 'Master District', 'SB 40 District', 'School District', 
    'Special Road District', 'State', 'Voted Road District', 'Watershed', 'Wheel Tax-Commercial Only', 
    'Full_Market-Agricultural-Land', 'Full_Market-Residential-Land', 'Full_Market-Commercial_Other-Land', 'Full_Market-Exempt-Land', 'Full_Market-Total-Land', 
    'Full_Market-Agricultural-Building', 'Full_Market-Residential-Building', 'Full_Market-Commercial_Other-Building', 'Full_Market-Exempt-Building', 'Full_Market-Total-Building', 
    'Full_Market-Agricultural-Total', 'Full_Market-Residential-Total', 'Full_Market-Commercial_Other-Total', 'Full_Market-Exempt-Total', 
    'Full_Market-Total-Total', 
    'Assessed-Agricultural-Land', 'Assessed-Residential-Land', 'Assessed-Commercial_Other-Land', 'Assessed-Exempt-Land', 
    'Assessed-Land-Total', 'Assessed-Agricultural-Building', 'Assessed-Residential-Building', 'Assessed-Commercial_Other-Building', 
    'Assessed-Exempt-Building', 'Assessed-TotalBuilding', 'Assessed-Agricultural-Total', 'Assessed-Residential-Total', 'Assessed-Commercial_Other-Total', 
    'Assessed-Exempt-Total', 'Assessed-Total-Total', 
    'Lot Type', 'Square Feet', 'Acres',
    'Lot Type', 'Square Feet', 'Acres', 
    'Lot Type', 'Square Feet', 'Acres', 
    'Occupancy', 'Style', 'Year_Built', 'Total_Living_Area', 
    'Building-Occupancy:', 'Building-Year Built:', 'Building-Style:', 'Building-Area:', 'Building-TLA:', 'Building-Condition:', 'Building-Basement:', 
    'Building-Heating:', 'Building-AC:', 'Building-Attic:', 
    'Room Count-Rms Above Ground:', 'Room Count-Rms Below Ground:', 'Room Count-Bedrooms Above:', 
    'Room Count-Bedrooms Below:', 
    'Building Descriptions-Foundation:', 'Building Descriptions-Exterior Walls:', 'Building Descriptions-Roof:', 
    'Building Descriptions-Interior Walls:', 'Building Descriptions-Flooring:', 'Building Descriptions-Architectural Design:', 'Building Descriptions-Single Siding:',
    'Basement Finish-Description','Basement Finish-Area','Basement Finish-Units','Basement Finish-Range', 
    'Plumbing-Style', 'Plumbing-Count', 
    'Porch-1-SF Area:', 'Porch-1-Style:', 'Porch-1-Bsmt SF:', 'Porch-1-Qtrs SF:', 'Porch-1-Qtrs Style:', 'Porch-1-Qtrs AC:', 
    'Porch-2-SF Area:', 'Porch-2-Style:', 'Porch-2-Bsmt SF:', 'Porch-2-Qtrs SF:', 'Porch-2-Qtrs Style:', 'Porch-2-Qtrs AC:', 
    'Deck_Patio_1_Style', 'Deck_Patio_1_SF Area',
    'Deck_Patio_2_Style', 'Deck_Patio_2_SF Area',
    'Deck_Patio_3_Style', 'Deck_Patio_3_SF Area',
    'Garage 1 of 1-Year Built:', 'Garage 1 of 1-Style:', 'Garage 1 of 1-Area:', 'Garage 1 of 1-Condition:', 'Garage 1 of 1-Basement SF:', 'Garage 1 of 1-Qtrs Over Style:', 'Garage 1 of 1-Qtrs Over SF:', 'Garage 1 of 1-Qtrs Over AC (SF):', 'Garage 1 of 1-Door Openers:', 
    'Addition 1 of 2-Year Built:', 'Addition 1 of 2-Style:', 'Addition 1 of 2-Area:', 'Addition 1 of 2-Condition:', 'Addition 1 of 2-Basement SF:', 'Addition 1 of 2-No Floor Adj (SF):', 
    'Addition 1 of 2-Heat:', 'Addition 1 of 2-AC:', 'Addition 1 of 2-Attic SF:', 
    'Addition 2 of 2-Year Built:', 'Addition 2 of 2-Style:', 'Addition 2 of 2-Area:', 'Addition 2 of 2-Condition:', 'Addition 2 of 2-Basement SF:', 'Addition 2 of 2-No Floor Adj (SF):', 'Addition 2 of 2-Heat:', 
    'Addition 2 of 2-AC:', 'Addition 2 of 2-Attic SF:', 
    'Sale-1-Buyer:', 'Sale-1-Seller:', 'Sale-1-Sale Date:', 'Sale-1-Sales Type:', 'Sale-1-Recording:',
    'Sale-2-Buyer:', 'Sale-2-Seller:', 'Sale-2-Sale Date:', 'Sale-2-Sales Type:', 'Sale-2-Recording:',
    'Sale-3-Buyer:', 'Sale-3-Seller:', 'Sale-3-Sale Date:', 'Sale-3-Sales Type:', 'Sale-3-Recording:',
    'Sale-4-Buyer:', 'Sale-4-Seller:', 'Sale-4-Sale Date:', 'Sale-4-Sales Type:', 'Sale-4-Recording:',
    'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:',
    'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:',
    'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:',
    'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:',
    'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:', 'Addtnl-Sales:'
    ]

    if ( state == 4):

        page_num +=1
        page_scrape_ct+=1
        scrape_group_ct+=1
        round_trip_ct+=1
       
        print('the curr page number is', page_num)
        print('the curr record number is', sent_record_num )
        
        if ( round_trip_ct < 2 ):  state = 6

        if ( round_trip_ct >= 2 ): # kv
            
            plug_file = 'plug.csv'
            file_name ='county_county1.csv'
            #this process works for csvs 
            #open original file in read mode and dummy file in write mode
            with open( file_name, 'r') as read_obj, open(plug_file, 'w', newline="") as write_obj:
                #-- create a write obj
                updated_csv_file = csv.writer(write_obj)
                ##-- original file read and write into temp
                orig_file_data = csv.reader(read_obj, delimiter=",")
                updated_csv_file.writerows(orig_file_data)
                ##-- new data write
                updated_csv_file.writerows(final_data)
                # remove orig csv
            os.remove(file_name)
                # Rename dummy file as the original csv file
            os.rename(plug_file, file_name)

            state = 5  
 
        
    if ( state == 5 ) : # clear the list

        final_data.clear()
        round_trip_ct = 0

        if( final_data ==[] ): 
            state = 6


    if ( state == 6 ) :

        
        if ( page_scrape_ct >= scrape_max ) : # quit the entire job
            state = 101 
            print('the curr page number is', page_num)
            print('the curr record number is', sent_record_num )
            print('<==============={ JOB COMPLETE }=====================>')
            browser.quit()

        if (  page_scrape_ct < scrape_max     ): # reset for another batch keep job open
 
            if ( scrape_group_ct >= 9     ): # reset for another batch with new browser keep job open
                state = 0
                scrape_group_ct = 0 
                browser.quit()

            
            if  scrape_group_ct < 9 : # stay in current browser
                state = 2


