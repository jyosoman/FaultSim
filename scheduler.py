from subprocess import call
import ctypes
from multiprocessing import Process, Lock, Queue
lock = Lock()
the_queue = Queue()
import sys

array=["astar_biglakes",
        "bwaves",
        "bzip2_source",
        "cactusADM",
        "calculix",
        "gamess_cytosine",
        "gcc_166",
        "GemsFDTD",
        "gobmk_13x13",
        "gromacs",
        "h264ref_fbase",
        "hmmer_nph3",
        "lbm",
        "leslie3d",
        "libquantum",
        "mcf",
        "milc",
        "namd",
        "omnetpp",
        "perlbench_checkspam",
        "sjeng",
        "soplex_pds50",
        "tonto",
        "zeusmp"]

x=int(sys.argv[1])
val=array[x]
dpoint=sys.argv[2]

def call_c( L ):
        bmTester = ctypes.cdll.LoadLibrary('./build/pythonTesting/bmTestAdder.so')
        arr = (ctypes.c_char_p * (len(L) + 1))()
        bmTester.runMain.restype = ctypes.c_char_p
        arr[:-1] = L
        arr[ len(L) ] = None
        result = bmTester.runMain(len(L),arr)
        del bmTester
        return result

def f(i):
    f = open('workfileSingle'+str(i)+val+dpoint+".txt", 'w')
    while not the_queue.empty():
        lock.acquire()
        if not the_queue.empty():
            l = the_queue.get(False)
        else:
            lock.release()
            break
        lock.release()
        # res=call_c([l[0],"/local/LargeDisk/gem5/takeLogs/pirafix/"+l[0]+".Adder.txt",(l[1]),str(int(l[1])+10)])
        # print >>f, "%d %s",(l, res)
        call(["./build/test/bmTestAdder.exe",l[0]+".Adder.txt",(l[1]),str(int(l[1])+1),dpoint,l[0]],stdout=f)




for i in range(0,230,10):
    lists=[]
    lists.append(val)
    # strv="ef"+str(i)+".txt"
    lists.append(str(i*11))
    # lists.append(strv)
    the_queue.put(list(lists))

for i in range(5):
    Process(target=f, args=(str(i))).start()
