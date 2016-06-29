import socket
import networkx as nx
from amertattoo.core.combinational.basic_components import Adder32Bit_Kogge_Stone, \
    Adder2Bit, dec7to128, Adder32Bit_Brent_Kung, Adder32Bit_Ladner_Fischer
from amertattoo.core.combinational.circuit_timing_analysis import CircuitAgeingData, loadAdder32Data, \
loadDecoder7to128Data, loadAdder2Data
from amertattoo.core.combinational.plotting import ImgLayoutMgr
import pylab as plt
from amertattoo.core.failure_mechanisms import Params
import numpy as np
from networkx.algorithms.simple_paths import all_simple_paths
import os
from collections import defaultdict
from matplotlib.figure import Figure

import traceback


#===============================================================================
# #Majjjjic
# oldFigureInit = Figure.__init__
# def newFigInit(*args,**kwargs):
#     print("newFigInit")
#     
#     for line in traceback.format_stack():
#         print(line.strip())
#     
#     return oldFigureInit(*args,**kwargs)
# Figure.__init__ = newFigInit
#===============================================================================




hostname = socket.gethostname()
if hostname == 'NEGAR':
    dir_name = 'E:\\benchMarks\\'
elif hostname =='london.cl.cam.ac.uk':
    dir_name = '/local/scratch/nm537/AgeingModel/TransistorModel/sample_bench_for_test/'
elif hostname =='oslo.cl.cam.ac.uk':
    dir_name = '/local/scratch-2/nm537/benchmarks/'
else:
    raise RuntimeError("I don't know this machine: %s" % hostname )


def main():
    print("Started")
    adder = Adder2Bit(name='add2bit')

    for (inputIdx, inputs) in enumerate( adder.generateAllInputDictsToBlock() ): 
        print inputs

        #
        intermed_signals = adder.simulate_all(inputs)
        
        
        wireSet = adder.get_wireset()
        wireMap = wireSet.getWireColorMap(intermed_signals)
        
        colorMap = { 
            True:(0.8,0.2,0.2),
            False:(0.8,0.8,0.8),
        }
        
        wireColorMap = { wire: colorMap[wireState] for (wire,wireState) in wireMap.items()}
        
        
        ImgLayoutMgr(adder, wireSet, wireColorMap).render(dir_name + r"adder2_out%02d.png" % inputIdx)
        
def decimal_bin(adder, num1, num2, carry_in):
    
    
    # Now, break input1 into 'vin_a0, vin_a1, vin_a2, vin_a3, vin_a4, '
    inputDict = {
           'vin_cin': np.zeros_like(carry_in).astype(bool), 
        } 
    for i in range(32):
        inputDict['vin_a%d'%i] =  np.bitwise_and(num1, 1<<i).astype(bool)
        inputDict['vin_b%d'%i] =  np.bitwise_and(num2, 1<<i).astype(bool)
    
    res = adder.simulate_all(inputDict)
    print res.keys()
    outsum = 0
    for i in range(32):
        outsum = np.bitwise_or(outsum, res['add32bit.s%d'%i]<<i)
    print num1, num2, outsum
    
def path_delay_calculations():
    pass
    
def call_decoder7to128(srcFilename, portnum):
            
    decoder = dec7to128(name = 'decoder7_128')
    circuitAgeingData_decoder = CircuitAgeingData(decoder, ageing_time = 3*365*24*60*60.0, params = Params(Vth = 0.49155, T_ox = 1.15e-009))
    circuitAgeingData_decoder.add_gem5_source(
                    "decoder7_128", 
                    loadDecoder7to128Data(srcFilename = srcFilename, usePort=portnum)
                    )
          
    #Further analysis
    for trans_name, trans_trans_table in circuitAgeingData_decoder.transistor_transition_tables.items():
        print( "%s %s" % (trans_name, trans_trans_table ) ) 

    xlabels = []
    initialDelays = []
    finalDelays = []   
    path_tot_graphs = defaultdict(list)
    path_init_graphs = defaultdict(list)
    for path, (sourceName, destName) in sorted(decoder.all_paths(), key=str):
        #print len(path)
        #if (len(path) == 19):
        init_totTime = np.sum( [circuitAgeingData_decoder.params.initDelay for gate in path] )
        print("Between: %s and %s len %d and init %2.12f" % (sourceName, destName, len(path), init_totTime) )
        totTime = np.sum( [circuitAgeingData_decoder.getDelayGate(gate) for gate in path] )
        #print " -- (%.10f)" % totTime, path
        xlabels.append(str(path))
        initialDelays.append(init_totTime)
        finalDelays.append(totTime)
        path_tot_graphs[len(path)].append(totTime)
        path_init_graphs[len(path)].append(init_totTime)

    allData = zip(initialDelays, finalDelays)
    allData = sorted(allData)
    #print(allData)
    initialDelays, finalDelays = zip(*allData)
     
    f, ax = plt.subplots(1)
    ax.plot(finalDelays, "rx-")
    ax.bar(range(len(initialDelays)), initialDelays, alpha = 0.5, linewidth=0, align = "center")
    ax.set_xlim(-0.5,len(initialDelays))
    ax.set_ylim(0, 2.3e-10)
    f.tight_layout()
    plt.savefig(dir_name + "h264ref_fbase/" + decoder.name + "_" + "barchart.png")
 
    plt.show()

def call_adder2bit(srcFilename, portnum):
    adder = Adder2Bit(name = 'add2bit')
    circuitAgeingData_adder = CircuitAgeingData(adder, ageing_time = 3*365*24*60*60.0, params = Params(Vth = 0.49155, T_ox = 1.15e-009))
    circuitAgeingData_adder.add_gem5_source(
                    "add2bit", 
                    loadAdder2Data(srcFilename = dir_name + "system.switch_cpus.iew.adder", usePort=0)
                    )     
    
def call_adder32bit(srcFilename, portnum):

    #check the adder actually works
    #print 'Kogge_Stone'
    #decimal_bin(adder, 2147483647, 2147483647, False)
    #print 'Brent_Kung'
    #decimal_bin(adder1, 2147483647, 2147483647, False)
    #print 'Ladner_Fischer'
    #decimal_bin(adder2, 2147483647, 2147483647, False)
    
    #adder = Adder32Bit_Brent_Kung(name='add32bit')
    #adder = Adder32Bit_Ladner_Fischer(name='add32bit')
    adder = Adder32Bit_Kogge_Stone(name='add32bit')
    circuitAgeingData_adder = CircuitAgeingData(adder, ageing_time = 3*365*24*60*60.0, params = Params(Vth = 0.49155, T_ox = 1.15e-009))
    circuitAgeingData_adder.add_gem5_source(
                    "add32bit", 
                    loadAdder32Data(srcFilename = srcFilename, usePort=portnum)
                    )
    
    
    #with open("D:/tmp/newTables.txt",'w') as fObj:
    for trans_name, trans_trans_table in circuitAgeingData_adder.transistor_transition_tables.items():
        print( "%s %s\n" % (trans_name, trans_trans_table ) )

    xlabels = []
    initialDelays = []
    finalDelays = []   
    path_tot_graphs = defaultdict(list)
    path_init_graphs = defaultdict(list)
    for path, (sourceName, destName) in sorted(adder.all_paths(), key=str):
        #print len(path)
        #if (len(path) == 19):
        init_totTime = np.sum( [circuitAgeingData_adder.params.initDelay for gate in path] )
        print("Between: %s and %s len %d and init %2.12f" % (sourceName, destName, len(path), init_totTime) )
        totTime = np.sum( [circuitAgeingData_adder.getDelayGate(gate) for gate in path] )
        #print " -- (%.10f)" % totTime, path
        xlabels.append(str(path))
        initialDelays.append(init_totTime)
        finalDelays.append(totTime)
        path_tot_graphs[len(path)].append(totTime)
        path_init_graphs[len(path)].append(init_totTime)

    allData = zip(initialDelays, finalDelays)
    allData = sorted(allData)
    #print(allData)
    initialDelays, finalDelays = zip(*allData)
     
    f, ax = plt.subplots(1)
    ax.plot(finalDelays, "rx-")
    ax.bar(range(len(initialDelays)), initialDelays, alpha = 0.5, linewidth=0, align = "center")
    ax.set_xlim(-0.5,len(initialDelays))
    ax.set_ylim(0, 2.3e-10)
    f.tight_layout()
    plt.savefig(dir_name + "h264ref_fbase/" + adder.name + "_" + "barchart.png")
 
    plt.show()
def main_negar():

    #call_decoder7to128(srcFilename = dir_name + "system.switch_cpus.phys_regfile.reg_writes_test", portnum = 2)
    call_adder32bit(srcFilename = dir_name + "lbm/system.switch_cpus.iew.adder", portnum = 0)
    

def test_profile():
    
    import cProfile
    profile = cProfile.Profile()
    profile.run('main_negar()')
    profile.dump_stats('D:/tmp/profile.prof')
    
    os.system("pyprof2calltree -i D:\\tmp\\profile.prof -o D:\\tmp\\out.callGrind")
    

#test_profile()
main_negar()
    
#main()
