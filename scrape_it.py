# Example of parsing/scraping data using BeautifulSoup. Source used here: http://www.labour.delhigovt.nic.in/
# Author: Kartik Verma <kartx111@gmail.com>
#
import requests
from bs4 import BeautifulSoup
import sys
import csv
sys.setrecursionlimit(5000)

# We've now imported the two packages that will do the heavy lifting
# for us, reqeusts and BeautifulSoup

# Let's put the URL of the page we want to scrape in a variable
# so that our code down below can be a little cleaner
# Down below we'll add our inmates to this list
inmates_list = []

for i in range(1, 4401):
    print "Iterating for Range: " + str(i)
    url_to_scrape = 'http://www.labour.delhigovt.nic.in/ser/r_regstatus.asp?currentpage={}'.format(i)

    # Tell requests to retreive the contents our page (it'll be grabbing
    # what you see when you use the View Source feature in your browser)
    r = requests.get(url_to_scrape)

    # We now have the source of the page, let's ask BeaultifulSoup
    # to parse it for us.
    soup = BeautifulSoup(r.text, "html.parser")
    local_list = []
    # BeautifulSoup provides nice ways to access the data in the parsed
    # page. Here, we'll use the select method and pass it a CSS style
    # selector to grab all the rows in the table
    try:
        for table_row in soup.select("table tr"):
            # Each tr (table row) has three td HTML elements (most people
            # call these table cels) in it (first name, last name, and age)
            cells = table_row.find_all('td')

            # Our table has one exception -- a row without any cells.
            # Let's handle that special case here by making sure we
            # have more than zero cells before processing the cells
            if len(cells) > 0:
                # Our first name seems to appear in the second td element
                # that ends up being the cell called 1, since we start
                # counting at 0
                data = cells[1].text.strip().encode('utf-8').split()

                # Let's add our inmate to our list in case
                # We do this by adding the values we want to a dictionary, and
                # appending that dictionary to the list we created above
                local_list.append(data[0])

                # Let's print our table out.
                # print "Added {0}, to the list".format(reg_no)
    except:
        local_list.pop(0)
        inmates_list = list(set(inmates_list + local_list))
        print "Range 100 x {}, Total data collected: {}".format(i, len(inmates_list))
        pass

inmates_list = list(set(inmates_list))

inmate_details_list = []
count = 0

print "Now details Fetch Commences!"
fields = ['Reg. No.','Registration Date','Name','Category','Date of Commencement','e-Mail ID','Website URL', \
          'Name of Occupier','Father Name of Occupier','Name of Manager','Fathers Name of Manager','Nature of Business', \
          'Total Male Workers','Total Female Workers','Total Young Workers','Total Workers','Total Family Members Working in the Establishment', \
          'Total Employers Working in Confidential Capacity','Certificate No.','Certificate Date','Address']
with open('/tmp/logFile.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
# # Loop through the list of inmates we built for fetching details
for inmate in inmates_list:
    count = count + 1
    print "Details Fetched for: {}, Left: {}".format(count, len(inmates_list) - count)

    url_to_scrape = 'http://www.labour.delhigovt.nic.in/ser/r_estdet.asp?cer={}'.format(inmate)
    r = requests.get(url_to_scrape)
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        for table_row in soup.select("table tr"):
            cells = table_row.find_all('td')
            local_detailed_data = []
            if len(cells) > 0:
                # Reg. No.
                local_detailed_data.append(cells[1].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Registration Date
                local_detailed_data.append(cells[3].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Name
                local_detailed_data.append(cells[5].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Category
                local_detailed_data.append(cells[7].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Date of Commencement
                local_detailed_data.append(cells[9].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # e-Mail
                local_detailed_data.append(cells[13].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Website URL
                local_detailed_data.append(cells[15].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Name of Occupier
                local_detailed_data.append(cells[17].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Father Name of Occupier
                local_detailed_data.append(cells[19].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Name of Manager
                local_detailed_data.append(cells[21].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Fathers Name of Manager
                local_detailed_data.append(cells[23].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Nature of Business
                local_detailed_data.append(cells[25].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Total Male Workers
                local_detailed_data.append(cells[27].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Total Female Workers
                local_detailed_data.append(cells[29].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Total Young Workers
                local_detailed_data.append(cells[31].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Total Workers
                local_detailed_data.append(cells[33].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Total Family Members Working in the Establishment
                local_detailed_data.append(cells[35].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Total Employers Working in Confidential Capacity
                local_detailed_data.append(cells[37].text.strip().encode('utf-8').strip().replace(":", "").strip())
                # Certificate No
                local_detailed_data.append(cells[39].text.strip().encode('utf-8').split().replace(":", "").strip())
                # Certificate Date
                local_detailed_data.append(cells[41].text.strip().encode('utf-8').split().replace(":", "").strip())
                # Address
                local_detailed_data.append(cells[10].text.strip().encode('utf-8').strip().replace(":", "").strip())

    except:
        pass
    inmate_details_list.append(local_detailed_data)
    print "Count: {}, List: {}".format(count, len(inmates_list))

    if ((count % 10) == 0) or (count == len(inmates_list)):
        with open('/tmp/logFile.csv','a') as f:
            writer = csv.writer(f)
            for eachFieldList in inmate_details_list:
                writer.writerow(eachFieldList)
            inmate_details_list = []
