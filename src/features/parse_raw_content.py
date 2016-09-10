import re, json, datetime

from unidecode import unidecode
from bs4 import BeautifulSoup


# html tags of interest
TAGS = ['title', 'h1', 'h2', 'h3', 'meta-description', 'meta-keywords',
        'img', 'a', 'other']

def clean_string(s):
    s = s.lower()
    s = re.sub(r'\s+', ' ', s)
    return s.strip()
    
def soupify(urlid, parser='lxml'):
    filename = '../data/raw/raw_content/' + str(urlid)
    
    with open(filename, 'rb') as infile:
        html = infile.read()
        
        for parser in ['lxml', 'xml', 'html5lib']:
            soup = BeautifulSoup(html, parser)
            
            if soup.body:
                return soup
        
        infile.close()
        return BeautifulSoup(html)
        
def main(train, test):
    data = train + test
    
    with open('../data/processed/extracted_text', 'w') as outfile:

        for i, item in enumerate(data):
            # status update
            
            if (i % 500 == 0):
                print(i, datetime.datetime.now().time())
            
        
            # parse file
            parsed_data = {}
            
            soup = soupify(item['urlid'])
            
            # given boilerplate
            
            parsed_data['boilerplate'] = [item['title'], item['body']]
            
            # remove non-text tags
            for tag in ['script', 'style']:
                for el in soup.find_all(tag):
                    el.extract()
                    
            # extract text from each tag
            
            for tag in TAGS:
                items = []
                
                for el in soup.find_all(tag):
                    el.extract()
                    
                    if tag == 'img':
                        try:
                            items.append(el['alt'])
                        except KeyError:
                            pass
                        
                        try:
                            items.append(el['title'])
                        except KeyError:
                            pass
                    else:
                        items.append(el.text)
                
                parsed_data[tag] = items
            
            # extract meta tags
            meta = soup.find_all('meta')
            
            for el in meta:
                prop = el.get('property') if el.get('property') else el.get('name')
                
                if not prop:
                    continue
                prop = prop.lower()
                
                try:
                    s = s.decode('unicode-escape')
                except:
                    continue
                
                parsed_data['meta-'+prop] = s.split(u',') if prop == 'keywords' else [s]
            
            # clean string
            for d in parsed_data:
                parsed_data[d] = list(map(clean_string, parsed_data[d]))
                parsed_data[d] = list(filter(None, parsed_data[d]))
        
            outfile.write(json.dumps(parsed_data))
            outfile.write('\n')
            
        outfile.close()






