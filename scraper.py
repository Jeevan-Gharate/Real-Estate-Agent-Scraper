# AUTHOR: ZYRO aka Jeevan

import pandas as pd
import requests, time, datetime
from bs4 import BeautifulSoup


# Create and export to names.csv
def createcsv(results, phone_results, st, cityn):
    df = pd.DataFrame({'Names': results, 'Phone': phone_results})
    df.to_csv(f'{cityn.replace("-", "")}.csv', index=False, encoding='utf-8')
    print("\n[!] Data Scraped and Saved into names.csv!")
    print("\n--- in %s seconds ---" % (time.time() - st))


def scrapeit():
    state=str(input("[!] Enter State Abbreviation: "))
    city_name = str(input("[!] Enter City name (use - in place of spaces): "))
    r = requests.get('https://www.realtor.com/realestateagents/' + city_name + '_' + state + '/', headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"})
    occurrences = r.text.count("Go to page ")
    index_positions = []
    index = -1
    while True:
        index = r.text.find("Go to page ", index + 1)
        if index == -1:
            break
        index_positions.append(index)
    last_oc = index_positions[index_positions.__len__()-1]

    pageNumber = 2
    max_pages = int(r.text[last_oc+14-3:last_oc+14])
    while True:
        e_page = int(input(f"[!] Enter number of Pages to Scrape ~max ({max_pages}): "))
        if e_page > max_pages:
            e_page = int(input(f"[!] Enter less that {max_pages}: "))
        else:
            break
    print("")
    st=time.time()

    if r.status_code == 200:
        # Create Arrays
        results = []
        phone_results = []
        content = r.text
        soup = BeautifulSoup(content, features="html.parser")

        # Find Names
        for a in soup.findAll(attrs='mobile-agent-card-wrapper'):
            name = a.find("a")
            if name not in results:
                results.append(name.text)

        # Find Phone Numbers
        for link in soup.find_all('a', {"class": "btn-contact-me-call"}):
            phone_results.append(link.get('href'))

        
        while pageNumber <= e_page: # change end page as per your convinience (200 max recommended) remember: end_page*sleep_time*per_req_time = program_execution_time
            # Get 2nd Page
            print(f"[~] Scraping Data from page Number: {pageNumber}")
            rr = requests.get('https://www.realtor.com/realestateagents/' + city_name + '_' + state + '/pg-' + str(pageNumber))
            # Find Names
            content = rr.text
            soup = BeautifulSoup(content, features="html.parser")
            for a in soup.findAll(attrs='mobile-agent-card-wrapper'):
                name = a.find("a")
                if name not in results:
                    results.append(name.text)

            # Find Phone Numbers
            for link in soup.find_all('a', {"class": "btn-contact-me-call"}):
                phone_results.append(link.get('href'))

            #Iterates through pages
            pageNumber += 1
            #Slows down HTTP Requests to prevent connection refusal
            time.sleep(2) # change number of seconds as per your convinience
        createcsv(results, phone_results, st, cityn)
    else:
        print(f"\n[!] Something Went Wrong: Response Code {r.status_code}\n\nMore details:\n{r.text}")

if __name__ == "__main__":
    scrapeit()
