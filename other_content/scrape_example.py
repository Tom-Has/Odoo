import requests
from bs4 import BeautifulSoup
import csv

def extract_details(html_content):
    detail_soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract school details (assuming these are common elements)
    name = detail_soup.find('h1', class_="headline", itemprop="name").text.strip() if detail_soup.find('h1', class_="headline", itemprop="name") else "N/A"
    street = detail_soup.find('span', itemprop='streetAddress').text.strip() if detail_soup.find('span', itemprop='streetAddress') else "N/A"
    zip = detail_soup.find('span', itemprop='postalCode').text.strip() if detail_soup.find('span', itemprop='postalCode') else "N/A"
    city = detail_soup.find('span', itemprop='addressLocality').text.strip() if detail_soup.find('span', itemprop='addressLocality') else "N/A"
    mail = detail_soup.find('a', class_='link', href=lambda href: href and href.startswith('mailto:')).text if detail_soup.find('a', class_='link', href=lambda href: href and href.startswith('mailto:')) else "N/A"
    phone = detail_soup.find('a', class_='link schoolContactPhone__number', href=lambda href: href and href.startswith('tel:')).text if detail_soup.find('a', class_='link schoolContactPhone__number', href=lambda href: href and href.startswith('tel:')) else "N/A"
    
    return {
        'name': name,
        'street': street,
        'zip': zip,
        'city': city,
        'mail': mail,
        'phone': phone
    }

def scrape_school_directory(bundesland, max_pages=float('inf')):
    base_url = "https://www.schulverzeichnis.eu/typ/?p={}&bundesland={}"
    results = []
    page = 1
    
    while True:
        url = base_url.format(page, bundesland)
        try:
            response = requests.get(url)
            response.raise_for_status()  # Will raise an HTTPError for bad status codes
            soup = BeautifulSoup(response.text, 'html.parser').find('div', class_='cardList cardList--spaceTop-38')
            
            entries = soup.find_all('p', class_='post__more')
            
            if not entries:  # If no entries found, we've reached the last page
                break
            
            for entry in entries:
                link = entry.find('a')
                if link and 'href' in link.attrs:
                    detail_page_url = link['href']
                    detail_response = requests.get(detail_page_url)
                    detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                    details = extract_details(detail_response.text)
                    details['state'] = bundesland
                    results.append(details)
                    
            page += 1
            if page > max_pages:
                break  # Stop if we've reached the maximum number of pages to scrape
            
        except requests.HTTPError:
            print(f"HTTP Error on page {page} for {bundesland}")
            break
        except requests.RequestException as e:
            print(f"Request Exception for {bundesland}: {e}")
            break

    return results

# List of bundesland names
bundeslaender = ['wien', 'burgenland', 'niederosterreich', 'oberosterreich',
                 'steiermark', 'salzburg', 'karnten', 'tirol', 'vorarlberg']

"""
bundeslaender = ['wien', 'tirol']
"""
                 
mp = 100

# Example usage
all_results = []
for bundesland in bundeslaender:
    results = scrape_school_directory(bundesland, max_pages=mp)  # Adjust max_pages as needed
    all_results.extend(results)
    print(f"Finished scraping {bundesland}. Found {len(results)} entries.")

# Writing to CSV
with open('school_directory.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['name', 'street', 'zip', 'city', 'state', 'mail', 'phone']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for result in all_results:
        writer.writerow(result)

print(f"Total entries written to CSV: {len(all_results)}")