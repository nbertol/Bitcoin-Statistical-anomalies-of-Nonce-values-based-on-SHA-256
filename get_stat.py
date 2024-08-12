#to run: python get_stat.py bitcoin
import sys
import os

folder=""
stat_N=0
stat=[]
def init_stat():
    global stat
    global stat_N
    stat_N=0
    i=0
    while i<64:
       stat.append(0.0)
       i=i+1

def clear_stat():
    global stat
    global stat_N
    stat_N=0
    i=0
    while i<64:
       stat[i]=0.0
       i=i+1

def add_stat(nonce):
    global stat
    global stat_N
    stat_N=stat_N+1
    i=0
    while i<64:
        if nonce & (1<<i):
            stat[i]=stat[i]+1
        i=i+1

def nonce_num_bits():
    i=32
    while i<64:
        if stat[i]:
            return 64
        i=i+1
    return 32

def print_stat():
    global stat
    global stat_N
    i=0
    sz = nonce_num_bits()
    while i<sz:
        print(i," ",stat[i]/stat_N)
        i=i+1

def init_stat_file():
    global folder
    txt=open(folder+"/stat.txt","w")
    txt.close()

def write_stat():
    global folder
    global stat
    global stat_N
    txt=open(folder+"/stat.txt","a")
    i=0
    sz = nonce_num_bits()
    while i<sz:
        s=stat[i]/stat_N
        txt.write("%.2f " % s )
        i=i+1
    txt.write("\n")
    txt.close()

#--------------------------------
args = sys.argv
if len(args)<2:
    print("Error: need argument name of folder with list of nonces")
    exit()

# Set the folder name directly
folder = "bitcoin"

print("Working on \"" + folder + "\"")
if os.path.isdir(folder) == False:
    print("Error: folder \"" + folder + "\" does not exist")
    exit()


folder=args[1]
print( "Working on \"" + folder +"\"" )
if os.path.isdir(folder)==False:
    print("Error: folder \""+folder+"\" does not exist")
    exit()

init_stat()
init_stat_file()

f = open(folder+"/nonces.txt","r")
content = f.read().split("\n")
for line in content:
    word = line.split(" ")
    if len(word)<2:
        break
    nonce=int(word[1],16)
    add_stat(nonce)
    if stat_N==100:
        write_stat()
        clear_stat()

f.close