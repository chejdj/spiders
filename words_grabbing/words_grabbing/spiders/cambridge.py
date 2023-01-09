from scrapy import Request
import scrapy
import sys
import xlrd
import xlwt
from words_grabbing.items import WordsGrabbingItem
from bs4 import BeautifulSoup
from xlutils.copy import copy


class CamDicWord:
    def __init__(self):
        self.headword = ''
        self.pos = ''
        self.pos_detail = ''
        self.level = ''
        self.english_trans = ''
        self.chinese_trans = ''
        self.sentences = []

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

def _write_to_xls(cam_dic_words, file_name, write_time, startCount):
        if write_time <= 0:
            workbook = xlwt.Workbook(encoding='utf-8')
            sheet = workbook.add_sheet('cambridge_dictionary_words')
        else:
            fileIndex  = write_time -1
            path = file_name+ str(fileIndex) + ".xls"
            wb = xlrd.open_workbook(path)
            workbook = copy(wb)
            sheet = workbook.get_sheet(0)
        index = startCount
        for word in cam_dic_words:
            index += 1
            sheet.write(index, 0, word.headword)
            sheet.write(index, 1, word.pos)
            sheet.write(index, 2, word.pos_detail)
            sheet.write(index, 3, word.level)
            sheet.write(index, 4, word.english_trans)
            sheet.write(index, 5, word.chinese_trans)

            x = 6
            for sentence in word.sentences:
                sheet.write(index, x, sentence.english)
                x += 1
                sheet.write(index, x, sentence.chinese)
                x += 1        
        workbook.save(file_name + str(write_time) + ".xls")

class Sentence:
    def __init__(self):
        self.english = ''
        self.chinese = ''    


class CambridgeSpider(scrapy.Spider):
    name = 'cambridge'
    host = 'https://dictionary.cambridge.org/dictionary/english-chinese-simplified/'
    index = 0
    length = 500
    words = _read_words_from_xls_file('todo.xlsx')
    url = host + words[index]
    start_urls = [url]
    cam_dic_words = []
    write_time = 0
    startCount = 0
    lastWords = ''

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        word_pos_sections = soup.findAll(attrs={'class': 'entry-body__el'})
        for word_pos_section in word_pos_sections:
            header = word_pos_section.find(attrs={'class': 'pos-header'})

            if not header.find(attrs={'class': 'headword'}):
                continue
            if not header.find(attrs={'class': 'posgram'}):
                continue

            headword = header.find(attrs={'class': 'headword'}).text
            pos = header.find(attrs={'class': 'posgram'}).text

            body = word_pos_section.find(attrs={'class': 'pos-body'})
            word_pos_detail_sections = body.findAll(attrs={'class': 'dsense'})
            for word_pos_detail_section in word_pos_detail_sections:
                if 'dsense-noh' in word_pos_detail_section['class']:
                    item = CamDicWord()
                    item.headword = headword
                    item.pos = pos
                    item.level = ''
                    real_word_section = word_pos_detail_section.find(attrs={'class': 'def-block'})
                    if real_word_section.find(attrs={'class': 'epp-xref'}):
                        item.level = real_word_section.find(attrs={'class': 'epp-xref'}).text
                    item.english_trans = real_word_section.find(attrs={'class': 'def'}).text
                    if(real_word_section.find(attrs={'class': 'trans'})): 
                      item.chinese_trans = real_word_section.find(attrs={'class': 'trans'}).text
                    sentence_sections = real_word_section.findAll(attrs={'class': 'examp'})
                    for sentence_section in sentence_sections:
                        sentence = Sentence()
                        sentence_english = sentence_section.find(attrs={'class': 'eg'})
                        if sentence_english is not None:
                            sentence.english = sentence_section.find(attrs={'class': 'eg'}).text
                        sentence_chinese = sentence_section.find(attrs={'class': 'trans'})
                        if sentence_chinese is not None:
                            sentence.chinese = sentence_section.find(attrs={'class': 'trans'}).text
                        item.sentences.append(sentence)
                    self.cam_dic_words.append(item)
                    continue
                pos_detail = ''
                if word_pos_detail_section.find(attrs={'class': 'dsense_h'}):
                    pos_detail = word_pos_detail_section.find(attrs={'class': 'dsense_h'}).text

                real_word_sections = word_pos_detail_section.findAll(attrs={'class': 'def-block'})
                for real_word_section in real_word_sections:
                    item = CamDicWord()
                    item.headword = headword
                    item.pos= pos
                    item.pos_detail = pos_detail
                    item.level = ''
                    if real_word_section.find(attrs={'class': 'epp-xref'}):
                        item.level = real_word_section.find(attrs={'class': 'epp-xref'}).text
                    item.english_trans = real_word_section.find(attrs={'class': 'def'}).text
                    item.chinese_trans = ''
                    for child in real_word_section.find(attrs={'class': 'def-body'}).contents:
                        if child.name == 'span':
                            item.chinese_trans = child.text

                    sentence_sections = real_word_section.findAll(attrs={'class': 'examp'})
                    for sentence_section in sentence_sections:
                        sentence = Sentence()
                        sentence.english = sentence_section.find(attrs={'class': 'eg'}).text
                        sentence_chinese = sentence_section.find(attrs={'class': 'trans'})
                        if sentence_chinese is not None:
                            sentence.chinese = sentence_section.find(attrs={'class': 'trans'}).text
                        item.sentences.append(sentence)
                    self.cam_dic_words.append(item)
                    


        self.index = self.index + 1
        if self.index < self.length :
            print('have finished '+ str(self.index))
            nexturl = self.host + self.words[self.index].lower()
            yield Request(nexturl,meta={"handle_httpstatus_all": True},dont_filter = True)
        else:
            _write_to_xls(self.cam_dic_words, 'test', self.write_time, self.startCount)
            if self.index < len(self.words):
                self.length = self.length + 500
                nexturl = self.host + self.words[self.index]
                self.startCount = self.startCount + len(self.cam_dic_words)
                self.cam_dic_words = []
                self.write_time = self.write_time +1
                yield Request(nexturl,meta={"handle_httpstatus_all": True},dont_filter = True)
        pass


