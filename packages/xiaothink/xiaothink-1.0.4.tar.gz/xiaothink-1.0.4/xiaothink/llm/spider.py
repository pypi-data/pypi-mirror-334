import requests
from bs4 import BeautifulSoup
import re
import easyocr
reader = easyocr.Reader(['ch_sim'])
ret=''
def fetch_links_and_text(url, visited_urls, file):
    global ret
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers,timeout=60)
        if '.jpg' in url or '.jpeg' in url or '.png' in url or '.gif' in url:
                    with open("tmp.png", "wb") as image_file:
                        image_file.write(response.content)
                    result = reader.readtext('tmp.png')
                    ocrt='\n'.join([i[-2] for i in result])
                    print("\033[0;33;40m ",'OCR',ocrt[:10].replace('\n','\\n')," \033[0m")

                    '''
                    with open('img_uli.txt', 'r', encoding='utf-8') as file:
                        uli=eval(file.read())
                    uli.append(url)
                    with open('img_uli.txt', 'w', encoding='utf-8') as file:
                        file.write(str(uli))
                    '''
                    with open(file, 'a', encoding='utf-8') as file:
                        file.write(ocrt)
                    return []
                
        elif response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text from the page
            text = ''
            for tag in soup.find_all(['a', 'p', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']):
                text += str(tag.text) + '\n'
            
            # Write to file
            if file:
                with open(file, 'a', encoding='utf-8') as file:
                    file.write(text.replace('\n\n','\n'))
                
            ret+=text.replace('\n\n','\n')
                


                        
            # Find all links and add to the list if not already visited
            new_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Ensure the URL is absolute
                if re.match(r'^http', href) is None:
                    href = requests.compat.urljoin(url, href)
                if href not in visited_urls:
                    new_links.append(href)
                    visited_urls.add(href)

            return new_links
        else:
            print(f"\033[0;31;40m Failed to retrieve {url} - Status Code: {response.status_code} \033[0m")
    except Exception as e:
        print(f"\033[0;31;40m Error fetching {url}: {e} \033[0m")
    
    return []

sy=0
def main(start_urls,passli=[
    'http://ir.baidu.com',
    'https://ir.ifeng.com/',
    ],
         maxlen=0,
         returnlen=0,
         file=None
         ):
    global sy,ret
    
    visited_urls = set(start_urls)
    urls_to_visit = start_urls[:]
    sy=len(visited_urls)
    
    while urls_to_visit:
        url = urls_to_visit.pop(0)
        sy-=1
        print(f"\033[0;36;40m请求: {url}","剩余个数：",sy,"\033[0m")

        if  '.bin' in url\
             or '.zip' in url\
             or '.tar' in url\
             or '.7z' in url:
            continue
        new_links = fetch_links_and_text(url, visited_urls,file)
        if returnlen and ret>returnlen:
            return ret

        if sy<maxlen:
            urls_to_visit.extend(new_links)
            urls_to_visit=list(set(urls_to_visit))
            sy=len(urls_to_visit)

