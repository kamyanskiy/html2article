# html2article Get article from html and save as formatted text.
 
Library newspaper3k was used https://github.com/codelucas/newspaper
 
#### On Windows (in cmd)
```
E:\> cd html2article
E:\html2article> virtualenv.exe .
E:\html2article> Scripts\activate.bat
(grab_article) E:\html2article> pip install -r requirements.txt

(grab_article) E:\html2article> html2article.py -h
usage: html2article.py [-h] [-v] url

Parse HTML into structured text.

positional arguments:
  url            URL to grab html from.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Verbose output

```  

It requires nltk library 'punkt' package, probably after first start, it asks
to install it. On tab Modules - select 'punkt' package, then Install.

### Examples 

```
./html2article https://lenta.ru/news/2017/05/25/ka62/ -v

Page https://lenta.ru/news/2017/05/25/ka62/ was downloaded successful.

Вертолет  .....
....

File was successfully stored as lenta.ru/news/2017/05/25/ka62/ka62.txt

```

```
./html2article https://www.gazeta.ru/culture/2017/05/25/a_10693097.shtml

Here is nothing in output


File was stored into www.gazeta.ru/culture/2017/05/25/a_10693097.txt

```
