import sys
import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import urllib.error
import getopt

def check_page(target_url, contains_url):
    print("\n-----" + target_url + "-----")
    for url in contains_url:
        if url.find("#") >= 0:  
            continue
        try: 
            with urllib.request.urlopen(url) as res:
                print("  " + url + " : OK")
        except urllib.error.HTTPError as err:
            print("  " + url + " : NG " + err.reason)
        except Exception as e:
            print("  " + url + " : NG ", e.args)

opts, args = getopt.getopt(sys.argv[1:], "t:o:", ["check"])
if not args: 
    print("usage: python crawl.py [option -t read target -o filename --check] url")

read_targets = []
out_file = None
is_check = False

for opt, value in opts:
    if opt == "-t":
        read_targets.append(value)
    elif opt == "-o":
        out_file = value
    elif opt == "--check":
        is_check = True

base_url = args[0]
hostname = urlparse(base_url).hostname
read_targets.append(hostname)

url_map = {}
crawl_targets = [base_url]
err_targets = []
while crawl_targets:
    print(".", end='', flush=True)
    c_base_url = crawl_targets.pop()
    if c_base_url in url_map:
        continue
    if c_base_url in err_targets:
        continue

    try: 
        with urllib.request.urlopen(c_base_url) as res:
            html = res.read()
            soup = BeautifulSoup(html, "html.parser")

            c_urls = []
            for link in soup.find_all('a'):
                if link.get('href'):
                    c_url = link.get('href')
                    parse_result = urlparse(c_url)
                    if parse_result.scheme == '':
                        c_url = urljoin(c_base_url, c_url)
                    if c_url not in c_urls:
                        c_urls.append(c_url)
                        if c_url in url_map:
                            continue
                        c_url_hostname = urlparse(c_url).hostname
                        for r in read_targets:
                            if c_url_hostname == r:
                                if c_url.find("#") == -1:  
                                 crawl_targets.append(c_url)
                                 break
            c_urls.sort()
            url_map[c_base_url] = c_urls

            if is_check:
                check_page(base_url, url_map[base_url])
                sys.exit(0)

    except urllib.error.HTTPError as err:
        err_targets.append(c_base_url)


print()
if out_file:
    f = open(out_file, "w")
else:
    f = sys.stdout

url_keys = list(url_map.keys())
url_keys.sort()
for key in url_keys:
    print("-----" + key + "-----", file=f)
    for result in url_map[key]:
        print(" " + result, file=f)

print("----- error links -----", file=f)
for e_url in err_targets:
    print(e_url, file=f)

if out_file:
    f.close()
