response = requests.get('https://www.wien.gv.at/kultur/archiv/politik/vertretungen.html')

soup = BeautifulSoup(response.text, 'html.parser').find('ul', class_='ul_unmarked')

entries = soup.find_all('a')

results = []

for entry in entries:
    link = entry.find('a')
    if link and 'href' in link.attrs:
        detail_page_url = 'https://www.wien.gv.at' + link['href']
        detail_response = requests.get(detail_page_url)
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
        details = extract_details(detail_response.text)
        results.append(details)

for entry in entries:
    detail_page_url = 'https://www.wien.gv.at' + entry['href']
    detail_response = requests.get(detail_page_url)
    detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
    details = extract_details(detail_response.text)
    results.append(details)



def extract_details(html_content):
    content = BeautifulSoup(html_content, 'html.parser')
    
    # Extract school details (assuming these are common elements)
    #name = content.find('h1', class_="headline", itemprop="name").text.strip() if detail_soup.find('h1', class_="headline", itemprop="name") else "N/A"
    table = content.find('tbody').text.strip() if detail_soup.find('tbody') else 'N/A'
    
    return {
        #'name': name
        'table': table
    }
