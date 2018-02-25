#!/usr/bin/python
# -*- encoding: utf-8 -*-

import struct
import random
import utils
import time
import os


rc4_encry_key = [0xc9, 0x2a, 0x82, 0x04, 0x45, 0X00, 0xca, 0x88, 0x40, 0x10, 0x08, 0x88, 0x84, 0x00, 0x88, 0x74, 0x04, 0x20, 0x10, 0x40, 0x11, 0x02, 0x6b, 0x10, 0x20, 0x57, 0x0e, 0x1c, 0x89, 0x45, 0x2a, 0x40, 0x1d, 0x09, 0x00, 0x80, 0x2c, 0x48, 0x08, 0x48, 0x19, 0x04, 0x90, 0x81, 0x42, 0x19, 0x08, 0x8c]



base_characters = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '2', '3', '4', '5', '6', '7', '8', '9']

base_characters_2_num = {
    'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,
    'J':8, 'K':9, 'L':10, 'M':11, 'N':12, 'P':13, 'Q':14, 'R':15,
    'S':16, 'T':17, 'U':18, 'V':19, 'W':20, 'X':21, 'Y':22, 'Z':23,
    '2':24, '3':25, '4':26, '5':27, '6':28, '7':29, '8':30, '9':31}



g_redeem_xml = None
g_redeem_logger = None

class RedeemXML:
    ' '
    version = '0.1'
    xmlfile = None
    xmlfilehandle = None
    lines = None
    xmlfilehandle_new = None
    
    def __init__(self, xmlfile = 'CfgRedeem.xml'):
        self.xmlfile = xmlfile
        
        try:
            self.xmlfilehandle = open(xmlfile, 'r')
            self.xmlfilehandle_new = open(xmlfile + ".new", 'w')

            # self.rawinfo('<?xml version="1.0" ?>' + '\n')
            # self.rawinfo('<root>' + '\n')
        except IOError, e:
            print('open file' + xmlfile + 'error: ' + e)
            self.xmlfilehandle.close()
            self.xmlfilehandle_new.close()
            exit(1)
        except Exception, e:
            print('Exception: ' + e)
            self.xmlfilehandle.close()
            self.xmlfilehandle_new.close()
            exit(1)
            
        lines = self.xmlfilehandle.readlines()
        line_count = 0
        for line in lines:
            line_count += 1
            if line_count != lines.__len__(): 
                self.xmlfilehandle_new.write(line)

        self.xmlfilehandle_new.flush()

        
    def __del__(self):
        self.rawinfo('</root>' + '\n')
        self.xmlfilehandle.close()
        self.xmlfilehandle_new.close()

        os.system('mv ' + self.xmlfile + '.new' + ' ' + self.xmlfile)
        
        
    def rawinfo(self, msg):
        self.xmlfilehandle_new.write(msg)
        self.xmlfilehandle_new.flush()

    def new_redeem(self, redeem_id, redeem_code):
        msg = '<CfgRedeem redeem_id="' + str(redeem_id) + '"' + ' redeem_code="' + redeem_code + '" type="1" gamezones="0" beg_time="15061918" end_time="15083018" times="1"'
        msg += ' gold="' + str(gold) + '"'
        msg += ' diamond="' + str(diamond) + '"'

        if len(items) > 0:
            msg += ' items="'
        items_i = 0
        items_str = ''
        for key in items:
            if items_i != 0:
                items_str += '|'
            items_i += 1
            items_str += str(key) + ',' + str(items[key])

        msg += items_str
        msg += '"'
        msg += ' />' + '\n'
        self.rawinfo(msg)

        
class RedeemLogger:
    ' '
    version = '0.1'
    xmlfile = None
    xmlfilehandle = None
    
    def __init__(self, beg_id, num, diamond,  gold, items, msg, xmlfile = 'CfgRedeem.log'):
        self.xmlfile = xmlfile
        
        try:
            self.xmlfilehandle = open(xmlfile, 'a')
            self.rawinfo('---------------------------------------' + '\n')
            self.rawinfo('RedeemLogger Begin ' + self.currentTimestamp() + '\n')
            self.rawinfo('MSG: ' + msg + '\n')
            self.rawinfo('\n')
        except IOError, e:
            print('open file' + xmlfile + 'error: ' + e)
            self.xmlfilehandle.close()
            exit(1)
        except Exception, e:
            print('Exception: ', e)
            self.xmlfilehandle.close()
            exit(1)
            
    def __del__(self):
        self.rawinfo('\n')
        self.rawinfo('RedeemLogger End ' + '\n')
        self.rawinfo('---------------------------------------' + '\n')
        self.rawinfo('\n')
        self.rawinfo('\n')
        self.xmlfilehandle.close()

    def currentTimestamp(self):
        curTS = time.strptime(time.ctime())
        retStr = "%4d%02d%02d %02d:%02d:%02d " % (curTS.tm_year, curTS.tm_mon, curTS.tm_mday, curTS.tm_hour,  curTS.tm_min, curTS.tm_sec)

        return retStr        
        
    def rawinfo(self, msg):
        self.xmlfilehandle.write(msg)
        self.xmlfilehandle.flush()

    def new_redeem_pair(self, origin_id, redeem_id, redeem_code):
        msg = str(origin_id) + '  ' + str(redeem_id) + ': ' + str(redeem_code) + '\n'
        self.xmlfilehandle.write(msg)
        self.xmlfilehandle.flush()        

        
        

        
def num_2_base32_encode(x):

    buf = ''
    x_list = []
    x_list.append(x % 32)
    x /= 32
    while(0 != x):    
        x_list.append(x % 32)
        x /= 32

    x_list.reverse()
    for item in x_list:
        buf += base_characters[item]
        
    return buf


def num_2_base32_decode(x_list):

    x_list.reverse()
    
    x = 0
    factor = 1
    
    for item in x_list:
        x += (base_characters_2_num[item] * factor)
        factor *= 32
        
    return x
        
# unsigned char *b24d(unsigned char *buf, char *str, size_t countOfChars):
#     size_t i;
#     char *p = str;
#     char *loc[2];
#     unsigned char n[2];
#     if (countOfChars % 2)
#     return NULL;
    
#     for (i = 0; i < (countOfChars>>1); i++) {
 
#         loc[0] = strchr( sel, str[2*i] );
#         loc[1] = strchr( sel, str[ ( 2*i ) + 1 ] );
#         if (loc[0] == NULL || loc[1] == NULL)
#     return NULL;
#         n[0] = (unsigned char)( loc[0] - sel );
#         n[1] = 23 - (unsigned char)( loc[1] - sel );
#         buf[i] = (unsigned char)((n[0] << 4) | n[1]);
#             }
    
#     return buf;

def check_beg_id_valid(beg_id, numfile = 'numfile.log'):
    try:
        numfilehandle = open(numfile, 'r')
    except IOError, e:
        #print('open file' + numfile + 'error: ' + str(e))
        #numfilehandle.close()
        return True
        #exit(1)
    except Exception, e:
        print('Exception: ', e)
        numfilehandle.close()
        
        exit(1)        

    line = numfilehandle.readline()
    last_end_id = int(line)    
    if beg_id <= last_end_id:
        print('beg_id must greater than: ' + str(last_end_id))
        return False

    return True
    

    
def write_numfile(num, numfile = 'numfile.log'):
    try:
        numfilehandle = open(numfile, 'w')
    except IOError, e:
        print('open file' + numfile + 'error: ' + e)
        numfilehandle.close()
        exit(1)
    except Exception, e:
        print('Exception: ', e)
        numfilehandle.close()        
        exit(1)

    numfilehandle.write(str(num))
    
    
#[4][8] --> [][]  4位整型1000-9999随机数 8位顺序不重复数字        
def gen_redeem(beg=10000000, num=5):
    i = 0
    index = 0
    while i<num:        
        tmp_target = (beg + i)
        target = tmp_target
        i += 1

        a_list = []
        while 0 != tmp_target:
            a_list.append(tmp_target % 10)
            tmp_target /= 10

            
        # 4 wei random
        index = target
        target = random.randint(1000, 9999) * 100000000  + target
        
        inbuf = num_2_base32_encode(target)
        #print(inbuf)
        
        #en_str = utils.rc4(struct.pack('=L', target), rc4_encry_key)
        en_str = utils.rc4(struct.pack('=Q', target), rc4_encry_key)
        #print("len(en_str):" + str(len(en_str)))

        en_num = target 
        
        outbuf = ''
        for tmp in en_str:
            outbuf += chr(tmp)    
        #en_num = struct.unpack('=Q', outbuf[:8])[0]
        #print(str(index) + '  ' + str(target) + ': ' + num_2_base32_encode(en_num))
        #print("en_num:" + str(en_num))

        global g_redeem_xml
        global g_redeem_logger
        g_redeem_xml.new_redeem(target, num_2_base32_encode(en_num))
        g_redeem_logger.new_redeem_pair(index, target, num_2_base32_encode(en_num))


    write_numfile(index)
    
if __name__ == '__main__':
    #utils.testfun()

    #8位顺序不重复数字        
    beg_id = 10003020
    num = 110

    if check_beg_id_valid(beg_id) is False:
        print('check_beg_id_valid failed!')
        exit(1)

    diamond = 500
    gold = 200000
    #小经验药水5101; 大经验药水5103;
    items = {5103:5}
    #items = {5101:5, 5105:2}
    
    g_redeem_xml = RedeemXML()
    #g_redeem_logger = RedeemLogger(beg_id, num, gold, diamond, items, "Q群礼包, 单账号使用, 2000个, 钻石*50；金币*30000；经验药水（小）*10")

    #g_redeem_logger = RedeemLogger(beg_id, num, gold, diamond, items, "渠道礼包, 单账号使用, 1000个, 钻石*100；金币*30000；经验药水（小）*10")

    g_redeem_logger = RedeemLogger(beg_id, num, gold, diamond, items, "精英礼包, 单账号使用, 100个, 钻石*500；金币*200000；经验药水（大）*5")

    

    gen_redeem(beg_id, num)    
