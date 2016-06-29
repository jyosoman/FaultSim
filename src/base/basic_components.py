
import itertools
import networkx as nx
from amertattoo.core.combinational.wire import NetworkWire, WireSet
from amertattoo.core.common.circuit_base import NMOS, PMOS
import numpy as np
from networkx.algorithms.simple_paths import all_simple_paths


# BaseClass
class Gate(object):
    internal_nodes = []
    def __init__(self, name):
        self.name = name
        self.transistors = []
        for trans_name, trans_type in self.class_transistors:
            trans_name_full = self.name + '.' + trans_name
            transistor = trans_type(name = trans_name_full)
            self.transistors.append(transistor)
        #print("Created gate: %s (%s)" % (self.name, type(self) ))

    def printpretty(self, depth):
        print (' ' * depth) + str(self)
        
    def __str__(self):
        return "<%s of %s>" % (self.name, type(self).__name__)
    def __repr__(self):
        return str(self)
        
    def add_to_graph(self, graphObj):
        graphObj.add_node(self.name)

    def get_all_gates(self,):
        return [self]

    @property
    def local_name(self):
        return self.name.split(".")[-1]
    
    def get_all_transistors(self):
        return self.transistors
        
    def get_gate_connections_by_inout_name(self, inout_name):
        return [self]
                
    def get_gate_gate_connections(self):
        return []
    
    def get_all_wires(self):
        assert(0)
        
    def populate_wire(self, wire, connection_name):
        wire.add_gate_connection(self, connection_name)
    
    def generateAllInputDictsToBlock(self):
        inputNames = sorted(self.inputs)
        inputValues = [ [True,False] for _ in inputNames]
        res = []
        for vals in itertools.product(*inputValues):
            res.append( dict(zip(inputNames,vals)))
        return res
    
    def get_gate_logical_effort(self):
        return self.logical_effort 

# Basic Gate templates:
class Inv(Gate):
    inputs = ['vin']
    outputs = ['vout']
    class_transistors = [
                   ('mn', NMOS ), 
                   ('mp', PMOS ),
                   ]
    logical_effort = 1.
    def simulate(self, inputs, save_intermediate_signals=None):
        return {'vout': np.logical_not(inputs['vin']) }
    def get_transistor_input_signal(self, transistor_name, inputDct):
        if   transistor_name in ['mn', 'mp']: return inputDct['vin']
    
class Xor2(Gate):
    inputs = ['vin1', 'vin2']
    outputs = ['vout']
    class_transistors = [
                ('mn7', NMOS),
                ('mp7', PMOS),
                ('mn8', NMOS),
                ('mp8', PMOS),
                ('mn9', NMOS),
                ('mp9', PMOS),
                ('mn10', NMOS),
                ('mp10', PMOS),
                ('mn11', NMOS),
                ('mp11', PMOS)
                   ]
    logical_effort = 4.
    def simulate(self, inputs, save_intermediate_signals=None):
        return {'vout': np.logical_xor(inputs['vin1'], inputs['vin2'])}
    
    def get_transistor_input_signal(self, transistor_name, inputDct):
        if   transistor_name in ['mn7', 'mp7', 'mn10', 'mp10']: return inputDct['vin1']
        elif transistor_name in ['mn8', 'mp8', 'mn11', 'mp11']: return inputDct['vin2']
        elif transistor_name in ['mn9', 'mp9']: return np.logical_not(np.logical_or(inputDct['vin1'], inputDct['vin2']))
        else:
            assert(0)
        
class Nand2(Gate):
    inputs = ['vin1', 'vin2']
    outputs = ['vout']
    class_transistors = [
               ('mn3', NMOS ), 
               ('mp3', PMOS ),
               ('mn4', NMOS ), 
               ('mp4', PMOS )
               ]
    logical_effort = 4./3.
    def simulate(self, inputs, save_intermediate_signals=None):
        return {'vout': np.logical_not(np.logical_and(inputs['vin1'], inputs['vin2']))}
    def get_transistor_input_signal(self, transistor_name, inputDct):
        if   transistor_name in ['mn3', 'mp3']: return inputDct['vin1']
        elif transistor_name in ['mn4', 'mp4']: return inputDct['vin2']
        else: 
            assert(0)

class Nor2(Gate):
    inputs = ['vin1', 'vin2']
    outputs = ['vout']
    class_transistors = [
           ('mn5', NMOS ), 
           ('mp5', PMOS ),
           ('mn6', NMOS ), 
           ('mp6', PMOS )
           ]
    logical_effort = 5./3.
    def simulate(self, inputs, save_intermediate_signals=None):
        return {'vout': np.logical_not(np.logical_or(inputs['vin1'], inputs['vin2']))}
    def get_transistor_input_signal(self, transistor_name, inputDct):
        if   transistor_name in ['mn5', 'mp5']: return inputDct['vin1']
        elif transistor_name in ['mn6', 'mp6']: return inputDct['vin2']
        else: 
            assert(0)


class CombinationalBlock(object):
    def __init__(self, name):
        self.name = name
        self.blks = []
        for (blkName, blk, connections) in self.class_blocks:
            newBlk = blk(name=self.name+"."+blkName)
            #print("Created block: %s (%s)" % (self.name, type(self) ))
            self.blks.append( (newBlk, connections) )
    def __str__(self):
        return "<%s of %s>" % (self.name, type(self).__name__)
    def __repr__(self):
        return str(self)
    
    def printpretty(self, depth=0):
        print (' ' * depth) + str(self)
        for blk, _ in self.blks:
            blk.printpretty(4 + depth)     

    @property
    def local_name(self):
        return self.name.split(".")[-1]
    
    def get_all_gates(self,):
        all_gates = []
        for blk, _ in self.blks:
            all_gates.extend(blk.get_all_gates())
        return all_gates
    
    def get_all_transistors(self,):
        all_trans = []
        for blk, _ in self.blks:
            all_trans.extend(blk.get_all_transistors())
        return all_trans
    
    def get_gate_connections_by_inout_name(self, inout_name):
        """
        """
        gates = []
        for blk, connections in self.blks:
            for key_blk_child_name, value_local_node_name in connections.items():
                    if value_local_node_name == inout_name:
                        gates.extend(blk.get_gate_connections_by_inout_name(key_blk_child_name))
        return gates

    def generateAllInputDictsToBlock(self):
        inputNames = sorted(self.inputs)
        inputValues = [ [True,False] for _ in inputNames]
        res = []
        for vals in itertools.product(*inputValues):
            res.append( dict(zip(inputNames,vals)))
        return res
    
    
    def get_gate_gate_connections(self):
        #returns a list of all the pairs of gates that are connected to each other inside a block
        all_connections = []
        #loop over 
        for blk, connections in self.blks:
            blk_connection = blk.get_gate_gate_connections()
            all_connections.extend(blk_connection)
        for intern_node in self.internal_nodes:
            predecessor_gates = []
            successor_gates = []
            for subBlk, connections in self.blks:
                for key_blk_child_name, value_local_node_name in connections.items():
                    if value_local_node_name == intern_node:
                        gates = subBlk.get_gate_connections_by_inout_name(key_blk_child_name)
                        if key_blk_child_name in subBlk.inputs:
                            successor_gates.extend(gates)
                        else:
                            assert key_blk_child_name in subBlk.outputs
                            predecessor_gates.extend(gates)
            assert(len(predecessor_gates) == 1)
            for suc_node in successor_gates:
                all_connections.append((predecessor_gates[0], suc_node))
        return all_connections
    
    def simulate_all(self, inputs):
        intermeds = {}
        self.simulate(inputs, intermeds)     
        return intermeds
                
    def simulate(self, inputs, save_intermediate_signals=None):
        """
        Simulates an object. The input should be a dictionary, mapping for example
        
            inputs = { 'vin_cin': [False,True, False], 'vin_a0':[True,True,False], ... }
        
        The return value will be another dictionary 
        
            inputs = { 'vout_cout': [False,True, False], 's0':[True,True,False],  's1':[True,True,False], }.
            
        The optional parameter, save_intermediate_signals, is a dictionary, which will be populated with all the
        intermediate values of all the nodes, with full gate-names, e.g.:
            {
                'add2bit.gray0.Gk_1j' : array([ True,  True,  True,  True,  True,  True,  True,  True,  True,])
                'add2bit.gray1.or.vin1': array([False, False, False, False, False, False, False, False, False,]),
                'add2bit.pg1.xor.vout': array([ True, False, False, False, False,  True, False, False, False,])
                'add2bit.gray1.grayMid', array([ True, False, False, False, False,  True, False, False, False]),
            }
       
        """
        
        nodeValues = inputs.copy()
        
        for (blk, connections) in self.blks:
            #print blk, connections
            blkInputDict = dict( [ (k, nodeValues[v]) for (k,v) in connections.items() if k in blk.inputs] )
            
            blkOutputDict = blk.simulate(blkInputDict, save_intermediate_signals=save_intermediate_signals)
            
            
            # Copy new values into nodeValues:
            for rName, rValue in blkOutputDict.items():
                localName = connections[rName]
                nodeValues[localName] = rValue
            
            # Save the intermediate variables    
            if save_intermediate_signals is not None:
                for (k,v) in blkInputDict.items():
                    save_intermediate_signals[blk.name + "." + k] = v
                for (k,v) in blkOutputDict.items():
                    save_intermediate_signals[blk.name + "." + k] = v
            
        
        
        # Save the intermediate signals?
        if save_intermediate_signals is not None:
            for (k,v) in nodeValues.items():
                save_intermediate_signals[self.name + "." + k] = v
                
        
        # Return the output-values:
        results = {}
        for opName in self.outputs:
            results[opName] = nodeValues[opName]
        return results
    
    def add_to_graph(self, graphObj):
        
        # Add all the child nodes:
        for blk, connections in self.blks:
            blk.add_to_graph(graphObj)

        # Add 'fake nodes' for the inputs, outputs, and internal_nodes:
        for interfaceNode in (self.inputs+self.outputs+self.internal_nodes):
            graphObj.add_node( "_" + self.name+ "." + interfaceNode)

        for blk, connections in self.blks:
            # Need to handle block/gate slightly differently:
            if isinstance(blk, Gate):
                for gateConnection, localConnectionName in connections.items():
                    localPortName = "_" + self.name+ "." + localConnectionName
                    
                    if gateConnection in blk.inputs:
                        graphObj.add_edge(localPortName, blk.name )
                    else:
                        assert gateConnection in blk.outputs
                        graphObj.add_edge(blk.name, localPortName )
                        
            elif isinstance(blk, CombinationalBlock):
                for blkConnection, localConnectionName in connections.items():
                    localPortName = "_" + self.name+ "." + localConnectionName
                    blockPortName = "_" + blk.name+ "." + blkConnection
                    if blkConnection in blk.inputs:
                        graphObj.add_edge(localPortName, blockPortName)
                    else:
                        assert blkConnection in blk.outputs
                        graphObj.add_edge(blockPortName, localPortName)



    def get_wireset(self):
        wires = {}
        # We will get a wire per node:
        for localNodeName in self.inputs + self.outputs + self.internal_nodes:
            wires[localNodeName] = NetworkWire()
            wires[localNodeName].add_block_connection(self, localNodeName)
        return WireSet(wires.values())
        
    def all_paths(self):
        ageing_graph = nx.DiGraph()
        for gate in self.get_all_gates():
            ageing_graph.add_node(gate)
        for gate0, gate1 in self.get_gate_gate_connections():
            print gate0, gate1
            ageing_graph.add_edge(gate0, gate1)
            
        graph_source_nodes = []
        graph_dest_nodes = []
        for inputName in self.inputs:
            graph_source_nodes.extend( self.get_gate_connections_by_inout_name(inputName) )
        for outputName in self.outputs:
            graph_dest_nodes.extend( self.get_gate_connections_by_inout_name(outputName) )
            
        graph_source_nodes = list(set(graph_source_nodes))
        #print "graph_source_nodes: ", graph_source_nodes
        graph_dest_nodes = list(set(graph_dest_nodes))
        #print "graph_dest_nodes: ", graph_dest_nodes
        #graph_source_nodes = [node for node in ageing_graph.nodes() if not ageing_graph.predecessors(node)]
        #print graph_source_nodes
        #graph_dest_nodes = [node for node in ageing_graph.nodes() if not ageing_graph.successors(node)]
        #print "paths: "
        for source in graph_source_nodes:
            for dest in graph_dest_nodes:
                #if there is one gate on a path, the simple path function returns null, so we need to fix it here
                if source == dest:
                    paths = [[source]]
                else:
                    paths = list(all_simple_paths(ageing_graph, source, dest))
                
                if paths:
                    #print("Between: %s and %s" % (source, dest) )
                    for path in paths:
                        yield path, (source, dest)
    

# 'Derived' gate templates:
class Or2(CombinationalBlock):
    inputs = ['vin1', 'vin2']
    outputs = ['vout']
    internal_nodes = ['mid']
    class_blocks = [
        ('nor', Nor2, {'vin1': 'vin1', 'vin2': 'vin2', 'vout': 'mid'}),
        ('inv', Inv,  {'vin': 'mid', 'vout': 'vout'}),
        ]       
    
class And2(CombinationalBlock):
    inputs = ['vin1', 'vin2']
    outputs = ['vout']
    internal_nodes = ['mid']
    class_blocks = [
                ('nand', Nand2, {'vin1': 'vin1', 'vin2': 'vin2', 'vout': 'mid'}),
                ('inv', Inv,    {'vin': 'mid', 'vout': 'vout'})
                ]


class dec2to4(CombinationalBlock):
    inputs = ['vin1', 'vin2']
    outputs = ['vout1', 'vout2', 'vout3', 'vout4']
    internal_nodes = ['vin1_bar', 'vin2_bar']
    class_blocks = [
                ('inv1', Inv,  {'vin': 'vin1', 'vout': 'vin1_bar'}),
                ('inv2', Inv,  {'vin': 'vin2', 'vout': 'vin2_bar'}),
                ('and1', And2, {'vin1': 'vin1_bar', 'vin2': 'vin2_bar', 'vout': 'vout1'}),
                ('and2', And2, {'vin1': 'vin1', 'vin2': 'vin2_bar', 'vout': 'vout2'}),
                ('and3', And2, {'vin1': 'vin1_bar', 'vin2': 'vin2', 'vout': 'vout3'}),
                ('and4', And2, {'vin1': 'vin1', 'vin2': 'vin2', 'vout': 'vout4'}),
                ]

class dec2to4_EN(CombinationalBlock):
    inputs = ['vin1', 'vin2', 'EN']
    outputs = ['vout1', 'vout2', 'vout3', 'vout4']
    internal_nodes = ['vin1_bar', 'vin2_bar', 'Y0', 'Y1', 'Y2', 'Y3']
    class_blocks = [
                ('inv1', Inv,    {'vin': 'vin1', 'vout': 'vin1_bar'}),
                ('inv2', Inv,    {'vin': 'vin2', 'vout': 'vin2_bar'}),
                ('and1_1', And2, {'vin1': 'vin1_bar', 'vin2': 'vin2_bar', 'vout': 'Y0'}),
                ('and2_1', And2, {'vin1': 'vin1', 'vin2': 'vin2_bar', 'vout': 'Y1'}),
                ('and3_1', And2, {'vin1': 'vin1_bar', 'vin2': 'vin2', 'vout': 'Y2'}),
                ('and4_1', And2, {'vin1': 'vin1', 'vin2': 'vin2', 'vout': 'Y3'}),
                ('and1_2', And2, {'vin1': 'Y0', 'vin2': 'EN', 'vout': 'vout1'}),
                ('and2_2', And2, {'vin1': 'Y1', 'vin2': 'EN', 'vout': 'vout2'}),
                ('and3_2', And2, {'vin1': 'Y2', 'vin2': 'EN', 'vout': 'vout3'}),
                ('and4_2', And2, {'vin1': 'Y3', 'vin2': 'EN', 'vout': 'vout4'}),
                ]
    

class dec3to8(CombinationalBlock):
    inputs = ['vin1', 'vin2', 'vin3']
    outputs = ['vout1', 'vout2', 'vout3', 'vout4', 'vout5', 'vout6', 'vout7', 'vout8']
    internal_nodes = ['vin3_bar', ]
    class_blocks = [
                ('inv', Inv,            {'vin': 'vin3', 'vout': 'vin3_bar'}),
                ('dec24_1', dec2to4_EN, {'vin1': 'vin1', 'vin2': 'vin2', 'EN': 'vin3_bar', 
                                         'vout1': 'vout1', 'vout2': 'vout2', 
                                         'vout3': 'vout3', 'vout4': 'vout4'}),
                ('dec24_2', dec2to4_EN, {'vin1': 'vin1', 'vin2': 'vin2', 'EN': 'vin3', 
                                         'vout1': 'vout5', 'vout2': 'vout6', 
                                         'vout3': 'vout7', 'vout4': 'vout8'}),
                ]

class dec4to16(CombinationalBlock):
    inputs = ['vin1', 'vin2', 'vin3', 'vin4']
    outputs = [
               'vout1', 'vout2', 'vout3', 'vout4', 'vout5', 'vout6', 'vout7', 'vout8',
               'vout9', 'vout10', 'vout11', 'vout12', 'vout13', 'vout14', 'vout15', 'vout16'
               ]
    internal_nodes = ['EN1', 'EN2', 'EN3', 'EN4']
    class_blocks = [
                ('dec24_EN', dec2to4,   {'vin1': 'vin3', 'vin2': 'vin4', 'vout1': 'EN1', 
                                         'vout2': 'EN2', 'vout3': 'EN3', 'vout4': 'EN4'}),
                ('dec24_1', dec2to4_EN, {'vin1': 'vin1', 'vin2': 'vin2', 'EN': 'EN1', 
                                         'vout1': 'vout1', 'vout2': 'vout2', 'vout3': 'vout3', 'vout4': 'vout4'}),
                ('dec24_2', dec2to4_EN, {'vin1': 'vin1', 'vin2': 'vin2', 'EN': 'EN2', 
                                         'vout1': 'vout5', 'vout2': 'vout6', 'vout3': 'vout7', 'vout4': 'vout8'}),
                ('dec24_3', dec2to4_EN, {'vin1': 'vin1', 'vin2': 'vin2', 'EN': 'EN3', 
                                         'vout1': 'vout9', 'vout2': 'vout10', 'vout3': 'vout11', 'vout4': 'vout12'}),
                ('dec24_4', dec2to4_EN, {'vin1': 'vin1', 'vin2': 'vin2', 'EN': 'EN4', 
                                         'vout1': 'vout13', 'vout2': 'vout14', 'vout3': 'vout15', 'vout4': 'vout16'}),
                ]
    
class dec7to128(CombinationalBlock):
    inputs = ['vin1', 'vin2', 'vin3', 'vin4', 'vin5', 'vin6', 'vin7']
    outputs = [
               'vout1', 'vout2', 'vout3', 'vout4', 'vout5', 'vout6', 'vout7', 'vout8',
               'vout9', 'vout10', 'vout11', 'vout12', 'vout13', 'vout14', 'vout15', 'vout16',
               'vout17', 'vout18', 'vout19', 'vout20', 'vout21', 'vout22', 'vout23', 'vout24',
               'vout25', 'vout26', 'vout27', 'vout28', 'vout29', 'vout30', 'vout31', 'vout32',
               'vout33', 'vout34', 'vout35', 'vout36', 'vout37', 'vout38', 'vout39', 'vout40',
               'vout41', 'vout42', 'vout43', 'vout44', 'vout45', 'vout46', 'vout47', 'vout48',
               'vout49', 'vout50', 'vout51', 'vout52', 'vout53', 'vout54', 'vout55', 'vout56',
               'vout57', 'vout58', 'vout59', 'vout60', 'vout61', 'vout62', 'vout63', 'vout64',
               'vout65', 'vout66', 'vout67', 'vout68', 'vout69', 'vout70', 'vout71', 'vout72',
               'vout73', 'vout74', 'vout75', 'vout76', 'vout77', 'vout78', 'vout79', 'vout80',
               'vout81', 'vout82', 'vout83', 'vout84', 'vout85', 'vout86', 'vout87', 'vout88',
               'vout89', 'vout90', 'vout91', 'vout92', 'vout93', 'vout94', 'vout95', 'vout96',
               'vout97', 'vout98', 'vout99', 'vout100', 'vout101', 'vout102', 'vout103', 'vout104',
               'vout105', 'vout106', 'vout107', 'vout108', 'vout109', 'vout110', 'vout111', 'vout112',
               'vout113', 'vout114', 'vout115', 'vout116', 'vout117', 'vout118', 'vout119', 'vout120',
               'vout121', 'vout122', 'vout123', 'vout124', 'vout125', 'vout126', 'vout127', 'vout128',
               ]
    internal_nodes = [
                      'Y0', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'Y9', 'Y10', 'Y11',
                      'Y12', 'Y13', 'Y14', 'Y15', 'Y16', 'Y17', 'Y18', 'Y19', 'Y20', 'Y21', 'Y22', 'Y23',
                      ]
    class_blocks = [
                ('dec3_8', dec3to8,   {'vin1': 'vin1', 'vin2': 'vin2', 'vin3': 'vin3', 
                                       'vout1': 'Y0', 'vout2': 'Y1', 'vout3': 'Y2', 'vout4': 'Y3', 
                                       'vout5': 'Y4', 'vout6': 'Y5', 'vout7': 'Y6', 'vout8': 'Y7'}),
                ('dec4_16', dec4to16, {'vin1': 'vin4', 'vin2': 'vin5', 'vin3': 'vin6', 'vin4': 'vin7', 
                                       'vout1': 'Y8', 'vout2': 'Y9', 'vout3': 'Y10', 'vout4': 'Y11', 
                                       'vout5': 'Y12', 'vout6': 'Y13', 'vout7': 'Y14', 'vout8': 'Y15', 
                                       'vout9': 'Y16', 'vout10': 'Y17', 'vout11': 'Y18', 'vout12': 'Y19', 
                                       'vout13': 'Y20', 'vout14': 'Y21', 'vout15': 'Y22', 'vout16': 'Y23'}),
                ('and_1', And2, {'vin1': 'Y0', 'vin2': 'Y8', 'vout': 'vout1'}),
                ('and_2', And2, {'vin1': 'Y1', 'vin2': 'Y8', 'vout': 'vout2'}),
                ('and_3', And2, {'vin1': 'Y2', 'vin2': 'Y8', 'vout': 'vout3'}),
                ('and_4', And2, {'vin1': 'Y3', 'vin2': 'Y8', 'vout': 'vout4'}),
                ('and_5', And2, {'vin1': 'Y4', 'vin2': 'Y8', 'vout': 'vout5'}),
                ('and_6', And2, {'vin1': 'Y5', 'vin2': 'Y8', 'vout': 'vout6'}),
                ('and_7', And2, {'vin1': 'Y6', 'vin2': 'Y8', 'vout': 'vout7'}),
                ('and_8', And2, {'vin1': 'Y7', 'vin2': 'Y8', 'vout': 'vout8'}),
                ('and_9', And2, {'vin1': 'Y0', 'vin2': 'Y9', 'vout': 'vout9'}),
                ('and_10', And2, {'vin1': 'Y1', 'vin2': 'Y9', 'vout': 'vout10'}),
                ('and_11', And2, {'vin1': 'Y2', 'vin2': 'Y9', 'vout': 'vout11'}),
                ('and_12', And2, {'vin1': 'Y3', 'vin2': 'Y9', 'vout': 'vout12'}),
                ('and_13', And2, {'vin1': 'Y4', 'vin2': 'Y9', 'vout': 'vout13'}),
                ('and_14', And2, {'vin1': 'Y5', 'vin2': 'Y9', 'vout': 'vout14'}),
                ('and_15', And2, {'vin1': 'Y6', 'vin2': 'Y9', 'vout': 'vout15'}),
                ('and_16', And2, {'vin1': 'Y7', 'vin2': 'Y9', 'vout': 'vout16'}),
                ('and_17', And2, {'vin1': 'Y0', 'vin2': 'Y10', 'vout': 'vout17'}),
                ('and_18', And2, {'vin1': 'Y1', 'vin2': 'Y10', 'vout': 'vout18'}),
                ('and_19', And2, {'vin1': 'Y2', 'vin2': 'Y10', 'vout': 'vout19'}),
                ('and_20', And2, {'vin1': 'Y3', 'vin2': 'Y10', 'vout': 'vout20'}),
                ('and_21', And2, {'vin1': 'Y4', 'vin2': 'Y10', 'vout': 'vout21'}),
                ('and_22', And2, {'vin1': 'Y5', 'vin2': 'Y10', 'vout': 'vout22'}),
                ('and_23', And2, {'vin1': 'Y6', 'vin2': 'Y10', 'vout': 'vout23'}),
                ('and_24', And2, {'vin1': 'Y7', 'vin2': 'Y10', 'vout': 'vout24'}),
                ('and_25', And2, {'vin1': 'Y0', 'vin2': 'Y11', 'vout': 'vout25'}),
                ('and_26', And2, {'vin1': 'Y1', 'vin2': 'Y11', 'vout': 'vout26'}),
                ('and_27', And2, {'vin1': 'Y2', 'vin2': 'Y11', 'vout': 'vout27'}),
                ('and_28', And2, {'vin1': 'Y3', 'vin2': 'Y11', 'vout': 'vout28'}),
                ('and_29', And2, {'vin1': 'Y4', 'vin2': 'Y11', 'vout': 'vout29'}),
                ('and_30', And2, {'vin1': 'Y5', 'vin2': 'Y11', 'vout': 'vout30'}),
                ('and_31', And2, {'vin1': 'Y6', 'vin2': 'Y11', 'vout': 'vout31'}),
                ('and_32', And2, {'vin1': 'Y7', 'vin2': 'Y11', 'vout': 'vout32'}),
                ('and_33', And2, {'vin1': 'Y0', 'vin2': 'Y12', 'vout': 'vout33'}),
                ('and_34', And2, {'vin1': 'Y1', 'vin2': 'Y12', 'vout': 'vout34'}),
                ('and_35', And2, {'vin1': 'Y2', 'vin2': 'Y12', 'vout': 'vout35'}),
                ('and_36', And2, {'vin1': 'Y3', 'vin2': 'Y12', 'vout': 'vout36'}),
                ('and_37', And2, {'vin1': 'Y4', 'vin2': 'Y12', 'vout': 'vout37'}),
                ('and_38', And2, {'vin1': 'Y5', 'vin2': 'Y12', 'vout': 'vout38'}),
                ('and_39', And2, {'vin1': 'Y6', 'vin2': 'Y12', 'vout': 'vout39'}),
                ('and_40', And2, {'vin1': 'Y7', 'vin2': 'Y12', 'vout': 'vout40'}),
                ('and_41', And2, {'vin1': 'Y0', 'vin2': 'Y13', 'vout': 'vout41'}),
                ('and_42', And2, {'vin1': 'Y1', 'vin2': 'Y13', 'vout': 'vout42'}),
                ('and_43', And2, {'vin1': 'Y2', 'vin2': 'Y13', 'vout': 'vout43'}),
                ('and_44', And2, {'vin1': 'Y3', 'vin2': 'Y13', 'vout': 'vout44'}),
                ('and_45', And2, {'vin1': 'Y4', 'vin2': 'Y13', 'vout': 'vout45'}),
                ('and_46', And2, {'vin1': 'Y5', 'vin2': 'Y13', 'vout': 'vout46'}),
                ('and_47', And2, {'vin1': 'Y6', 'vin2': 'Y13', 'vout': 'vout47'}),
                ('and_48', And2, {'vin1': 'Y7', 'vin2': 'Y13', 'vout': 'vout48'}),
                ('and_49', And2, {'vin1': 'Y0', 'vin2': 'Y14', 'vout': 'vout49'}),
                ('and_50', And2, {'vin1': 'Y1', 'vin2': 'Y14', 'vout': 'vout50'}),
                ('and_51', And2, {'vin1': 'Y2', 'vin2': 'Y14', 'vout': 'vout51'}),
                ('and_52', And2, {'vin1': 'Y3', 'vin2': 'Y14', 'vout': 'vout52'}),
                ('and_53', And2, {'vin1': 'Y4', 'vin2': 'Y14', 'vout': 'vout53'}),
                ('and_54', And2, {'vin1': 'Y5', 'vin2': 'Y14', 'vout': 'vout54'}),
                ('and_55', And2, {'vin1': 'Y6', 'vin2': 'Y14', 'vout': 'vout55'}),
                ('and_56', And2, {'vin1': 'Y7', 'vin2': 'Y14', 'vout': 'vout56'}),
                ('and_57', And2, {'vin1': 'Y0', 'vin2': 'Y15', 'vout': 'vout57'}),
                ('and_58', And2, {'vin1': 'Y1', 'vin2': 'Y15', 'vout': 'vout58'}),
                ('and_59', And2, {'vin1': 'Y2', 'vin2': 'Y15', 'vout': 'vout59'}),
                ('and_60', And2, {'vin1': 'Y3', 'vin2': 'Y15', 'vout': 'vout60'}),
                ('and_61', And2, {'vin1': 'Y4', 'vin2': 'Y15', 'vout': 'vout61'}),
                ('and_62', And2, {'vin1': 'Y5', 'vin2': 'Y15', 'vout': 'vout62'}),
                ('and_63', And2, {'vin1': 'Y6', 'vin2': 'Y15', 'vout': 'vout63'}),
                ('and_64', And2, {'vin1': 'Y7', 'vin2': 'Y15', 'vout': 'vout64'}),
                ('and_65', And2, {'vin1': 'Y0', 'vin2': 'Y16', 'vout': 'vout65'}),
                ('and_66', And2, {'vin1': 'Y1', 'vin2': 'Y16', 'vout': 'vout66'}),
                ('and_67', And2, {'vin1': 'Y2', 'vin2': 'Y16', 'vout': 'vout67'}),
                ('and_68', And2, {'vin1': 'Y3', 'vin2': 'Y16', 'vout': 'vout68'}),
                ('and_69', And2, {'vin1': 'Y4', 'vin2': 'Y16', 'vout': 'vout69'}),
                ('and_70', And2, {'vin1': 'Y5', 'vin2': 'Y16', 'vout': 'vout70'}),
                ('and_71', And2, {'vin1': 'Y6', 'vin2': 'Y16', 'vout': 'vout71'}),
                ('and_72', And2, {'vin1': 'Y7', 'vin2': 'Y16', 'vout': 'vout72'}),
                ('and_73', And2, {'vin1': 'Y0', 'vin2': 'Y17', 'vout': 'vout73'}),
                ('and_74', And2, {'vin1': 'Y1', 'vin2': 'Y17', 'vout': 'vout74'}),
                ('and_75', And2, {'vin1': 'Y2', 'vin2': 'Y17', 'vout': 'vout75'}),
                ('and_76', And2, {'vin1': 'Y3', 'vin2': 'Y17', 'vout': 'vout76'}),
                ('and_77', And2, {'vin1': 'Y4', 'vin2': 'Y17', 'vout': 'vout77'}),
                ('and_78', And2, {'vin1': 'Y5', 'vin2': 'Y17', 'vout': 'vout78'}),
                ('and_79', And2, {'vin1': 'Y6', 'vin2': 'Y17', 'vout': 'vout79'}),
                ('and_80', And2, {'vin1': 'Y7', 'vin2': 'Y17', 'vout': 'vout80'}),
                ('and_81', And2, {'vin1': 'Y0', 'vin2': 'Y18', 'vout': 'vout81'}),
                ('and_82', And2, {'vin1': 'Y1', 'vin2': 'Y18', 'vout': 'vout82'}),
                ('and_83', And2, {'vin1': 'Y2', 'vin2': 'Y18', 'vout': 'vout83'}),
                ('and_84', And2, {'vin1': 'Y3', 'vin2': 'Y18', 'vout': 'vout84'}),
                ('and_85', And2, {'vin1': 'Y4', 'vin2': 'Y18', 'vout': 'vout85'}),
                ('and_86', And2, {'vin1': 'Y5', 'vin2': 'Y18', 'vout': 'vout86'}),
                ('and_87', And2, {'vin1': 'Y6', 'vin2': 'Y18', 'vout': 'vout87'}),
                ('and_88', And2, {'vin1': 'Y7', 'vin2': 'Y18', 'vout': 'vout88'}),
                ('and_89', And2, {'vin1': 'Y0', 'vin2': 'Y19', 'vout': 'vout89'}),
                ('and_90', And2, {'vin1': 'Y1', 'vin2': 'Y19', 'vout': 'vout90'}),
                ('and_91', And2, {'vin1': 'Y2', 'vin2': 'Y19', 'vout': 'vout91'}),
                ('and_92', And2, {'vin1': 'Y3', 'vin2': 'Y19', 'vout': 'vout92'}),
                ('and_93', And2, {'vin1': 'Y4', 'vin2': 'Y19', 'vout': 'vout93'}),
                ('and_94', And2, {'vin1': 'Y5', 'vin2': 'Y19', 'vout': 'vout94'}),
                ('and_95', And2, {'vin1': 'Y6', 'vin2': 'Y19', 'vout': 'vout95'}),
                ('and_96', And2, {'vin1': 'Y7', 'vin2': 'Y19', 'vout': 'vout96'}),
                ('and_97', And2, {'vin1': 'Y0', 'vin2': 'Y20', 'vout': 'vout97'}),
                ('and_98', And2, {'vin1': 'Y1', 'vin2': 'Y20', 'vout': 'vout98'}),
                ('and_99', And2, {'vin1': 'Y2', 'vin2': 'Y20', 'vout': 'vout99'}),
                ('and_100', And2, {'vin1': 'Y3', 'vin2': 'Y20', 'vout': 'vout100'}),
                ('and_101', And2, {'vin1': 'Y4', 'vin2': 'Y20', 'vout': 'vout101'}),
                ('and_102', And2, {'vin1': 'Y5', 'vin2': 'Y20', 'vout': 'vout102'}),
                ('and_103', And2, {'vin1': 'Y6', 'vin2': 'Y20', 'vout': 'vout103'}),
                ('and_104', And2, {'vin1': 'Y7', 'vin2': 'Y20', 'vout': 'vout104'}),
                ('and_105', And2, {'vin1': 'Y0', 'vin2': 'Y21', 'vout': 'vout105'}),
                ('and_106', And2, {'vin1': 'Y1', 'vin2': 'Y21', 'vout': 'vout106'}),
                ('and_107', And2, {'vin1': 'Y2', 'vin2': 'Y21', 'vout': 'vout107'}),
                ('and_108', And2, {'vin1': 'Y3', 'vin2': 'Y21', 'vout': 'vout108'}),
                ('and_109', And2, {'vin1': 'Y4', 'vin2': 'Y21', 'vout': 'vout109'}),
                ('and_110', And2, {'vin1': 'Y5', 'vin2': 'Y21', 'vout': 'vout110'}),
                ('and_111', And2, {'vin1': 'Y6', 'vin2': 'Y21', 'vout': 'vout111'}),
                ('and_112', And2, {'vin1': 'Y7', 'vin2': 'Y21', 'vout': 'vout112'}),
                ('and_113', And2, {'vin1': 'Y0', 'vin2': 'Y22', 'vout': 'vout113'}),
                ('and_114', And2, {'vin1': 'Y1', 'vin2': 'Y22', 'vout': 'vout114'}),
                ('and_115', And2, {'vin1': 'Y2', 'vin2': 'Y22', 'vout': 'vout115'}),
                ('and_116', And2, {'vin1': 'Y3', 'vin2': 'Y22', 'vout': 'vout116'}),
                ('and_117', And2, {'vin1': 'Y4', 'vin2': 'Y22', 'vout': 'vout117'}),
                ('and_118', And2, {'vin1': 'Y5', 'vin2': 'Y22', 'vout': 'vout118'}),
                ('and_119', And2, {'vin1': 'Y0', 'vin2': 'Y22', 'vout': 'vout119'}),
                ('and_120', And2, {'vin1': 'Y7', 'vin2': 'Y22', 'vout': 'vout120'}),
                ('and_121', And2, {'vin1': 'Y0', 'vin2': 'Y23', 'vout': 'vout121'}),
                ('and_122', And2, {'vin1': 'Y1', 'vin2': 'Y23', 'vout': 'vout122'}),
                ('and_123', And2, {'vin1': 'Y2', 'vin2': 'Y23', 'vout': 'vout123'}),
                ('and_124', And2, {'vin1': 'Y3', 'vin2': 'Y23', 'vout': 'vout124'}),
                ('and_125', And2, {'vin1': 'Y4', 'vin2': 'Y23', 'vout': 'vout125'}),
                ('and_126', And2, {'vin1': 'Y5', 'vin2': 'Y23', 'vout': 'vout126'}),
                ('and_127', And2, {'vin1': 'Y6', 'vin2': 'Y23', 'vout': 'vout127'}),
                ('and_128', And2, {'vin1': 'Y7', 'vin2': 'Y23', 'vout': 'vout128'}),
                ]


class BlackCell(CombinationalBlock):
    inputs = ['Gik','Pik','Gk_1j','Pk_1j']
    outputs = ['Gij', 'Pij']
    internal_nodes = ['blackMid']
    class_blocks = [
        ('and1', And2, {'vin1': 'Pik', 'vin2': 'Gk_1j', 'vout': 'blackMid'}),
        ('and2', And2, {'vin1': 'Pik', 'vin2': 'Pk_1j', 'vout': 'Pij'}),
        ('or', Or2,    {'vin1': 'Gik', 'vin2': 'blackMid', 'vout': 'Gij'}),
                       ]
    
class GrayCell(CombinationalBlock):
    inputs = ['Gik','Pik','Gk_1j']
    outputs = ['Gij']
    internal_nodes = ['grayMid']
    class_blocks = [
        ('and', And2, {'vin1': 'Pik', 'vin2': 'Gk_1j', 'vout': 'grayMid'}),
        ('or', Or2,   {'vin1': 'Gik', 'vin2': 'grayMid', 'vout': 'Gij'}),
                       ]

class PGCell(CombinationalBlock):
    inputs = ['vin1', 'vin2']
    outputs = ['P','G']
    internal_nodes = []
    class_blocks = [
        ('and', And2,  {'vin1': 'vin1', 'vin2': 'vin2', 'vout': 'G'}),
        ('xor', Xor2,   {'vin1': 'vin1', 'vin2': 'vin2', 'vout': 'P'}),
                       ]


class Adder2Bit(CombinationalBlock):
    inputs = ['vin_cin', 'vin_a0', 'vin_a1', 'vin_b0', 'vin_b1',]
    outputs = ['s0', 's1', 'vout_cout']
    internal_nodes = ['p0','p1','g0','g1','c0' ]
    class_blocks = [
        ('pg0', PGCell, {'vin1':'vin_a0', 'vin2': 'vin_b0', 'P':'p0', 'G':'g0'} ),
        ('pg1', PGCell, {'vin1':'vin_a1', 'vin2': 'vin_b1', 'P':'p1', 'G':'g1'} ),
        ('gray0', GrayCell, {'Gik':'g0','Pik':'p0','Gk_1j':'vin_cin', 'Gij': 'c0'}  ),
        ('gray1', GrayCell, {'Gik':'g1','Pik':'p1','Gk_1j':'c0', 'Gij': 'vout_cout'}  ),
        ('sum0', Xor2, {'vin1': 'vin_cin', 'vin2': 'p0', 'vout': 's0'} ),
        ('sum1', Xor2, {'vin1': 'c0', 'vin2': 'p1', 'vout': 's1'} ),
        ]
    
class Adder32Bit_Kogge_Stone(CombinationalBlock):
    inputs = [
              'vin_cin', 
              'vin_a0', 'vin_a1', 'vin_a2', 'vin_a3', 'vin_a4', 'vin_a5', 'vin_a6', 'vin_a7', 'vin_a8','vin_a9', 'vin_a10', 
              'vin_a11', 'vin_a12', 'vin_a13', 'vin_a14', 'vin_a15', 'vin_a16', 'vin_a17', 'vin_a18', 'vin_a19', 'vin_a20', 
              'vin_a21', 'vin_a22', 'vin_a23', 'vin_a24', 'vin_a25', 'vin_a26', 'vin_a27', 'vin_a28', 'vin_a29', 'vin_a30',
              'vin_a31',
              'vin_b0', 'vin_b1', 'vin_b2', 'vin_b3', 'vin_b4', 'vin_b5', 'vin_b6', 'vin_b7', 'vin_b8', 'vin_b9', 'vin_b10', 
              'vin_b11', 'vin_b12', 'vin_b13', 'vin_b14', 'vin_b15', 'vin_b16', 'vin_b17', 'vin_b18', 'vin_b19', 'vin_b20', 
              'vin_b21', 'vin_b22', 'vin_b23', 'vin_b24', 'vin_b25', 'vin_b26', 'vin_b27', 'vin_b28', 'vin_b29', 'vin_b30',
              'vin_b31', 
              ]
    outputs = [
               'vout_cout', 
               's0', 's1', 's2', 's3', 's4','s5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 's17',
               's18', 's19', 's20', 's21', 's22', 's23', 's24', 's25', 's26', 's27', 's28', 's29', 's30', 's31', 
               ]
    internal_nodes = [
                      'p0', 'p1','p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15', 'p16', 
                      'p17', 'p18', 'p19', 'p20', 'p21', 'p22', 'p23', 'p24', 'p25', 'p26', 'p27', 'p28', 'p29', 'p30', 'p31', 
                      'g0', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9', 'g10', 'g11', 'g12', 'g13', 'g14', 'g15', 'g16', 
                      'g17', 'g18', 'g19', 'g20', 'g21', 'g22', 'g23', 'g24', 'g25', 'g26', 'g27', 'g28', 'g29', 'g30', 'g31',  
                      
                      'gg0', 'gg1', 'gg2', 'gg3', 'gg4', 'gg5', 'gg6', 'gg7', 'gg8', 'gg9', 'gg10', 'gg11', 'gg12', 'gg13', 'gg14', 'gg15', 
                      'gg16', 'gg17', 'gg18', 'gg19', 'gg20', 'gg21', 'gg22', 'gg23', 'gg24', 'gg25', 'gg26', 'gg27', 'gg28', 'gg29', 'gg30',
                      
                      'bg0', 'bg1', 'bg2', 'bg3', 'bg4', 'bg5', 'bg6', 'bg7', 'bg8', 'bg9', 'bg10', 'bg11', 'bg12', 'bg13', 'bg14', 'bg15', 
                      'bg16', 'bg17', 'bg18', 'bg19', 'bg20', 'bg21', 'bg22', 'bg23', 'bg24', 'bg25', 'bg26', 'bg27', 'bg28', 'bg29', 'bg30',
                      'bg31', 'bg32', 'bg33', 'bg34', 'bg35', 'bg36', 'bg37', 'bg38', 'bg39', 'bg40', 'bg41','bg42','bg43','bg44', 'bg45', 
                      'bg46', 'bg47', 'bg48', 'bg49', 'bg50', 'bg51', 'bg52', 'bg53', 'bg54', 'bg55', 'bg56', 'bg57', 'bg58', 'bg59', 'bg60', 
                      'bg61', 'bg62', 'bg63', 'bg64', 'bg65', 'bg66', 'bg67', 'bg68', 'bg69', 'bg70', 'bg71', 'bg72', 'bg73', 'bg74', 'bg75', 
                      'bg76', 'bg77', 'bg78', 'bg79', 'bg80', 'bg81', 'bg82', 'bg83', 'bg84', 'bg85', 'bg86', 'bg87', 'bg88', 'bg89', 'bg90',     
                      'bg91', 'bg92', 'bg93', 'bg94', 'bg95', 'bg96', 'bg97', 
                      
                      'bp0', 'bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8', 'bp9', 'bp10', 'bp11', 'bp12', 'bp13', 'bp14', 'bp15', 
                      'bp16', 'bp17', 'bp18', 'bp19', 'bp20', 'bp21', 'bp22', 'bp23', 'bp24', 'bp25', 'bp26', 'bp27', 'bp28', 'bp29', 'bp30',
                      'bp31', 'bp32', 'bp33', 'bp34', 'bp35', 'bp36', 'bp37', 'bp38', 'bp39', 'bp40', 'bp41','bp42','bp43','bp44', 'bp45', 
                      'bp46', 'bp47', 'bp48', 'bp49', 'bp50', 'bp51', 'bp52', 'bp53', 'bp54', 'bp55', 'bp56', 'bp57', 'bp58', 'bp59', 'bp60', 
                      'bp61', 'bp62', 'bp63', 'bp64', 'bp65', 'bp66', 'bp67', 'bp68', 'bp69', 'bp70', 'bp71', 'bp72', 'bp73', 'bp74', 'bp75', 
                      'bp76', 'bp77', 'bp78', 'bp79', 'bp80', 'bp81', 'bp82', 'bp83', 'bp84', 'bp85', 'bp86', 'bp87', 'bp88', 'bp89', 'bp90',     
                      'bp91', 'bp92', 'bp93', 'bp94', 'bp95', 'bp96', 'bp97', 
 
                      ]
    class_blocks = [
        ('pg0', PGCell, {'vin1':'vin_a0', 'vin2': 'vin_b0', 'P':'p0', 'G':'g0'} ),
        ('pg1', PGCell, {'vin1':'vin_a1', 'vin2': 'vin_b1', 'P':'p1', 'G':'g1'} ),
        ('pg2', PGCell, {'vin1':'vin_a2', 'vin2': 'vin_b2', 'P':'p2', 'G':'g2'} ),
        ('pg3', PGCell, {'vin1':'vin_a3', 'vin2': 'vin_b3', 'P':'p3', 'G':'g3'} ),
        ('pg4', PGCell, {'vin1':'vin_a4', 'vin2': 'vin_b4', 'P':'p4', 'G':'g4'} ),
        ('pg5', PGCell, {'vin1':'vin_a5', 'vin2': 'vin_b5', 'P':'p5', 'G':'g5'} ),
        ('pg6', PGCell, {'vin1':'vin_a6', 'vin2': 'vin_b6', 'P':'p6', 'G':'g6'} ),
        ('pg7', PGCell, {'vin1':'vin_a7', 'vin2': 'vin_b7', 'P':'p7', 'G':'g7'} ),
        ('pg8', PGCell, {'vin1':'vin_a8', 'vin2': 'vin_b8', 'P':'p8', 'G':'g8'} ),
        ('pg9', PGCell, {'vin1':'vin_a9', 'vin2': 'vin_b9', 'P':'p9', 'G':'g9'} ),
        ('pg10', PGCell, {'vin1':'vin_a10', 'vin2': 'vin_b10', 'P':'p10', 'G':'g10'} ),
        ('pg11', PGCell, {'vin1':'vin_a11', 'vin2': 'vin_b11', 'P':'p11', 'G':'g11'} ),
        ('pg12', PGCell, {'vin1':'vin_a12', 'vin2': 'vin_b12', 'P':'p12', 'G':'g12'} ),
        ('pg13', PGCell, {'vin1':'vin_a13', 'vin2': 'vin_b13', 'P':'p13', 'G':'g13'} ),
        ('pg14', PGCell, {'vin1':'vin_a14', 'vin2': 'vin_b14', 'P':'p14', 'G':'g14'} ),
        ('pg15', PGCell, {'vin1':'vin_a15', 'vin2': 'vin_b15', 'P':'p15', 'G':'g15'} ),
        ('pg16', PGCell, {'vin1':'vin_a16', 'vin2': 'vin_b16', 'P':'p16', 'G':'g16'} ),
        ('pg17', PGCell, {'vin1':'vin_a17', 'vin2': 'vin_b17', 'P':'p17', 'G':'g17'} ),
        ('pg18', PGCell, {'vin1':'vin_a18', 'vin2': 'vin_b18', 'P':'p18', 'G':'g18'} ),
        ('pg19', PGCell, {'vin1':'vin_a19', 'vin2': 'vin_b19', 'P':'p19', 'G':'g19'} ),
        ('pg20', PGCell, {'vin1':'vin_a20', 'vin2': 'vin_b20', 'P':'p20', 'G':'g20'} ),
        ('pg21', PGCell, {'vin1':'vin_a21', 'vin2': 'vin_b21', 'P':'p21', 'G':'g21'} ),
        ('pg22', PGCell, {'vin1':'vin_a22', 'vin2': 'vin_b22', 'P':'p22', 'G':'g22'} ),
        ('pg23', PGCell, {'vin1':'vin_a23', 'vin2': 'vin_b23', 'P':'p23', 'G':'g23'} ),
        ('pg24', PGCell, {'vin1':'vin_a24', 'vin2': 'vin_b24', 'P':'p24', 'G':'g24'} ),
        ('pg25', PGCell, {'vin1':'vin_a25', 'vin2': 'vin_b25', 'P':'p25', 'G':'g25'} ),
        ('pg26', PGCell, {'vin1':'vin_a26', 'vin2': 'vin_b26', 'P':'p26', 'G':'g26'} ),
        ('pg27', PGCell, {'vin1':'vin_a27', 'vin2': 'vin_b27', 'P':'p27', 'G':'g27'} ),
        ('pg28', PGCell, {'vin1':'vin_a28', 'vin2': 'vin_b28', 'P':'p28', 'G':'g28'} ),
        ('pg29', PGCell, {'vin1':'vin_a29', 'vin2': 'vin_b29', 'P':'p29', 'G':'g29'} ),
        ('pg30', PGCell, {'vin1':'vin_a30', 'vin2': 'vin_b30', 'P':'p30', 'G':'g30'} ),
        ('pg31', PGCell, {'vin1':'vin_a31', 'vin2': 'vin_b31', 'P':'p31', 'G':'g31'} ),
        #row 1
        ('gray0', GrayCell, {'Gik':'g0','Pik':'p0','Gk_1j':'vin_cin', 'Gij': 'gg0'} ),
        ('black0', BlackCell, {'Gik':'g1','Pik':'p1','Gk_1j':'g0', 'Pk_1j':'p0', 'Gij': 'bg0', 'Pij': 'bp0'} ),
        ('black1', BlackCell, {'Gik':'g2','Pik':'p2','Gk_1j':'g1', 'Pk_1j':'p1', 'Gij': 'bg1', 'Pij': 'bp1'} ),
        ('black2', BlackCell, {'Gik':'g3','Pik':'p3','Gk_1j':'g2', 'Pk_1j':'p2', 'Gij': 'bg2', 'Pij': 'bp2'} ),
        ('black3', BlackCell, {'Gik':'g4','Pik':'p4','Gk_1j':'g3', 'Pk_1j':'p3', 'Gij': 'bg3', 'Pij': 'bp3'} ),
        ('black4', BlackCell, {'Gik':'g5','Pik':'p5','Gk_1j':'g4', 'Pk_1j':'p4', 'Gij': 'bg4', 'Pij': 'bp4'} ),
        ('black5', BlackCell, {'Gik':'g6','Pik':'p6','Gk_1j':'g5', 'Pk_1j':'p5', 'Gij': 'bg5', 'Pij': 'bp5'} ),
        ('black6', BlackCell, {'Gik':'g7','Pik':'p7','Gk_1j':'g6', 'Pk_1j':'p6', 'Gij': 'bg6', 'Pij': 'bp6'} ),
        ('black7', BlackCell, {'Gik':'g8','Pik':'p8','Gk_1j':'g7', 'Pk_1j':'p7', 'Gij': 'bg7', 'Pij': 'bp7'} ),
        ('black8', BlackCell, {'Gik':'g9','Pik':'p9','Gk_1j':'g8', 'Pk_1j':'p8', 'Gij': 'bg8', 'Pij': 'bp8'} ),
        ('black9', BlackCell, {'Gik':'g10','Pik':'p10','Gk_1j':'g9', 'Pk_1j':'p9', 'Gij': 'bg9', 'Pij': 'bp9'} ),
        ('black10', BlackCell, {'Gik':'g11','Pik':'p11','Gk_1j':'g10', 'Pk_1j':'p10', 'Gij': 'bg10', 'Pij': 'bp10'} ),
        ('black11', BlackCell, {'Gik':'g12','Pik':'p12','Gk_1j':'g11', 'Pk_1j':'p11', 'Gij': 'bg11', 'Pij': 'bp11'} ),
        ('black12', BlackCell, {'Gik':'g13','Pik':'p13','Gk_1j':'g12', 'Pk_1j':'p12', 'Gij': 'bg12', 'Pij': 'bp12'} ),
        ('black13', BlackCell, {'Gik':'g14','Pik':'p14','Gk_1j':'g13', 'Pk_1j':'p13', 'Gij': 'bg13', 'Pij': 'bp13'} ),
        ('black14', BlackCell, {'Gik':'g15','Pik':'p15','Gk_1j':'g14', 'Pk_1j':'p14', 'Gij': 'bg14', 'Pij': 'bp14'} ),
        ('black15', BlackCell, {'Gik':'g16','Pik':'p16','Gk_1j':'g15', 'Pk_1j':'p15', 'Gij': 'bg15', 'Pij': 'bp15'} ),
        ('black16', BlackCell, {'Gik':'g17','Pik':'p17','Gk_1j':'g16', 'Pk_1j':'p16', 'Gij': 'bg16', 'Pij': 'bp16'} ),
        ('black17', BlackCell, {'Gik':'g18','Pik':'p18','Gk_1j':'g17', 'Pk_1j':'p17', 'Gij': 'bg17', 'Pij': 'bp17'} ),
        ('black18', BlackCell, {'Gik':'g19','Pik':'p19','Gk_1j':'g18', 'Pk_1j':'p18', 'Gij': 'bg18', 'Pij': 'bp18'} ),
        ('black19', BlackCell, {'Gik':'g20','Pik':'p20','Gk_1j':'g19', 'Pk_1j':'p19', 'Gij': 'bg19', 'Pij': 'bp19'} ),
        ('black20', BlackCell, {'Gik':'g21','Pik':'p21','Gk_1j':'g20', 'Pk_1j':'p20', 'Gij': 'bg20', 'Pij': 'bp20'} ),
        ('black21', BlackCell, {'Gik':'g22','Pik':'p22','Gk_1j':'g21', 'Pk_1j':'p21', 'Gij': 'bg21', 'Pij': 'bp21'} ),
        ('black22', BlackCell, {'Gik':'g23','Pik':'p23','Gk_1j':'g22', 'Pk_1j':'p22', 'Gij': 'bg22', 'Pij': 'bp22'} ),
        ('black23', BlackCell, {'Gik':'g24','Pik':'p24','Gk_1j':'g23', 'Pk_1j':'p23', 'Gij': 'bg23', 'Pij': 'bp23'} ),
        ('black24', BlackCell, {'Gik':'g25','Pik':'p25','Gk_1j':'g24', 'Pk_1j':'p24', 'Gij': 'bg24', 'Pij': 'bp24'} ),
        ('black25', BlackCell, {'Gik':'g26','Pik':'p26','Gk_1j':'g25', 'Pk_1j':'p25', 'Gij': 'bg25', 'Pij': 'bp25'} ),
        ('black26', BlackCell, {'Gik':'g27','Pik':'p27','Gk_1j':'g26', 'Pk_1j':'p26', 'Gij': 'bg26', 'Pij': 'bp26'} ),
        ('black27', BlackCell, {'Gik':'g28','Pik':'p28','Gk_1j':'g27', 'Pk_1j':'p27', 'Gij': 'bg27', 'Pij': 'bp27'} ),
        ('black28', BlackCell, {'Gik':'g29','Pik':'p29','Gk_1j':'g28', 'Pk_1j':'p28', 'Gij': 'bg28', 'Pij': 'bp28'} ),
        ('black29', BlackCell, {'Gik':'g30','Pik':'p30','Gk_1j':'g29', 'Pk_1j':'p29', 'Gij': 'bg29', 'Pij': 'bp29'} ),
        #row 2
        ('gray1', GrayCell, {'Gik':'bg0','Pik':'bp0','Gk_1j':'vin_cin', 'Gij': 'gg1'} ),
        ('gray2', GrayCell, {'Gik':'bg1','Pik':'bp1','Gk_1j':'gg0', 'Gij': 'gg2'} ),
        ('black30', BlackCell, {'Gik':'bg2','Pik':'bp2','Gk_1j':'bg0', 'Pk_1j':'bp0', 'Gij': 'bg30', 'Pij': 'bp30'} ),
        ('black31', BlackCell, {'Gik':'bg3','Pik':'bp3','Gk_1j':'bg1', 'Pk_1j':'bp1', 'Gij': 'bg31', 'Pij': 'bp31'} ),
        ('black32', BlackCell, {'Gik':'bg4','Pik':'bp4','Gk_1j':'bg2', 'Pk_1j':'bp2', 'Gij': 'bg32', 'Pij': 'bp32'} ),
        ('black33', BlackCell, {'Gik':'bg5','Pik':'bp5','Gk_1j':'bg3', 'Pk_1j':'bp3', 'Gij': 'bg33', 'Pij': 'bp33'} ),
        ('black34', BlackCell, {'Gik':'bg6','Pik':'bp6','Gk_1j':'bg4', 'Pk_1j':'bp4', 'Gij': 'bg34', 'Pij': 'bp34'} ),
        ('black35', BlackCell, {'Gik':'bg7','Pik':'bp7','Gk_1j':'bg5', 'Pk_1j':'bp5', 'Gij': 'bg35', 'Pij': 'bp35'} ),
        ('black36', BlackCell, {'Gik':'bg8','Pik':'bp8','Gk_1j':'bg6', 'Pk_1j':'bp6', 'Gij': 'bg36', 'Pij': 'bp36'} ),
        ('black37', BlackCell, {'Gik':'bg9','Pik':'bp9','Gk_1j':'bg7', 'Pk_1j':'bp7', 'Gij': 'bg37', 'Pij': 'bp37'} ),
        ('black38', BlackCell, {'Gik':'bg10','Pik':'bp10','Gk_1j':'bg8', 'Pk_1j':'bp8', 'Gij': 'bg38', 'Pij': 'bp38'} ),
        ('black39', BlackCell, {'Gik':'bg11','Pik':'bp11','Gk_1j':'bg9', 'Pk_1j':'bp9', 'Gij': 'bg39', 'Pij': 'bp39'} ),
        ('black40', BlackCell, {'Gik':'bg12','Pik':'bp12','Gk_1j':'bg10', 'Pk_1j':'bp10', 'Gij': 'bg40', 'Pij': 'bp40'} ),
        ('black41', BlackCell, {'Gik':'bg13','Pik':'bp13','Gk_1j':'bg11', 'Pk_1j':'bp11', 'Gij': 'bg41', 'Pij': 'bp41'} ),
        ('black42', BlackCell, {'Gik':'bg14','Pik':'bp14','Gk_1j':'bg12', 'Pk_1j':'bp12', 'Gij': 'bg42', 'Pij': 'bp42'} ),
        ('black43', BlackCell, {'Gik':'bg15','Pik':'bp15','Gk_1j':'bg13', 'Pk_1j':'bp13', 'Gij': 'bg43', 'Pij': 'bp43'} ),
        ('black44', BlackCell, {'Gik':'bg16','Pik':'bp16','Gk_1j':'bg14', 'Pk_1j':'bp14', 'Gij': 'bg44', 'Pij': 'bp44'} ),
        ('black45', BlackCell, {'Gik':'bg17','Pik':'bp17','Gk_1j':'bg15', 'Pk_1j':'bp15', 'Gij': 'bg45', 'Pij': 'bp45'} ),
        ('black46', BlackCell, {'Gik':'bg18','Pik':'bp18','Gk_1j':'bg16', 'Pk_1j':'bp16', 'Gij': 'bg46', 'Pij': 'bp46'} ),
        ('black47', BlackCell, {'Gik':'bg19','Pik':'bp19','Gk_1j':'bg17', 'Pk_1j':'bp17', 'Gij': 'bg47', 'Pij': 'bp47'} ),
        ('black48', BlackCell, {'Gik':'bg20','Pik':'bp20','Gk_1j':'bg18', 'Pk_1j':'bp18', 'Gij': 'bg48', 'Pij': 'bp48'} ),
        ('black49', BlackCell, {'Gik':'bg21','Pik':'bp21','Gk_1j':'bg19', 'Pk_1j':'bp19', 'Gij': 'bg49', 'Pij': 'bp49'} ),
        ('black50', BlackCell, {'Gik':'bg22','Pik':'bp22','Gk_1j':'bg20', 'Pk_1j':'bp20', 'Gij': 'bg50', 'Pij': 'bp50'} ),
        ('black51', BlackCell, {'Gik':'bg23','Pik':'bp23','Gk_1j':'bg21', 'Pk_1j':'bp21', 'Gij': 'bg51', 'Pij': 'bp51'} ),
        ('black52', BlackCell, {'Gik':'bg24','Pik':'bp24','Gk_1j':'bg22', 'Pk_1j':'bp22', 'Gij': 'bg52', 'Pij': 'bp52'} ),
        ('black53', BlackCell, {'Gik':'bg25','Pik':'bp25','Gk_1j':'bg23', 'Pk_1j':'bp23', 'Gij': 'bg53', 'Pij': 'bp53'} ),
        ('black54', BlackCell, {'Gik':'bg26','Pik':'bp26','Gk_1j':'bg24', 'Pk_1j':'bp24', 'Gij': 'bg54', 'Pij': 'bp54'} ),
        ('black55', BlackCell, {'Gik':'bg27','Pik':'bp27','Gk_1j':'bg25', 'Pk_1j':'bp25', 'Gij': 'bg55', 'Pij': 'bp55'} ),
        ('black56', BlackCell, {'Gik':'bg28','Pik':'bp28','Gk_1j':'bg26', 'Pk_1j':'bp26', 'Gij': 'bg56', 'Pij': 'bp56'} ),
        ('black57', BlackCell, {'Gik':'bg29','Pik':'bp29','Gk_1j':'bg27', 'Pk_1j':'bp27', 'Gij': 'bg57', 'Pij': 'bp57'} ),
        #row 3
        ('gray3', GrayCell, {'Gik':'bg30','Pik':'bp30','Gk_1j':'vin_cin', 'Gij': 'gg3'} ),
        ('gray4', GrayCell, {'Gik':'bg31','Pik':'bp31','Gk_1j':'gg0', 'Gij': 'gg4'} ),
        ('gray5', GrayCell, {'Gik':'bg32','Pik':'bp32','Gk_1j':'gg1', 'Gij': 'gg5'} ),
        ('gray6', GrayCell, {'Gik':'bg33','Pik':'bp33','Gk_1j':'gg2', 'Gij': 'gg6'} ),
        ('black58', BlackCell, {'Gik':'bg34','Pik':'bp34','Gk_1j':'bg30', 'Pk_1j':'bp30', 'Gij': 'bg58', 'Pij': 'bp58'} ),
        ('black59', BlackCell, {'Gik':'bg35','Pik':'bp35','Gk_1j':'bg31', 'Pk_1j':'bp31', 'Gij': 'bg59', 'Pij': 'bp59'} ),
        ('black60', BlackCell, {'Gik':'bg36','Pik':'bp36','Gk_1j':'bg32', 'Pk_1j':'bp32', 'Gij': 'bg60', 'Pij': 'bp60'} ),
        ('black61', BlackCell, {'Gik':'bg37','Pik':'bp37','Gk_1j':'bg33', 'Pk_1j':'bp33', 'Gij': 'bg61', 'Pij': 'bp61'} ),
        ('black62', BlackCell, {'Gik':'bg38','Pik':'bp38','Gk_1j':'bg34', 'Pk_1j':'bp34', 'Gij': 'bg62', 'Pij': 'bp62'} ),
        ('black63', BlackCell, {'Gik':'bg39','Pik':'bp39','Gk_1j':'bg35', 'Pk_1j':'bp35', 'Gij': 'bg63', 'Pij': 'bp63'} ),
        ('black64', BlackCell, {'Gik':'bg40','Pik':'bp40','Gk_1j':'bg36', 'Pk_1j':'bp36', 'Gij': 'bg64', 'Pij': 'bp64'} ),
        ('black65', BlackCell, {'Gik':'bg41','Pik':'bp41','Gk_1j':'bg37', 'Pk_1j':'bp37', 'Gij': 'bg65', 'Pij': 'bp65'} ),
        ('black66', BlackCell, {'Gik':'bg42','Pik':'bp42','Gk_1j':'bg38', 'Pk_1j':'bp38', 'Gij': 'bg66', 'Pij': 'bp66'} ),
        ('black67', BlackCell, {'Gik':'bg43','Pik':'bp43','Gk_1j':'bg39', 'Pk_1j':'bp39', 'Gij': 'bg67', 'Pij': 'bp67'} ),
        ('black68', BlackCell, {'Gik':'bg44','Pik':'bp44','Gk_1j':'bg40', 'Pk_1j':'bp40', 'Gij': 'bg68', 'Pij': 'bp68'} ),
        ('black69', BlackCell, {'Gik':'bg45','Pik':'bp45','Gk_1j':'bg41', 'Pk_1j':'bp41', 'Gij': 'bg69', 'Pij': 'bp69'} ),
        ('black70', BlackCell, {'Gik':'bg46','Pik':'bp46','Gk_1j':'bg42', 'Pk_1j':'bp42', 'Gij': 'bg70', 'Pij': 'bp70'} ),
        ('black71', BlackCell, {'Gik':'bg47','Pik':'bp47','Gk_1j':'bg43', 'Pk_1j':'bp43', 'Gij': 'bg71', 'Pij': 'bp71'} ),
        ('black72', BlackCell, {'Gik':'bg48','Pik':'bp48','Gk_1j':'bg44', 'Pk_1j':'bp44', 'Gij': 'bg72', 'Pij': 'bp72'} ),
        ('black73', BlackCell, {'Gik':'bg49','Pik':'bp49','Gk_1j':'bg45', 'Pk_1j':'bp45', 'Gij': 'bg73', 'Pij': 'bp73'} ),
        ('black74', BlackCell, {'Gik':'bg50','Pik':'bp50','Gk_1j':'bg46', 'Pk_1j':'bp46', 'Gij': 'bg74', 'Pij': 'bp74'} ),
        ('black75', BlackCell, {'Gik':'bg51','Pik':'bp51','Gk_1j':'bg47', 'Pk_1j':'bp47', 'Gij': 'bg75', 'Pij': 'bp75'} ),
        ('black76', BlackCell, {'Gik':'bg52','Pik':'bp52','Gk_1j':'bg48', 'Pk_1j':'bp48', 'Gij': 'bg76', 'Pij': 'bp76'} ),
        ('black77', BlackCell, {'Gik':'bg53','Pik':'bp53','Gk_1j':'bg49', 'Pk_1j':'bp49', 'Gij': 'bg77', 'Pij': 'bp77'} ),
        ('black78', BlackCell, {'Gik':'bg54','Pik':'bp54','Gk_1j':'bg50', 'Pk_1j':'bp50', 'Gij': 'bg78', 'Pij': 'bp78'} ),
        ('black79', BlackCell, {'Gik':'bg55','Pik':'bp55','Gk_1j':'bg51', 'Pk_1j':'bp51', 'Gij': 'bg79', 'Pij': 'bp79'} ),
        ('black80', BlackCell, {'Gik':'bg56','Pik':'bp56','Gk_1j':'bg52', 'Pk_1j':'bp52', 'Gij': 'bg80', 'Pij': 'bp80'} ),
        ('black81', BlackCell, {'Gik':'bg57','Pik':'bp57','Gk_1j':'bg53', 'Pk_1j':'bp53', 'Gij': 'bg81', 'Pij': 'bp81'} ),
        #row 4
        ('gray7', GrayCell, {'Gik':'bg58','Pik':'bp58','Gk_1j':'vin_cin', 'Gij': 'gg7'} ),
        ('gray8', GrayCell, {'Gik':'bg59','Pik':'bp59','Gk_1j':'gg0', 'Gij': 'gg8'} ),
        ('gray9', GrayCell, {'Gik':'bg60','Pik':'bp60','Gk_1j':'gg1', 'Gij': 'gg9'} ),
        ('gray10', GrayCell, {'Gik':'bg61','Pik':'bp61','Gk_1j':'gg2', 'Gij': 'gg10'} ),
        ('gray11', GrayCell, {'Gik':'bg62','Pik':'bp62','Gk_1j':'gg3', 'Gij': 'gg11'} ),
        ('gray12', GrayCell, {'Gik':'bg63','Pik':'bp63','Gk_1j':'gg4', 'Gij': 'gg12'} ),
        ('gray13', GrayCell, {'Gik':'bg64','Pik':'bp64','Gk_1j':'gg5', 'Gij': 'gg13'} ),
        ('gray14', GrayCell, {'Gik':'bg65','Pik':'bp65','Gk_1j':'gg6', 'Gij': 'gg14'} ),
        ('black82', BlackCell, {'Gik':'bg66','Pik':'bp66','Gk_1j':'bg58', 'Pk_1j':'bp58', 'Gij': 'bg82', 'Pij': 'bp82'} ),
        ('black83', BlackCell, {'Gik':'bg67','Pik':'bp67','Gk_1j':'bg59', 'Pk_1j':'bp59', 'Gij': 'bg83', 'Pij': 'bp83'} ),
        ('black84', BlackCell, {'Gik':'bg68','Pik':'bp68','Gk_1j':'bg60', 'Pk_1j':'bp60', 'Gij': 'bg84', 'Pij': 'bp84'} ),
        ('black85', BlackCell, {'Gik':'bg69','Pik':'bp69','Gk_1j':'bg61', 'Pk_1j':'bp61', 'Gij': 'bg85', 'Pij': 'bp85'} ),
        ('black86', BlackCell, {'Gik':'bg70','Pik':'bp70','Gk_1j':'bg62', 'Pk_1j':'bp62', 'Gij': 'bg86', 'Pij': 'bp86'} ),
        ('black87', BlackCell, {'Gik':'bg71','Pik':'bp71','Gk_1j':'bg63', 'Pk_1j':'bp63', 'Gij': 'bg87', 'Pij': 'bp87'} ),
        ('black88', BlackCell, {'Gik':'bg72','Pik':'bp72','Gk_1j':'bg64', 'Pk_1j':'bp64', 'Gij': 'bg88', 'Pij': 'bp88'} ),
        ('black89', BlackCell, {'Gik':'bg73','Pik':'bp73','Gk_1j':'bg65', 'Pk_1j':'bp65', 'Gij': 'bg89', 'Pij': 'bp89'} ),
        ('black90', BlackCell, {'Gik':'bg74','Pik':'bp74','Gk_1j':'bg66', 'Pk_1j':'bp66', 'Gij': 'bg90', 'Pij': 'bp90'} ),
        ('black91', BlackCell, {'Gik':'bg75','Pik':'bp75','Gk_1j':'bg67', 'Pk_1j':'bp67', 'Gij': 'bg91', 'Pij': 'bp91'} ),
        ('black92', BlackCell, {'Gik':'bg76','Pik':'bp76','Gk_1j':'bg68', 'Pk_1j':'bp68', 'Gij': 'bg92', 'Pij': 'bp92'} ),
        ('black93', BlackCell, {'Gik':'bg77','Pik':'bp77','Gk_1j':'bg69', 'Pk_1j':'bp69', 'Gij': 'bg93', 'Pij': 'bp93'} ),
        ('black94', BlackCell, {'Gik':'bg78','Pik':'bp78','Gk_1j':'bg70', 'Pk_1j':'bp70', 'Gij': 'bg94', 'Pij': 'bp94'} ),
        ('black95', BlackCell, {'Gik':'bg79','Pik':'bp79','Gk_1j':'bg71', 'Pk_1j':'bp71', 'Gij': 'bg95', 'Pij': 'bp95'} ),
        ('black96', BlackCell, {'Gik':'bg80','Pik':'bp80','Gk_1j':'bg72', 'Pk_1j':'bp72', 'Gij': 'bg96', 'Pij': 'bp96'} ),
        ('black97', BlackCell, {'Gik':'bg81','Pik':'bp81','Gk_1j':'bg73', 'Pk_1j':'bp73', 'Gij': 'bg97', 'Pij': 'bp97'} ),
        #row 5
        ('gray15', GrayCell, {'Gik':'bg82','Pik':'bp82','Gk_1j':'vin_cin', 'Gij': 'gg15'} ),
        ('gray16', GrayCell, {'Gik':'bg83','Pik':'bp83','Gk_1j':'gg0', 'Gij': 'gg16'} ),
        ('gray17', GrayCell, {'Gik':'bg84','Pik':'bp84','Gk_1j':'gg1', 'Gij': 'gg17'} ),
        ('gray18', GrayCell, {'Gik':'bg85','Pik':'bp85','Gk_1j':'gg2', 'Gij': 'gg18'} ),
        ('gray19', GrayCell, {'Gik':'bg86','Pik':'bp86','Gk_1j':'gg3', 'Gij': 'gg19'} ),
        ('gray20', GrayCell, {'Gik':'bg87','Pik':'bp87','Gk_1j':'gg4', 'Gij': 'gg20'} ),
        ('gray21', GrayCell, {'Gik':'bg88','Pik':'bp88','Gk_1j':'gg5', 'Gij': 'gg21'} ),
        ('gray22', GrayCell, {'Gik':'bg89','Pik':'bp89','Gk_1j':'gg6', 'Gij': 'gg22'} ),
        ('gray23', GrayCell, {'Gik':'bg90','Pik':'bp90','Gk_1j':'gg7', 'Gij': 'gg23'} ),
        ('gray24', GrayCell, {'Gik':'bg91','Pik':'bp91','Gk_1j':'gg8', 'Gij': 'gg24'} ),
        ('gray25', GrayCell, {'Gik':'bg92','Pik':'bp92','Gk_1j':'gg9', 'Gij': 'gg25'} ),
        ('gray26', GrayCell, {'Gik':'bg93','Pik':'bp93','Gk_1j':'gg10', 'Gij': 'gg26'} ),
        ('gray27', GrayCell, {'Gik':'bg94','Pik':'bp94','Gk_1j':'gg11', 'Gij': 'gg27'} ),
        ('gray28', GrayCell, {'Gik':'bg95','Pik':'bp95','Gk_1j':'gg12', 'Gij': 'gg28'} ),
        ('gray29', GrayCell, {'Gik':'bg96','Pik':'bp96','Gk_1j':'gg13', 'Gij': 'gg29'} ),
        ('gray30', GrayCell, {'Gik':'bg97','Pik':'bp97','Gk_1j':'gg14', 'Gij': 'gg30'} ),
        
        ('sum0', Xor2, {'vin1': 'vin_cin', 'vin2': 'p0', 'vout': 's0'} ),
        ('sum1', Xor2, {'vin1': 'gg0', 'vin2': 'p1', 'vout': 's1'} ),
        ('sum2', Xor2, {'vin1': 'gg1', 'vin2': 'p2', 'vout': 's2'} ),
        ('sum3', Xor2, {'vin1': 'gg2', 'vin2': 'p3', 'vout': 's3'} ),
        ('sum4', Xor2, {'vin1': 'gg3', 'vin2': 'p4', 'vout': 's4'} ),
        ('sum5', Xor2, {'vin1': 'gg4', 'vin2': 'p5', 'vout': 's5'} ),
        ('sum6', Xor2, {'vin1': 'gg5', 'vin2': 'p6', 'vout': 's6'} ),
        ('sum7', Xor2, {'vin1': 'gg6', 'vin2': 'p7', 'vout': 's7'} ),
        ('sum8', Xor2, {'vin1': 'gg7', 'vin2': 'p8', 'vout': 's8'} ),
        ('sum9', Xor2, {'vin1': 'gg8', 'vin2': 'p9', 'vout': 's9'} ),
        ('sum10', Xor2, {'vin1': 'gg9', 'vin2': 'p10', 'vout': 's10'} ),
        ('sum11', Xor2, {'vin1': 'gg10', 'vin2': 'p11', 'vout': 's11'} ),
        ('sum12', Xor2, {'vin1': 'gg11', 'vin2': 'p12', 'vout': 's12'} ),
        ('sum13', Xor2, {'vin1': 'gg12', 'vin2': 'p13', 'vout': 's13'} ),
        ('sum14', Xor2, {'vin1': 'gg13', 'vin2': 'p14', 'vout': 's14'} ),
        ('sum15', Xor2, {'vin1': 'gg14', 'vin2': 'p15', 'vout': 's15'} ),
        ('sum16', Xor2, {'vin1': 'gg15', 'vin2': 'p16', 'vout': 's16'} ),
        ('sum17', Xor2, {'vin1': 'gg16', 'vin2': 'p17', 'vout': 's17'} ),
        ('sum18', Xor2, {'vin1': 'gg17', 'vin2': 'p18', 'vout': 's18'} ),
        ('sum19', Xor2, {'vin1': 'gg18', 'vin2': 'p19', 'vout': 's19'} ),
        ('sum20', Xor2, {'vin1': 'gg19', 'vin2': 'p20', 'vout': 's20'} ),
        ('sum21', Xor2, {'vin1': 'gg20', 'vin2': 'p21', 'vout': 's21'} ),
        ('sum22', Xor2, {'vin1': 'gg21', 'vin2': 'p22', 'vout': 's22'} ),
        ('sum23', Xor2, {'vin1': 'gg22', 'vin2': 'p23', 'vout': 's23'} ),
        ('sum24', Xor2, {'vin1': 'gg23', 'vin2': 'p24', 'vout': 's24'} ),
        ('sum25', Xor2, {'vin1': 'gg24', 'vin2': 'p25', 'vout': 's25'} ),
        ('sum26', Xor2, {'vin1': 'gg25', 'vin2': 'p26', 'vout': 's26'} ),
        ('sum27', Xor2, {'vin1': 'gg26', 'vin2': 'p27', 'vout': 's27'} ),
        ('sum28', Xor2, {'vin1': 'gg27', 'vin2': 'p28', 'vout': 's28'} ),
        ('sum29', Xor2, {'vin1': 'gg28', 'vin2': 'p29', 'vout': 's29'} ),
        ('sum30', Xor2, {'vin1': 'gg29', 'vin2': 'p30', 'vout': 's30'} ),
        ('sum31', Xor2, {'vin1': 'gg30', 'vin2': 'p31', 'vout': 's31'} ),
        
        ('gray31', GrayCell, {'Gik':'g31','Pik':'p31','Gk_1j':'gg30', 'Gij': 'vout_cout'} ),
                
        ]
    
class Adder32Bit_Brent_Kung(CombinationalBlock):
    inputs = [
              'vin_cin', 
              'vin_a0', 'vin_a1', 'vin_a2', 'vin_a3', 'vin_a4', 'vin_a5', 'vin_a6', 'vin_a7', 'vin_a8','vin_a9', 'vin_a10', 
              'vin_a11', 'vin_a12', 'vin_a13', 'vin_a14', 'vin_a15', 'vin_a16', 'vin_a17', 'vin_a18', 'vin_a19', 'vin_a20', 
              'vin_a21', 'vin_a22', 'vin_a23', 'vin_a24', 'vin_a25', 'vin_a26', 'vin_a27', 'vin_a28', 'vin_a29', 'vin_a30',
              'vin_a31',
              'vin_b0', 'vin_b1', 'vin_b2', 'vin_b3', 'vin_b4', 'vin_b5', 'vin_b6', 'vin_b7', 'vin_b8', 'vin_b9', 'vin_b10', 
              'vin_b11', 'vin_b12', 'vin_b13', 'vin_b14', 'vin_b15', 'vin_b16', 'vin_b17', 'vin_b18', 'vin_b19', 'vin_b20', 
              'vin_b21', 'vin_b22', 'vin_b23', 'vin_b24', 'vin_b25', 'vin_b26', 'vin_b27', 'vin_b28', 'vin_b29', 'vin_b30',
              'vin_b31', 
              ]
    outputs = [
               'vout_cout', 
               's0', 's1', 's2', 's3', 's4','s5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 's17',
               's18', 's19', 's20', 's21', 's22', 's23', 's24', 's25', 's26', 's27', 's28', 's29', 's30', 's31', 
               ]
    internal_nodes = [
                      'p0', 'p1','p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15', 'p16', 
                      'p17', 'p18', 'p19', 'p20', 'p21', 'p22', 'p23', 'p24', 'p25', 'p26', 'p27', 'p28', 'p29', 'p30', 'p31', 
                      'g0', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9', 'g10', 'g11', 'g12', 'g13', 'g14', 'g15', 'g16', 
                      'g17', 'g18', 'g19', 'g20', 'g21', 'g22', 'g23', 'g24', 'g25', 'g26', 'g27', 'g28', 'g29', 'g30', 'g31',                                             
                      
                      'gg0', 'gg1', 'gg2', 'gg3', 'gg4', 'gg5', 'gg6', 'gg7', 'gg8', 'gg9', 'gg10', 'gg11', 'gg12', 'gg13', 'gg14', 'gg15', 
                      'gg16', 'gg17', 'gg18', 'gg19', 'gg20', 'gg21', 'gg22', 'gg23', 'gg24', 'gg25', 'gg26', 'gg27', 'gg28', 'gg29', 'gg30', 
                      
                      'bg0', 'bg1', 'bg2', 'bg3', 'bg4', 'bg5', 'bg6', 'bg7', 'bg8', 'bg9', 'bg10', 'bg11', 'bg12', 'bg13', 'bg14', 'bg15', 
                      'bg16', 'bg17', 'bg18', 'bg19', 'bg20', 'bg21', 'bg22', 'bg23', 'bg24', 'bg25', 
                      
                      'bp0', 'bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8', 'bp9', 'bp10', 'bp11', 'bp12', 'bp13', 'bp14', 'bp15', 
                      'bp16', 'bp17', 'bp18', 'bp19', 'bp20', 'bp21', 'bp22', 'bp23', 'bp24', 'bp25', 
 
                      ]
    class_blocks = [
        ('pg0', PGCell, {'vin1':'vin_a0', 'vin2': 'vin_b0', 'P':'p0', 'G':'g0'} ),
        ('pg1', PGCell, {'vin1':'vin_a1', 'vin2': 'vin_b1', 'P':'p1', 'G':'g1'} ),
        ('pg2', PGCell, {'vin1':'vin_a2', 'vin2': 'vin_b2', 'P':'p2', 'G':'g2'} ),
        ('pg3', PGCell, {'vin1':'vin_a3', 'vin2': 'vin_b3', 'P':'p3', 'G':'g3'} ),
        ('pg4', PGCell, {'vin1':'vin_a4', 'vin2': 'vin_b4', 'P':'p4', 'G':'g4'} ),
        ('pg5', PGCell, {'vin1':'vin_a5', 'vin2': 'vin_b5', 'P':'p5', 'G':'g5'} ),
        ('pg6', PGCell, {'vin1':'vin_a6', 'vin2': 'vin_b6', 'P':'p6', 'G':'g6'} ),
        ('pg7', PGCell, {'vin1':'vin_a7', 'vin2': 'vin_b7', 'P':'p7', 'G':'g7'} ),
        ('pg8', PGCell, {'vin1':'vin_a8', 'vin2': 'vin_b8', 'P':'p8', 'G':'g8'} ),
        ('pg9', PGCell, {'vin1':'vin_a9', 'vin2': 'vin_b9', 'P':'p9', 'G':'g9'} ),
        ('pg10', PGCell, {'vin1':'vin_a10', 'vin2': 'vin_b10', 'P':'p10', 'G':'g10'} ),
        ('pg11', PGCell, {'vin1':'vin_a11', 'vin2': 'vin_b11', 'P':'p11', 'G':'g11'} ),
        ('pg12', PGCell, {'vin1':'vin_a12', 'vin2': 'vin_b12', 'P':'p12', 'G':'g12'} ),
        ('pg13', PGCell, {'vin1':'vin_a13', 'vin2': 'vin_b13', 'P':'p13', 'G':'g13'} ),
        ('pg14', PGCell, {'vin1':'vin_a14', 'vin2': 'vin_b14', 'P':'p14', 'G':'g14'} ),
        ('pg15', PGCell, {'vin1':'vin_a15', 'vin2': 'vin_b15', 'P':'p15', 'G':'g15'} ),
        ('pg16', PGCell, {'vin1':'vin_a16', 'vin2': 'vin_b16', 'P':'p16', 'G':'g16'} ),
        ('pg17', PGCell, {'vin1':'vin_a17', 'vin2': 'vin_b17', 'P':'p17', 'G':'g17'} ),
        ('pg18', PGCell, {'vin1':'vin_a18', 'vin2': 'vin_b18', 'P':'p18', 'G':'g18'} ),
        ('pg19', PGCell, {'vin1':'vin_a19', 'vin2': 'vin_b19', 'P':'p19', 'G':'g19'} ),
        ('pg20', PGCell, {'vin1':'vin_a20', 'vin2': 'vin_b20', 'P':'p20', 'G':'g20'} ),
        ('pg21', PGCell, {'vin1':'vin_a21', 'vin2': 'vin_b21', 'P':'p21', 'G':'g21'} ),
        ('pg22', PGCell, {'vin1':'vin_a22', 'vin2': 'vin_b22', 'P':'p22', 'G':'g22'} ),
        ('pg23', PGCell, {'vin1':'vin_a23', 'vin2': 'vin_b23', 'P':'p23', 'G':'g23'} ),
        ('pg24', PGCell, {'vin1':'vin_a24', 'vin2': 'vin_b24', 'P':'p24', 'G':'g24'} ),
        ('pg25', PGCell, {'vin1':'vin_a25', 'vin2': 'vin_b25', 'P':'p25', 'G':'g25'} ),
        ('pg26', PGCell, {'vin1':'vin_a26', 'vin2': 'vin_b26', 'P':'p26', 'G':'g26'} ),
        ('pg27', PGCell, {'vin1':'vin_a27', 'vin2': 'vin_b27', 'P':'p27', 'G':'g27'} ),
        ('pg28', PGCell, {'vin1':'vin_a28', 'vin2': 'vin_b28', 'P':'p28', 'G':'g28'} ),
        ('pg29', PGCell, {'vin1':'vin_a29', 'vin2': 'vin_b29', 'P':'p29', 'G':'g29'} ),
        ('pg30', PGCell, {'vin1':'vin_a30', 'vin2': 'vin_b30', 'P':'p30', 'G':'g30'} ),
        ('pg31', PGCell, {'vin1':'vin_a31', 'vin2': 'vin_b31', 'P':'p31', 'G':'g31'} ),
        #row 1
        ('gray0', GrayCell, {'Gik':'g0','Pik':'p0','Gk_1j':'vin_cin', 'Gij': 'gg0'} ),
        ('black0', BlackCell, {'Gik':'g2','Pik':'p2','Gk_1j':'g1', 'Pk_1j':'p1', 'Gij': 'bg0', 'Pij': 'bp0'} ),
        ('black1', BlackCell, {'Gik':'g4','Pik':'p4','Gk_1j':'g3', 'Pk_1j':'p3', 'Gij': 'bg1', 'Pij': 'bp1'} ),
        ('black2', BlackCell, {'Gik':'g6','Pik':'p6','Gk_1j':'g5', 'Pk_1j':'p5', 'Gij': 'bg2', 'Pij': 'bp2'} ),
        ('black3', BlackCell, {'Gik':'g8','Pik':'p8','Gk_1j':'g7', 'Pk_1j':'p7', 'Gij': 'bg3', 'Pij': 'bp3'} ),
        ('black4', BlackCell, {'Gik':'g10','Pik':'p10','Gk_1j':'g9', 'Pk_1j':'p9', 'Gij': 'bg4', 'Pij': 'bp4'} ),
        ('black5', BlackCell, {'Gik':'g12','Pik':'p12','Gk_1j':'g11', 'Pk_1j':'p11', 'Gij': 'bg5', 'Pij': 'bp5'} ),
        ('black6', BlackCell, {'Gik':'g14','Pik':'p14','Gk_1j':'g13', 'Pk_1j':'p13', 'Gij': 'bg6', 'Pij': 'bp6'} ),
        ('black7', BlackCell, {'Gik':'g16','Pik':'p16','Gk_1j':'g15', 'Pk_1j':'p15', 'Gij': 'bg7', 'Pij': 'bp7'} ),
        ('black8', BlackCell, {'Gik':'g18','Pik':'p18','Gk_1j':'g17', 'Pk_1j':'p17', 'Gij': 'bg8', 'Pij': 'bp8'} ),
        ('black9', BlackCell, {'Gik':'g20','Pik':'p20','Gk_1j':'g19', 'Pk_1j':'p19', 'Gij': 'bg9', 'Pij': 'bp9'} ),
        ('black10', BlackCell, {'Gik':'g22','Pik':'p22','Gk_1j':'g21', 'Pk_1j':'p21', 'Gij': 'bg10', 'Pij': 'bp10'} ),
        ('black11', BlackCell, {'Gik':'g24','Pik':'p24','Gk_1j':'g23', 'Pk_1j':'p23', 'Gij': 'bg11', 'Pij': 'bp11'} ),
        ('black12', BlackCell, {'Gik':'g26','Pik':'p26','Gk_1j':'g25', 'Pk_1j':'p25', 'Gij': 'bg12', 'Pij': 'bp12'} ),
        ('black13', BlackCell, {'Gik':'g28','Pik':'p28','Gk_1j':'g27', 'Pk_1j':'p27', 'Gij': 'bg13', 'Pij': 'bp13'} ),
        ('black14', BlackCell, {'Gik':'g30','Pik':'p30','Gk_1j':'g29', 'Pk_1j':'p29', 'Gij': 'bg14', 'Pij': 'bp14'} ),        
        #row 2
        ('gray1', GrayCell, {'Gik':'bg0','Pik':'bp0','Gk_1j':'gg0', 'Gij': 'gg1'} ),        
        ('black15', BlackCell, {'Gik':'bg2','Pik':'bp2','Gk_1j':'bg1', 'Pk_1j':'bp1', 'Gij': 'bg15', 'Pij': 'bp15'} ),
        ('black16', BlackCell, {'Gik':'bg4','Pik':'bp4','Gk_1j':'bg3', 'Pk_1j':'bp3', 'Gij': 'bg16', 'Pij': 'bp16'} ),
        ('black17', BlackCell, {'Gik':'bg6','Pik':'bp6','Gk_1j':'bg5', 'Pk_1j':'bp5', 'Gij': 'bg17', 'Pij': 'bp17'} ),
        ('black18', BlackCell, {'Gik':'bg8','Pik':'bp8','Gk_1j':'bg7', 'Pk_1j':'bp7', 'Gij': 'bg18', 'Pij': 'bp18'} ),
        ('black19', BlackCell, {'Gik':'bg10','Pik':'bp10','Gk_1j':'bg9', 'Pk_1j':'bp9', 'Gij': 'bg19', 'Pij': 'bp19'} ),
        ('black20', BlackCell, {'Gik':'bg12','Pik':'bp12','Gk_1j':'bg11', 'Pk_1j':'bp11', 'Gij': 'bg20', 'Pij': 'bp20'} ),
        ('black21', BlackCell, {'Gik':'bg14','Pik':'bp14','Gk_1j':'bg13', 'Pk_1j':'bp13', 'Gij': 'bg21', 'Pij': 'bp21'} ),
        #row 3
        ('gray2', GrayCell, {'Gik':'bg15','Pik':'bp15','Gk_1j':'gg1', 'Gij': 'gg2'} ),
        ('black22', BlackCell, {'Gik':'bg17','Pik':'bp17','Gk_1j':'bg16', 'Pk_1j':'bp16', 'Gij': 'bg22', 'Pij': 'bp22'} ),
        ('black23', BlackCell, {'Gik':'bg19','Pik':'bp19','Gk_1j':'bg18', 'Pk_1j':'bp18', 'Gij': 'bg23', 'Pij': 'bp23'} ),
        ('black24', BlackCell, {'Gik':'bg21','Pik':'bp21','Gk_1j':'bg20', 'Pk_1j':'bp20', 'Gij': 'bg24', 'Pij': 'bp24'} ),
        #row 4                
        ('gray3', GrayCell, {'Gik':'bg22','Pik':'bp22','Gk_1j':'gg2', 'Gij': 'gg3'} ),
        ('black25', BlackCell, {'Gik':'bg24','Pik':'bp24','Gk_1j':'bg23', 'Pk_1j':'bp23', 'Gij': 'bg25', 'Pij': 'bp25'} ),
        #row 5
        ('gray4', GrayCell, {'Gik':'bg25','Pik':'bp25','Gk_1j':'gg3', 'Gij': 'gg4'} ),
        ('gray5', GrayCell, {'Gik':'bg23','Pik':'bp23','Gk_1j':'gg3', 'Gij': 'gg5'} ),
        #row 6
        ('gray6', GrayCell, {'Gik':'bg16','Pik':'bp16','Gk_1j':'gg2', 'Gij': 'gg6'} ),
        ('gray7', GrayCell, {'Gik':'bg18','Pik':'bp18','Gk_1j':'gg3', 'Gij': 'gg7'} ),
        ('gray8', GrayCell, {'Gik':'bg20','Pik':'bp20','Gk_1j':'gg5', 'Gij': 'gg8'} ),
        #row 7
        ('gray9', GrayCell, {'Gik':'bg1','Pik':'bp1','Gk_1j':'gg1', 'Gij': 'gg9'} ),
        ('gray10', GrayCell, {'Gik':'bg3','Pik':'bp3','Gk_1j':'gg2', 'Gij': 'gg10'} ),
        ('gray11', GrayCell, {'Gik':'bg5','Pik':'bp5','Gk_1j':'gg6', 'Gij': 'gg11'} ),
        ('gray12', GrayCell, {'Gik':'bg7','Pik':'bp7','Gk_1j':'gg3', 'Gij': 'gg12'} ),
        ('gray13', GrayCell, {'Gik':'bg9','Pik':'bp9','Gk_1j':'gg7', 'Gij': 'gg13'} ),
        ('gray14', GrayCell, {'Gik':'bg11','Pik':'bp11','Gk_1j':'gg5', 'Gij': 'gg14'} ),
        ('gray15', GrayCell, {'Gik':'bg13','Pik':'bp13','Gk_1j':'gg8', 'Gij': 'gg15'} ),
        #row 8
        ('gray16', GrayCell, {'Gik':'g1','Pik':'p1','Gk_1j':'gg0', 'Gij': 'gg16'} ),
        ('gray17', GrayCell, {'Gik':'g3','Pik':'p3','Gk_1j':'gg1', 'Gij': 'gg17'} ),
        ('gray18', GrayCell, {'Gik':'g5','Pik':'p5','Gk_1j':'gg9', 'Gij': 'gg18'} ),
        ('gray19', GrayCell, {'Gik':'g7','Pik':'p7','Gk_1j':'gg2', 'Gij': 'gg19'} ),
        ('gray20', GrayCell, {'Gik':'g9','Pik':'p9','Gk_1j':'gg10', 'Gij': 'gg20'} ),
        ('gray21', GrayCell, {'Gik':'g11','Pik':'p11','Gk_1j':'gg6', 'Gij': 'gg21'} ),
        ('gray22', GrayCell, {'Gik':'g13','Pik':'p13','Gk_1j':'gg11', 'Gij': 'gg22'} ),
        ('gray23', GrayCell, {'Gik':'g15','Pik':'p15','Gk_1j':'gg3', 'Gij': 'gg23'} ),
        ('gray24', GrayCell, {'Gik':'g17','Pik':'p17','Gk_1j':'gg12', 'Gij': 'gg24'} ),
        ('gray25', GrayCell, {'Gik':'g19','Pik':'p19','Gk_1j':'gg7', 'Gij': 'gg25'} ),
        ('gray26', GrayCell, {'Gik':'g21','Pik':'p21','Gk_1j':'gg13', 'Gij': 'gg26'} ),
        ('gray27', GrayCell, {'Gik':'g23','Pik':'p23','Gk_1j':'gg5', 'Gij': 'gg27'} ),
        ('gray28', GrayCell, {'Gik':'g25','Pik':'p25','Gk_1j':'gg14', 'Gij': 'gg28'} ),
        ('gray29', GrayCell, {'Gik':'g27','Pik':'p27','Gk_1j':'gg8', 'Gij': 'gg29'} ),
        ('gray30', GrayCell, {'Gik':'g29','Pik':'p29','Gk_1j':'gg15', 'Gij': 'gg30'} ),
        
        ('sum0', Xor2, {'vin1': 'vin_cin', 'vin2': 'p0', 'vout': 's0'} ),
        ('sum1', Xor2, {'vin1': 'gg0', 'vin2': 'p1', 'vout': 's1'} ),
        ('sum2', Xor2, {'vin1': 'gg16', 'vin2': 'p2', 'vout': 's2'} ),
        ('sum3', Xor2, {'vin1': 'gg1', 'vin2': 'p3', 'vout': 's3'} ),
        ('sum4', Xor2, {'vin1': 'gg17', 'vin2': 'p4', 'vout': 's4'} ),
        ('sum5', Xor2, {'vin1': 'gg9', 'vin2': 'p5', 'vout': 's5'} ),
        ('sum6', Xor2, {'vin1': 'gg18', 'vin2': 'p6', 'vout': 's6'} ),
        ('sum7', Xor2, {'vin1': 'gg2', 'vin2': 'p7', 'vout': 's7'} ),
        ('sum8', Xor2, {'vin1': 'gg19', 'vin2': 'p8', 'vout': 's8'} ),
        ('sum9', Xor2, {'vin1': 'gg10', 'vin2': 'p9', 'vout': 's9'} ),
        ('sum10', Xor2, {'vin1': 'gg20', 'vin2': 'p10', 'vout': 's10'} ),
        ('sum11', Xor2, {'vin1': 'gg6', 'vin2': 'p11', 'vout': 's11'} ),
        ('sum12', Xor2, {'vin1': 'gg21', 'vin2': 'p12', 'vout': 's12'} ),
        ('sum13', Xor2, {'vin1': 'gg11', 'vin2': 'p13', 'vout': 's13'} ),
        ('sum14', Xor2, {'vin1': 'gg22', 'vin2': 'p14', 'vout': 's14'} ),
        ('sum15', Xor2, {'vin1': 'gg3', 'vin2': 'p15', 'vout': 's15'} ),
        ('sum16', Xor2, {'vin1': 'gg23', 'vin2': 'p16', 'vout': 's16'} ),
        ('sum17', Xor2, {'vin1': 'gg12', 'vin2': 'p17', 'vout': 's17'} ),
        ('sum18', Xor2, {'vin1': 'gg24', 'vin2': 'p18', 'vout': 's18'} ),
        ('sum19', Xor2, {'vin1': 'gg7', 'vin2': 'p19', 'vout': 's19'} ),
        ('sum20', Xor2, {'vin1': 'gg25', 'vin2': 'p20', 'vout': 's20'} ),
        ('sum21', Xor2, {'vin1': 'gg13', 'vin2': 'p21', 'vout': 's21'} ),
        ('sum22', Xor2, {'vin1': 'gg26', 'vin2': 'p22', 'vout': 's22'} ),
        ('sum23', Xor2, {'vin1': 'gg5', 'vin2': 'p23', 'vout': 's23'} ),
        ('sum24', Xor2, {'vin1': 'gg27', 'vin2': 'p24', 'vout': 's24'} ),
        ('sum25', Xor2, {'vin1': 'gg14', 'vin2': 'p25', 'vout': 's25'} ),
        ('sum26', Xor2, {'vin1': 'gg28', 'vin2': 'p26', 'vout': 's26'} ),
        ('sum27', Xor2, {'vin1': 'gg8', 'vin2': 'p27', 'vout': 's27'} ),
        ('sum28', Xor2, {'vin1': 'gg29', 'vin2': 'p28', 'vout': 's28'} ),
        ('sum29', Xor2, {'vin1': 'gg15', 'vin2': 'p29', 'vout': 's29'} ),
        ('sum30', Xor2, {'vin1': 'gg30', 'vin2': 'p30', 'vout': 's30'} ),
        ('sum31', Xor2, {'vin1': 'gg4', 'vin2': 'p31', 'vout': 's31'} ),
        
        ('gray31', GrayCell, {'Gik':'g31','Pik':'p31','Gk_1j':'gg4', 'Gij': 'vout_cout'} ),
                
        ]                
            
class Adder32Bit_Ladner_Fischer(CombinationalBlock):
    inputs = [
              'vin_cin', 
              'vin_a0', 'vin_a1', 'vin_a2', 'vin_a3', 'vin_a4', 'vin_a5', 'vin_a6', 'vin_a7', 'vin_a8','vin_a9', 'vin_a10', 
              'vin_a11', 'vin_a12', 'vin_a13', 'vin_a14', 'vin_a15', 'vin_a16', 'vin_a17', 'vin_a18', 'vin_a19', 'vin_a20', 
              'vin_a21', 'vin_a22', 'vin_a23', 'vin_a24', 'vin_a25', 'vin_a26', 'vin_a27', 'vin_a28', 'vin_a29', 'vin_a30',
              'vin_a31',
              'vin_b0', 'vin_b1', 'vin_b2', 'vin_b3', 'vin_b4', 'vin_b5', 'vin_b6', 'vin_b7', 'vin_b8', 'vin_b9', 'vin_b10', 
              'vin_b11', 'vin_b12', 'vin_b13', 'vin_b14', 'vin_b15', 'vin_b16', 'vin_b17', 'vin_b18', 'vin_b19', 'vin_b20', 
              'vin_b21', 'vin_b22', 'vin_b23', 'vin_b24', 'vin_b25', 'vin_b26', 'vin_b27', 'vin_b28', 'vin_b29', 'vin_b30',
              'vin_b31', 
              ]
    outputs = [
               'vout_cout', 
               's0', 's1', 's2', 's3', 's4','s5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 's17',
               's18', 's19', 's20', 's21', 's22', 's23', 's24', 's25', 's26', 's27', 's28', 's29', 's30', 's31', 
               ]
    internal_nodes = [
                      'p0', 'p1','p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15', 'p16', 
                      'p17', 'p18', 'p19', 'p20', 'p21', 'p22', 'p23', 'p24', 'p25', 'p26', 'p27', 'p28', 'p29', 'p30', 'p31', 
                      'g0', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9', 'g10', 'g11', 'g12', 'g13', 'g14', 'g15', 'g16', 
                      'g17', 'g18', 'g19', 'g20', 'g21', 'g22', 'g23', 'g24', 'g25', 'g26', 'g27', 'g28', 'g29', 'g30', 'g31',  
                      
                      'gg0', 'gg1', 'gg2', 'gg3', 'gg4', 'gg5', 'gg6', 'gg7', 'gg8', 'gg9', 'gg10', 'gg11', 'gg12', 'gg13', 'gg14', 'gg15', 
                      'gg16', 'gg17', 'gg18', 'gg19', 'gg20', 'gg21', 'gg22', 'gg23', 'gg24', 'gg25', 'gg26', 'gg27', 'gg28', 'gg29', 'gg30', 'g31', 
                      
                      'bg0', 'bg1', 'bg2', 'bg3', 'bg4', 'bg5', 'bg6', 'bg7', 'bg8', 'bg9', 'bg10', 'bg11', 'bg12', 'bg13', 'bg14', 'bg15', 
                      'bg16', 'bg17', 'bg18', 'bg19', 'bg20', 'bg21', 'bg22', 'bg23', 'bg24', 'bg25', 'bg26', 'bg27', 'bg28', 'bg29', 'bg30',
                      'bg31', 
                      
                      'bp0', 'bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8', 'bp9', 'bp10', 'bp11', 'bp12', 'bp13', 'bp14', 'bp15', 
                      'bp16', 'bp17', 'bp18', 'bp19', 'bp20', 'bp21', 'bp22', 'bp23', 'bp24', 'bp25', 'bp26', 'bp27', 'bp28', 'bp29', 'bp30',
                      'bp31', 
 
                      ]
    class_blocks = [
        ('pg0', PGCell, {'vin1':'vin_a0', 'vin2': 'vin_b0', 'P':'p0', 'G':'g0'} ),
        ('pg1', PGCell, {'vin1':'vin_a1', 'vin2': 'vin_b1', 'P':'p1', 'G':'g1'} ),
        ('pg2', PGCell, {'vin1':'vin_a2', 'vin2': 'vin_b2', 'P':'p2', 'G':'g2'} ),
        ('pg3', PGCell, {'vin1':'vin_a3', 'vin2': 'vin_b3', 'P':'p3', 'G':'g3'} ),
        ('pg4', PGCell, {'vin1':'vin_a4', 'vin2': 'vin_b4', 'P':'p4', 'G':'g4'} ),
        ('pg5', PGCell, {'vin1':'vin_a5', 'vin2': 'vin_b5', 'P':'p5', 'G':'g5'} ),
        ('pg6', PGCell, {'vin1':'vin_a6', 'vin2': 'vin_b6', 'P':'p6', 'G':'g6'} ),
        ('pg7', PGCell, {'vin1':'vin_a7', 'vin2': 'vin_b7', 'P':'p7', 'G':'g7'} ),
        ('pg8', PGCell, {'vin1':'vin_a8', 'vin2': 'vin_b8', 'P':'p8', 'G':'g8'} ),
        ('pg9', PGCell, {'vin1':'vin_a9', 'vin2': 'vin_b9', 'P':'p9', 'G':'g9'} ),
        ('pg10', PGCell, {'vin1':'vin_a10', 'vin2': 'vin_b10', 'P':'p10', 'G':'g10'} ),
        ('pg11', PGCell, {'vin1':'vin_a11', 'vin2': 'vin_b11', 'P':'p11', 'G':'g11'} ),
        ('pg12', PGCell, {'vin1':'vin_a12', 'vin2': 'vin_b12', 'P':'p12', 'G':'g12'} ),
        ('pg13', PGCell, {'vin1':'vin_a13', 'vin2': 'vin_b13', 'P':'p13', 'G':'g13'} ),
        ('pg14', PGCell, {'vin1':'vin_a14', 'vin2': 'vin_b14', 'P':'p14', 'G':'g14'} ),
        ('pg15', PGCell, {'vin1':'vin_a15', 'vin2': 'vin_b15', 'P':'p15', 'G':'g15'} ),
        ('pg16', PGCell, {'vin1':'vin_a16', 'vin2': 'vin_b16', 'P':'p16', 'G':'g16'} ),
        ('pg17', PGCell, {'vin1':'vin_a17', 'vin2': 'vin_b17', 'P':'p17', 'G':'g17'} ),
        ('pg18', PGCell, {'vin1':'vin_a18', 'vin2': 'vin_b18', 'P':'p18', 'G':'g18'} ),
        ('pg19', PGCell, {'vin1':'vin_a19', 'vin2': 'vin_b19', 'P':'p19', 'G':'g19'} ),
        ('pg20', PGCell, {'vin1':'vin_a20', 'vin2': 'vin_b20', 'P':'p20', 'G':'g20'} ),
        ('pg21', PGCell, {'vin1':'vin_a21', 'vin2': 'vin_b21', 'P':'p21', 'G':'g21'} ),
        ('pg22', PGCell, {'vin1':'vin_a22', 'vin2': 'vin_b22', 'P':'p22', 'G':'g22'} ),
        ('pg23', PGCell, {'vin1':'vin_a23', 'vin2': 'vin_b23', 'P':'p23', 'G':'g23'} ),
        ('pg24', PGCell, {'vin1':'vin_a24', 'vin2': 'vin_b24', 'P':'p24', 'G':'g24'} ),
        ('pg25', PGCell, {'vin1':'vin_a25', 'vin2': 'vin_b25', 'P':'p25', 'G':'g25'} ),
        ('pg26', PGCell, {'vin1':'vin_a26', 'vin2': 'vin_b26', 'P':'p26', 'G':'g26'} ),
        ('pg27', PGCell, {'vin1':'vin_a27', 'vin2': 'vin_b27', 'P':'p27', 'G':'g27'} ),
        ('pg28', PGCell, {'vin1':'vin_a28', 'vin2': 'vin_b28', 'P':'p28', 'G':'g28'} ),
        ('pg29', PGCell, {'vin1':'vin_a29', 'vin2': 'vin_b29', 'P':'p29', 'G':'g29'} ),
        ('pg30', PGCell, {'vin1':'vin_a30', 'vin2': 'vin_b30', 'P':'p30', 'G':'g30'} ),
        ('pg31', PGCell, {'vin1':'vin_a31', 'vin2': 'vin_b31', 'P':'p31', 'G':'g31'} ),
        #row 1
        ('gray0', GrayCell, {'Gik':'g0','Pik':'p0','Gk_1j':'vin_cin', 'Gij': 'gg0'} ),
        ('black0', BlackCell, {'Gik':'g2','Pik':'p2','Gk_1j':'g1', 'Pk_1j':'p1', 'Gij': 'bg0', 'Pij': 'bp0'} ),
        ('black1', BlackCell, {'Gik':'g4','Pik':'p4','Gk_1j':'g3', 'Pk_1j':'p3', 'Gij': 'bg1', 'Pij': 'bp1'} ),
        ('black2', BlackCell, {'Gik':'g6','Pik':'p6','Gk_1j':'g5', 'Pk_1j':'p5', 'Gij': 'bg2', 'Pij': 'bp2'} ),
        ('black3', BlackCell, {'Gik':'g8','Pik':'p8','Gk_1j':'g7', 'Pk_1j':'p7', 'Gij': 'bg3', 'Pij': 'bp3'} ),
        ('black4', BlackCell, {'Gik':'g10','Pik':'p10','Gk_1j':'g9', 'Pk_1j':'p9', 'Gij': 'bg4', 'Pij': 'bp4'} ),
        ('black5', BlackCell, {'Gik':'g12','Pik':'p12','Gk_1j':'g11', 'Pk_1j':'p11', 'Gij': 'bg5', 'Pij': 'bp5'} ),
        ('black6', BlackCell, {'Gik':'g14','Pik':'p14','Gk_1j':'g13', 'Pk_1j':'p13', 'Gij': 'bg6', 'Pij': 'bp6'} ),
        ('black7', BlackCell, {'Gik':'g16','Pik':'p16','Gk_1j':'g15', 'Pk_1j':'p15', 'Gij': 'bg7', 'Pij': 'bp7'} ),
        ('black8', BlackCell, {'Gik':'g18','Pik':'p18','Gk_1j':'g17', 'Pk_1j':'p17', 'Gij': 'bg8', 'Pij': 'bp8'} ),
        ('black9', BlackCell, {'Gik':'g20','Pik':'p20','Gk_1j':'g19', 'Pk_1j':'p19', 'Gij': 'bg9', 'Pij': 'bp9'} ),
        ('black10', BlackCell, {'Gik':'g22','Pik':'p22','Gk_1j':'g21', 'Pk_1j':'p21', 'Gij': 'bg10', 'Pij': 'bp10'} ),
        ('black11', BlackCell, {'Gik':'g24','Pik':'p24','Gk_1j':'g23', 'Pk_1j':'p23', 'Gij': 'bg11', 'Pij': 'bp11'} ),
        ('black12', BlackCell, {'Gik':'g26','Pik':'p26','Gk_1j':'g25', 'Pk_1j':'p25', 'Gij': 'bg12', 'Pij': 'bp12'} ),
        ('black13', BlackCell, {'Gik':'g28','Pik':'p28','Gk_1j':'g27', 'Pk_1j':'p27', 'Gij': 'bg13', 'Pij': 'bp13'} ),
        ('black14', BlackCell, {'Gik':'g30','Pik':'p30','Gk_1j':'g29', 'Pk_1j':'p29', 'Gij': 'bg14', 'Pij': 'bp14'} ),  
        #row 2
        ('gray1', GrayCell, {'Gik':'bg0','Pik':'bp0','Gk_1j':'gg0', 'Gij': 'gg1'} ),        
        ('black15', BlackCell, {'Gik':'bg2','Pik':'bp2','Gk_1j':'bg1', 'Pk_1j':'bp1', 'Gij': 'bg15', 'Pij': 'bp15'} ),
        ('black16', BlackCell, {'Gik':'bg4','Pik':'bp4','Gk_1j':'bg3', 'Pk_1j':'bp3', 'Gij': 'bg16', 'Pij': 'bp16'} ),
        ('black17', BlackCell, {'Gik':'bg6','Pik':'bp6','Gk_1j':'bg5', 'Pk_1j':'bp5', 'Gij': 'bg17', 'Pij': 'bp17'} ),
        ('black18', BlackCell, {'Gik':'bg8','Pik':'bp8','Gk_1j':'bg7', 'Pk_1j':'bp7', 'Gij': 'bg18', 'Pij': 'bp18'} ),
        ('black19', BlackCell, {'Gik':'bg10','Pik':'bp10','Gk_1j':'bg9', 'Pk_1j':'bp9', 'Gij': 'bg19', 'Pij': 'bp19'} ),
        ('black20', BlackCell, {'Gik':'bg12','Pik':'bp12','Gk_1j':'bg11', 'Pk_1j':'bp11', 'Gij': 'bg20', 'Pij': 'bp20'} ),
        ('black21', BlackCell, {'Gik':'bg14','Pik':'bp14','Gk_1j':'bg13', 'Pk_1j':'bp13', 'Gij': 'bg21', 'Pij': 'bp21'} ),
        #row 3
        ('gray2', GrayCell, {'Gik':'bg1','Pik':'bp1','Gk_1j':'gg1', 'Gij': 'gg2'} ),
        ('gray3', GrayCell, {'Gik':'bg15','Pik':'bp15','Gk_1j':'gg1', 'Gij': 'gg3'} ),
        ('black22', BlackCell, {'Gik':'bg5','Pik':'bp5','Gk_1j':'bg16', 'Pk_1j':'bp16', 'Gij': 'bg22', 'Pij': 'bp22'} ),
        ('black23', BlackCell, {'Gik':'bg17','Pik':'bp17','Gk_1j':'bg16', 'Pk_1j':'bp16', 'Gij': 'bg23', 'Pij': 'bp23'} ),
        ('black24', BlackCell, {'Gik':'bg9','Pik':'bp9','Gk_1j':'bg18', 'Pk_1j':'bp18', 'Gij': 'bg24', 'Pij': 'bp24'} ),
        ('black25', BlackCell, {'Gik':'bg19','Pik':'bp19','Gk_1j':'bg18', 'Pk_1j':'bp18', 'Gij': 'bg25', 'Pij': 'bp25'} ),
        ('black26', BlackCell, {'Gik':'bg13','Pik':'bp13','Gk_1j':'bg20', 'Pk_1j':'bp20', 'Gij': 'bg26', 'Pij': 'bp26'} ),
        ('black27', BlackCell, {'Gik':'bg21','Pik':'bp21','Gk_1j':'bg20', 'Pk_1j':'bp20', 'Gij': 'bg27', 'Pij': 'bp27'} ),
        #row 4
        ('gray4', GrayCell, {'Gik':'bg3','Pik':'bp3','Gk_1j':'gg3', 'Gij': 'gg4'} ),
        ('gray5', GrayCell, {'Gik':'bg16','Pik':'bp16','Gk_1j':'gg3', 'Gij': 'gg5'} ),
        ('gray6', GrayCell, {'Gik':'bg22','Pik':'bp22','Gk_1j':'gg3', 'Gij': 'gg6'} ),
        ('gray7', GrayCell, {'Gik':'bg23','Pik':'bp23','Gk_1j':'gg3', 'Gij': 'gg7'} ),                
        ('black28', BlackCell, {'Gik':'bg11','Pik':'bp11','Gk_1j':'bg25', 'Pk_1j':'bp25', 'Gij': 'bg28', 'Pij': 'bp28'} ),
        ('black29', BlackCell, {'Gik':'bg20','Pik':'bp20','Gk_1j':'bg25', 'Pk_1j':'bp25', 'Gij': 'bg29', 'Pij': 'bp29'} ),        
        ('black30', BlackCell, {'Gik':'bg26','Pik':'bp26','Gk_1j':'bg25', 'Pk_1j':'bp25', 'Gij': 'bg30', 'Pij': 'bp30'} ),
        ('black31', BlackCell, {'Gik':'bg27','Pik':'bp27','Gk_1j':'bg25', 'Pk_1j':'bp25', 'Gij': 'bg31', 'Pij': 'bp31'} ),
        #row 5                   
        ('gray8', GrayCell, {'Gik':'bg7','Pik':'bp7','Gk_1j':'gg7', 'Gij': 'gg8'} ),
        ('gray9', GrayCell, {'Gik':'bg18','Pik':'bp18','Gk_1j':'gg7', 'Gij': 'gg9'} ),
        ('gray10', GrayCell, {'Gik':'bg24','Pik':'bp24','Gk_1j':'gg7', 'Gij': 'gg10'} ),
        ('gray11', GrayCell, {'Gik':'bg25','Pik':'bp25','Gk_1j':'gg7', 'Gij': 'gg11'} ),
        ('gray12', GrayCell, {'Gik':'bg28','Pik':'bp28','Gk_1j':'gg7', 'Gij': 'gg12'} ),
        ('gray13', GrayCell, {'Gik':'bg29','Pik':'bp29','Gk_1j':'gg7', 'Gij': 'gg13'} ),
        ('gray14', GrayCell, {'Gik':'bg30','Pik':'bp30','Gk_1j':'gg7', 'Gij': 'gg14'} ),
        ('gray15', GrayCell, {'Gik':'bg31','Pik':'bp31','Gk_1j':'gg7', 'Gij': 'gg15'} ),
        #row 6
        ('gray16', GrayCell, {'Gik':'g1','Pik':'p1','Gk_1j':'gg0', 'Gij': 'gg16'} ),
        ('gray17', GrayCell, {'Gik':'g3','Pik':'p3','Gk_1j':'gg1', 'Gij': 'gg17'} ),
        ('gray18', GrayCell, {'Gik':'g5','Pik':'p5','Gk_1j':'gg2', 'Gij': 'gg18'} ),
        ('gray19', GrayCell, {'Gik':'g7','Pik':'p7','Gk_1j':'gg3', 'Gij': 'gg19'} ),
        ('gray20', GrayCell, {'Gik':'g9','Pik':'p9','Gk_1j':'gg4', 'Gij': 'gg20'} ),
        ('gray21', GrayCell, {'Gik':'g11','Pik':'p11','Gk_1j':'gg5', 'Gij': 'gg21'} ),
        ('gray22', GrayCell, {'Gik':'g13','Pik':'p13','Gk_1j':'gg6', 'Gij': 'gg22'} ),
        ('gray23', GrayCell, {'Gik':'g15','Pik':'p15','Gk_1j':'gg7', 'Gij': 'gg23'} ),
        ('gray24', GrayCell, {'Gik':'g17','Pik':'p17','Gk_1j':'gg8', 'Gij': 'gg24'} ),
        ('gray25', GrayCell, {'Gik':'g19','Pik':'p19','Gk_1j':'gg9', 'Gij': 'gg25'} ),
        ('gray26', GrayCell, {'Gik':'g21','Pik':'p21','Gk_1j':'gg10', 'Gij': 'gg26'} ),
        ('gray27', GrayCell, {'Gik':'g23','Pik':'p23','Gk_1j':'gg11', 'Gij': 'gg27'} ),
        ('gray28', GrayCell, {'Gik':'g25','Pik':'p25','Gk_1j':'gg12', 'Gij': 'gg28'} ),
        ('gray29', GrayCell, {'Gik':'g27','Pik':'p27','Gk_1j':'gg13', 'Gij': 'gg29'} ),
        ('gray30', GrayCell, {'Gik':'g29','Pik':'p29','Gk_1j':'gg14', 'Gij': 'gg30'} ),
        
        ('sum0', Xor2, {'vin1': 'vin_cin', 'vin2': 'p0', 'vout': 's0'} ),
        ('sum1', Xor2, {'vin1': 'gg0', 'vin2': 'p1', 'vout': 's1'} ),
        ('sum2', Xor2, {'vin1': 'gg16', 'vin2': 'p2', 'vout': 's2'} ),
        ('sum3', Xor2, {'vin1': 'gg1', 'vin2': 'p3', 'vout': 's3'} ),
        ('sum4', Xor2, {'vin1': 'gg17', 'vin2': 'p4', 'vout': 's4'} ),
        ('sum5', Xor2, {'vin1': 'gg2', 'vin2': 'p5', 'vout': 's5'} ),
        ('sum6', Xor2, {'vin1': 'gg18', 'vin2': 'p6', 'vout': 's6'} ),
        ('sum7', Xor2, {'vin1': 'gg3', 'vin2': 'p7', 'vout': 's7'} ),
        ('sum8', Xor2, {'vin1': 'gg19', 'vin2': 'p8', 'vout': 's8'} ),
        ('sum9', Xor2, {'vin1': 'gg4', 'vin2': 'p9', 'vout': 's9'} ),
        ('sum10', Xor2, {'vin1': 'gg20', 'vin2': 'p10', 'vout': 's10'} ),
        ('sum11', Xor2, {'vin1': 'gg5', 'vin2': 'p11', 'vout': 's11'} ),
        ('sum12', Xor2, {'vin1': 'gg21', 'vin2': 'p12', 'vout': 's12'} ),
        ('sum13', Xor2, {'vin1': 'gg6', 'vin2': 'p13', 'vout': 's13'} ),
        ('sum14', Xor2, {'vin1': 'gg22', 'vin2': 'p14', 'vout': 's14'} ),
        ('sum15', Xor2, {'vin1': 'gg7', 'vin2': 'p15', 'vout': 's15'} ),
        ('sum16', Xor2, {'vin1': 'gg23', 'vin2': 'p16', 'vout': 's16'} ),
        ('sum17', Xor2, {'vin1': 'gg8', 'vin2': 'p17', 'vout': 's17'} ),
        ('sum18', Xor2, {'vin1': 'gg24', 'vin2': 'p18', 'vout': 's18'} ),
        ('sum19', Xor2, {'vin1': 'gg9', 'vin2': 'p19', 'vout': 's19'} ),
        ('sum20', Xor2, {'vin1': 'gg25', 'vin2': 'p20', 'vout': 's20'} ),
        ('sum21', Xor2, {'vin1': 'gg10', 'vin2': 'p21', 'vout': 's21'} ),
        ('sum22', Xor2, {'vin1': 'gg26', 'vin2': 'p22', 'vout': 's22'} ),
        ('sum23', Xor2, {'vin1': 'gg11', 'vin2': 'p23', 'vout': 's23'} ),
        ('sum24', Xor2, {'vin1': 'gg27', 'vin2': 'p24', 'vout': 's24'} ),
        ('sum25', Xor2, {'vin1': 'gg12', 'vin2': 'p25', 'vout': 's25'} ),
        ('sum26', Xor2, {'vin1': 'gg28', 'vin2': 'p26', 'vout': 's26'} ),
        ('sum27', Xor2, {'vin1': 'gg13', 'vin2': 'p27', 'vout': 's27'} ),
        ('sum28', Xor2, {'vin1': 'gg29', 'vin2': 'p28', 'vout': 's28'} ),
        ('sum29', Xor2, {'vin1': 'gg14', 'vin2': 'p29', 'vout': 's29'} ),
        ('sum30', Xor2, {'vin1': 'gg30', 'vin2': 'p30', 'vout': 's30'} ),
        ('sum31', Xor2, {'vin1': 'gg15', 'vin2': 'p31', 'vout': 's31'} ),
        
        ('gray32', GrayCell, {'Gik':'g31','Pik':'p31','Gk_1j':'gg15', 'Gij': 'vout_cout'} ),
                
        ]        
