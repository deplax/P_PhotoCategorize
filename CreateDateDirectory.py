# -*- coding: utf-8 -*-
__author__ = 'Administrator'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import os
import time
import shutil
from PIL import Image
from PIL.ExifTags import TAGS

filelist = []
def dirSearch(dirname):
    first = os.listdir(dirname)
    for f in first:
        next = os.path.join(dirname, f)

        if os.path.isdir(next):
            dirSearch(next)
        else:
            filelist.append(next)

    return filelist


def createDirectory(path):
    #파일 리스트를 돌면서 없는 날짜의 폴더를 만든다.
    if not os.path.isdir(path):
        os.mkdir(unicode(path))
        log(str(path + " 폴더 생성"))

def fileCopy(src, dsc):
    shutil.copy(src, dsc)
    print "%s에서 %s로 복사하였습니다." % (src, dsc)

def get_exif(path):
    ret = {}
    try:
        i = Image.open(path)
        info = i._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        return ret
    except:
        log(str("메타데이터를 가져올 수 없습니다. | " + path))
        return

logtext = ""
def log(str):
    global logtext
    if not str:
        logtext = logtext + "--- Str IS EMPTY ---" + "\r\n"
        print logtext
    else:
        logtext = logtext + str + "\r\n"
        print logtext

def extractDate(info):
    try:
        with open("logtext.txt", 'wb') as f:
            f.write(logtext)
        if info:
            dateall = info["DateTime"]
            datelist = dateall.split(':')
            date = datelist[0][2:4] + datelist[1] + datelist[2][0:2]
            return date
        else:
            pass
    except:
        pass

#---------------------------------------------------------------
# 정리할 최상위 디렉토리
rootdir = u"E:\PhotoTest\origin"
# 저장할 위치
movedir = u'E:\PhotoTest\sort'
#---------------------------------------------------------------

# 디렉토리를 넣으면 리스트를 만들어 준다.
filelist = dirSearch(rootdir)

# 만들어진 파일 리스트를 순회한다.
for f in filelist:

    # 이미지 메타데이터를 받아온다.
    info = get_exif(f)

    # 받아온 메타 데이터를 형식에 맞게 자른다.
    date = extractDate(info)

    # 파일을 받아온 경우에만
    if date:
        path = movedir + "/" + date
        createDirectory(path)

        # 파일을 날짜에 맞게 이동
        try:
            shutil.move(f, path)
            log(str(f + " 파일을 " + path + "로 이동"))
        except shutil.Error:
            log(str(f + " 파일이 " + path + "에 이미 존재하여 복사하지 않았습니다."))
            pass
    else:
        filestat = os.stat(f)
        timecode = time.strftime('%y%m%d', time.localtime(filestat.st_mtime))
        path = movedir + timecode
        createDirectory(path)

        # 파일을 날짜에 맞게 이동
        try:
            shutil.move(f, path)
            log(str(f + " 파일을 " + path + "로 이동"))
        except shutil.Error:
            log(str(f + " 파일이 " + path + "에 이미 존재하여 복사하지 않았습니다."))
            pass
        except WindowsError:
            log(str(f + " 파일이 " + path + "로 옮기는 도중 에러발생!!"))



#모두 끝나고 로그 저장
with open( movedir + "/mergeLog.txt", 'wb') as f:
    f.write(logtext)

#--------------------------------------------------------------
# #파일을 날짜에 맞게 복사해 넣는다.
# fileCopy(f, path)




