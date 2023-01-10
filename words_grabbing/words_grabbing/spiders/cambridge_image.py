import scrapy
from bs4 import BeautifulSoup
from scrapy import Request
import xlrd
import xlwt
import requests
from fake_user_agent import user_agent

def _read_words_from_xls_file(fileName):
    words = []
    workbook = xlrd.open_workbook(fileName)
    sheet = workbook.sheet_by_index(0)
    for i in range(sheet.nrows):
        if(len(words) == 0):
           words.append(sheet.row(i)[0].value)
        if sheet.row(i)[0].value != words[len(words) -1]:
           words.append(sheet.row(i)[0].value)
    return words

def _download_imag(imageUrl, filePath):
    ua = user_agent()
    print('image download ' + imageUrl)
    r = requests.get(imageUrl,headers={'User-Agent': ua},stream=True)
    print('image statusCode '+ str(r.status_code))
    if r.status_code == 200:
        open(filePath, 'wb').write(r.content)


class CambridgeImageSpider(scrapy.Spider):
    name = 'cambridge_image'
    host = 'https://dictionary.cambridge.org/dictionary/english/'
    imageHost = 'https://dictionary.cambridge.org'
    index = 0
    words = _read_words_from_xls_file('todo.xlsx')
    url = host + words[0]
    start_urls = [url]
    lastImages = ''
    lastIndex = 0

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        word_pos_sections = soup.findAll('div',attrs={'class','pr dsense'})
        for word_sections in word_pos_sections:
            imageUrlSection = word_sections.find('amp-img')
            if imageUrlSection is not None: 
              imageUrl = imageUrlSection['src']
              imageUrl = imageUrl.replace("/thumb/","/full/")
              imageUrl = self.imageHost + imageUrl
              pos = word_sections.find(attrs={'class': 'dsense_pos'}).text
              imagePath = 'images/'+self.words[self.index]+"_"+pos+".jpg"
              if(self.lastImages == imagePath):
                imagePath = 'images/'+self.words[self.index]+"_"+pos+"_"+ str(self.lastIndex)+".jpg"
                self.lastIndex = self.lastIndex+1
              else:
                self.lastImages = imagePath
                self.lastIndex = 0
              _download_imag(imageUrl, imagePath)
        self.index = self.index + 1
        newurl = self.host + self.words[self.index].lower()
        print('start index: '+ str(self.index))
        yield Request(newurl,meta={"handle_httpstatus_all": True},dont_filter = True)
        pass
