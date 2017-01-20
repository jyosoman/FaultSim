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
    f = open('output/'+str(i)+"rand.txt", 'w')
    while not the_queue.empty():
        lock.acquire()
        if not the_queue.empty():
            l = the_queue.get(False)
        else:
            lock.release()
            break
        lock.release()
        for j in range(0,42):
            print l,j
#            call(["./build/test/bmTestAdder.exe",l[0]+i+".Adder.txt",(l[1]),str(int(l[1])+1),str(j),l[0]],stdout=f)




for i in range(0,210,1):
        lists=[]
        lists.append("rand")
        # strv="ef"+str(i)+".txt"
        lists.append(str(i*12))
        the_queue.put(list(lists))
for i in range(31):
    p=Process(target=f, args=(str(i),))
    p.start()
