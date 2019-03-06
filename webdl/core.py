import urllib
import urllib3
import os
import sys

try:
        from bs4 import BeautifulSoup
except ImportError:
        print(
            "[*] Please download and install Beautiful Soup first!")
        sys.exit(0)


MOZVAL = (
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"
)

URL = "http://yeda.cs.technion.ac.il:8088/corpus/software/corpora/wiki/"
DOWNLOAD_PATH = "Users/shaypalachy/Downloads/wiki"

if __name__ == "__main__":
    url = URL
    download_path = DOWNLOAD_PATH

    try:
            # to make it look legit for the url
            headers = {"User-Agent": MOZVAL}
            i = 0
            request = urllib3.Request(url, None, headers)
            html = urllib3.urlopen(request)
            soup = BeautifulSoup(html.read())  # to parse the website
            # find <a> tags with href in it so you know it is for urls
            # so that if it doesn't contain the full url it can the url itself
            # to it for the download
            for tag in soup.findAll('a', href=True):
                    tag['href'] = urllib.urljoin(url, tag['href'])
                    # this is pretty easy we are getting the extension
                    # (splitext) from the last name of the full url(basename)
                    # the spiltext splits it into the filename and the
                    # extension so the [1] is for the second part
                    # (the extension)
                    current_ext = os.path.splitext(
                        os.path.basename(tag['href']))[1]
                    if current_ext == '.pdf':
                            current = urllib3.urlopen(tag['href'])
                            href = os.path.basename(tag['href'])
                            print(f"\n[*] Downloading: {href}")
                            fname = os.path.basename(tag['href'], "wb")
                            fpath = f"{download_path}\\{fname}"
                            with open(fpath) as f:
                                f.write(current.read())
                            i += 1
            print(f"\n[*] Downloaded {i+1} files")
    except KeyboardInterrupt:
            print("[*] Exiting...")
            sys.exit(1)
