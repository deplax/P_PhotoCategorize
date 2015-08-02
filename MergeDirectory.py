# -*- coding: utf-8 -*-
__author__ = 'Administrator'

# 한글처리
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import shutil
#---------------------------------------------------------------
# 정리할 최상위 디렉토리
rootdir = u"C:/align/150102 150122 일상"
#---------------------------------------------------------------
# 지정 폴더의 디렉토리 리스트 반환
def CreateDirList(dirname):
    list = os.listdir(dirname)
    dirlist = []

    for f in list:
        fullpath = os.path.join(dirname, f)
        if os.path.isdir(fullpath):
            dirlist.append(fullpath)
    return dirlist

# 지정 폴더 내부의 모든파일 반환
filelist = []
def dirSearch(dirname):
    first = os.listdir(dirname)
    for f in first:
        next = os.path.join(dirname, f)

        if os.path.isdir(next):
            dirSearch(next)
        else:
            filelist.append(next)

# 로그 기록
logtext = ""
def log(str):
    global logtext
    if not str:
        logtext = logtext + "--- Str IS EMPTY ---" + "\r\n"
        print logtext
    else:
        logtext = logtext + str + "\r\n"
        print logtext

codenum = 0
def DuplicateFile(src, dst):
    global codenum
    if src[-2] != "_":
        addsrc = src + "_" + str(codenum)
        codenum = 0
    else:
        addsrc = src[0:-1] + codenum
        codenum = codenum + 1
    try:
        shutil.move(addsrc, dst)
        log(str(addsrc + " 파일을 " + dst + "로 이동"))
    except shutil.Error:
        DuplicateFile(addsrc, dst)

#---------------------------------------------------------------
# 디렉토리를 넣으면 리스트를 만들어 준다.
dirlist = CreateDirList(rootdir)
for f in dirlist:
    dirSearch(f)
print filelist

# 만들어진 파일 리스트를 순회한다.
for f in filelist:

    #파일을 지정 디렉토리로 이동한다.
    try:
        shutil.move(f, rootdir)
        log(str(f + " 파일을 " + rootdir + "로 이동"))
    #이름이 같을 경우 파일 이름 뒤에 번호 지정
    except shutil.Error:
        DuplicateFile(f, rootdir)
        pass
    #시스템 파일일 경우 패스
    except WindowsError:
        log(str(f + " 파일은 " + rootdir + "로 이동할 수 없습니다."))

#모두 끝나고 로그 저장
with open( rootdir + "/mergeLog.txt", 'wb') as f:
    f.write(logtext)

#--------------------------------------------------------------



