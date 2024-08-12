#to run: python plot.py bitcoin
import sys
import os
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

folder=""

#--------------------------------
args = sys.argv
if len(args)<2:
    print("Error: need argument name of folder with list of nonces")
    exit()

folder=args[1]
print( "Working on \"" + folder +"\"" )
if os.path.isdir(folder)==False:
    print("Error: folder \""+folder+"\" does not exist")
    exit()


stat_N=0
stat=[]
def init_stat():
    global stat
    global stat_N
    stat_N=0
    i=0
    while i<64:
       stat.append([])
       i=i+1

def draw_stat(start_bit,ax=None):
    print("draw_stat ",start_bit)
    save_single=0
    if ax is None:
        fig = plt.figure( figsize=(16,9))
        ax = fig.gca()
        save_single=1
    ax.set_yticks( np.arange( 0.0, 1.0, 0.1 ) )
    plt.title("Probability of specific bit in nonce")
    plt.ylabel("Probability")
    plt.xlabel("Every X-point presents group nonces averaged")
    plt.ylim(0.0,1.0)
    plt.grid()
    i=0
    while i<8:
        color="#"
        if i&1:
            color=color+"FF"
        else:
            color=color+"00"
        if i&2:
            color=color+"FF"
        else:
            color=color+"00"
        if i&4:
            color=color+"FF"
        else:
            color=color+"00"
        if i==7:
            color="#A0A0A0"
        ax.plot(stat[start_bit+i],color,label="bit"+str(start_bit+i) )
        i=i+1
    ax.legend(loc="upper left",ncol=2)
    #plt.show()
    if save_single :
        plt.savefig(folder+"/bit"+str(start_bit)+"-"+str(start_bit+7)+".png",dpi=300)

def draw_hist(start_bit,ax=None):
    print("draw_hist ",start_bit)
    save_single=0
    if ax is None:
        fig = plt.figure( figsize=(16,9))
        ax = fig.gca()
        save_single=1
    ax.set_xticks( np.arange( 0.0, 1.0, 0.1 ) )
    x=np.arange( 0.0, 1.0, 0.05 )
    plt.title("Probability Density of specific bit in nonce")
    plt.ylabel("Density")
    plt.xlabel("Probability")
    plt.grid()
    i=0
    max_val=0
    while i<8:
        histogram=[0]*20
        k=0
        stat_column=stat[start_bit+i]
        n=len(stat_column)
        while k<n:
            val=stat_column[k]
            idx=int(round(val*20))
            histogram[idx]=histogram[idx]+1
            if max_val<histogram[idx]:
                max_val=histogram[idx];
            k=k+1
        color="#"
        if i&1:
            color=color+"FF"
        else:
            color=color+"00"
        if i&2:
            color=color+"FF"
        else:
            color=color+"00"
        if i&4:
            color=color+"FF"
        else:
            color=color+"00"
        if i==7:
            color="#A0A0A0"
        ax.plot(x,histogram,color,label="bit"+str(start_bit+i) )
        i=i+1
    plt.ylim(0.0,max_val*1.2)
    ax.set_yticks( np.arange( 0.0, max_val*1.2, 1.0 ) )
    ax.legend(loc="upper right")
    #plt.show()
    if save_single :
        plt.savefig(folder+"/density"+str(start_bit)+"-"+str(start_bit+7)+".png",dpi=300)

num_bits=32
init_stat()
f = open(folder+"/stat.txt","r")
content = f.read().split("\n")
for line in content:
    word = line.split(" ")
    nb=len(word)-1
    if nb==32 or nb==64:
        num_bits=nb
    else:
        break
    i=0
    while i<num_bits:
        stat[i].append( float(word[i]) )
        i=i+1
f.close

print("Num Bits in Nonce:",num_bits)
draw_hist(0)
draw_hist(8)
draw_hist(16)
draw_hist(24)
add_subplots = 0

fig = plt.figure( figsize=(16,9*num_bits/32))
ax1 = plt.subplot(221+add_subplots)
draw_hist(0,ax1)
ax2 = plt.subplot(222+add_subplots)
draw_hist(8,ax2)
ax3 = plt.subplot(223+add_subplots)
draw_hist(16,ax3)
ax4 = plt.subplot(224+add_subplots)
draw_hist(24,ax4)
plt.savefig(folder+"/density_all.png",dpi=300)

draw_stat(0)
draw_stat(8)
draw_stat(16)
draw_stat(24)
fig = plt.figure( figsize=(16,9*num_bits/32))
ax1 = plt.subplot(221+add_subplots)
draw_stat(0,ax1)
ax2 = plt.subplot(222+add_subplots)
draw_stat(8,ax2)
ax3 = plt.subplot(223+add_subplots)
draw_stat(16,ax3)
ax4 = plt.subplot(224+add_subplots)
draw_stat(24,ax4)
plt.savefig(folder+"/bits_all.png",dpi=300)