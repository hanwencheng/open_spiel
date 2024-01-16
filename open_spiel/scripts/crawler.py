import requests
from bs4 import BeautifulSoup

url = 'https://wiki.biligame.com/tdj/%E7%8E%84%E7%BE%BD' # Replace with your target URL

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Now, you can parse the soup object to find the information you need
# For example, to get all paragraph texts:
main_content = soup.find('div', {'class': 'container main'})
# start_tag = main_content.find('div', {'id': 'start'})
# end_tag = main_content.find('div', {'id': 'end'})
#
# content = []
# for element in start_tag.next_siblings:
#     if element == end_tag:
#         break
#     if hasattr(element, 'get_text'):
#         content.append(element.get_text())
# captured_text = ' '.join(content)

for paragraph in main_content.find_all('p'):
    text = ' '.join(paragraph.get_text().split())
    print(text)

for paragraph in main_content.find_all('tr'):
    text = ' '.join(paragraph.get_text().split())
    print(text)


