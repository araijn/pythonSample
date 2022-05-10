""" tail 先頭に説明文入れないと警告が出る """
import sys
import getopt
import os
import time

class TailBuffer:
    """ 最後のn行分を保持するためのBuffer クラスの説明を入れないと警告が出る """
    def __init__(self, max_line):
        self.max_line = max_line # javaではmaxLineだがpythonだとmax_lineが主流
        self.buffer = []

    def push(self, obj):
        """ bufferへ追記 メソッドの説明を入れないと警告が出る """
        if len(self.buffer) >= self.max_line:
            self.buffer.pop(0)
        self.buffer.append(obj)

    def pop_all(self):
        """ 保持分の出力 """
        return self.buffer

# python的には静的定義変数名は大文字であるべきというポリシーらしい
# Constant name "count" doesn't conform to UPPER_CASE naming style
DEFAULT_COUNT = 10
DEFAULT_ENCORDING = "utf-8"
DEFAULT_TRACKING = False

# オプションの指定
#  :をつけると引数有り
opts, args = getopt.getopt(sys.argv[1:], "fn:e:")
if not args:  # not len(args)とやると警告が出る リストが空でないときの条件はif args: とやれば良い
    print("usage: python tail.py " +
           "[option -n count -e encording(utf-8/shift_jis/euc-jp) -f : tracking mode] filename")
    sys.exit(1)

filename = args[0]
ino = os.stat(filename).st_ino
count = DEFAULT_COUNT          # こうやっても結局UPPER_CASE naming style警告はでる .pylintrcで無効化も可能
encording = DEFAULT_ENCORDING
tracking = DEFAULT_TRACKING

for opt, value in opts:
    if opt == "-n":
        count = int(value)
    elif opt == "-e":
        encording = value
    elif opt == "-f":
        tracking = True

lines = TailBuffer(count)

with open(filename, 'r', encoding=encording) as f:
    while True:
        line = f.readline()
        if line == '':
            seeksize = f.tell()  # 読込バイト数の保存 この数は\rなどreadlineで取り除かれた文字のバイト数も含まれる
            break
        lines.push(line)

for l in lines.pop_all():
    print(l.rstrip('\n'))

if not tracking:
    sys.exit(0)

filesize = seeksize

while True:
    time.sleep(1)
    if not os.path.exists(filename):
        continue
    nowsize = os.path.getsize(filename)
    now_ino = os.stat(filename).st_ino
    if ino != now_ino:  # ローリングによりファイルが新しいものにスイッチした場合
        seeksize = 0
        ino = now_ino
    else:
        if nowsize == filesize:
            continue
        elif nowsize > filesize:
            filesize = nowsize
        else:
            print("file is modifed")
            sys.exit(1)
    filesize = nowsize
    with open(filename, 'r', encoding=encording) as f:
        f.seek(seeksize)
        while True:
            line = f.readline()
            if line == '':
                seeksize = f.tell()
                break
            print(line.rstrip('\n'))

# tips
# 当初は読み込んだ文字列のバイト数を保存していたが実際のファイルサイズとずれていた → \r\nの\r分だと思われる
# 試験で手動ファイル変更した場合微妙にseek位置がズレることもあった → エディタでtail対象ファイルを開いていた影響か？
