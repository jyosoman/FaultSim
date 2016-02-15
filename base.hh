#ifndef __base__hh__
#define __base__hh__
#include<iostream>
#include<vector>
#include<list>
#include<map>
using namespace std;
class Wire{
    public:
    virtual void set(bool v)=0;
    virtual bool get()=0;
    virtual bool isChanged()=0;
//    virtual void setWire(Wire*w);
};
class OutWire:public Wire{
    bool val,changed;
    public:
    OutWire(bool v);
    OutWire();
    void set(bool v);
    bool get();
    bool isChanged();
//    void setWire(Wire*w){}
};
class InWire:public Wire{
   OutWire*  wire;
    public:
   InWire(){
   }
   InWire(OutWire*w){
       wire=w;
   }
   void set(bool v){
   }
   bool get(){
       if(wire!=NULL)
           return wire->get();
       return false;
   }
   bool isChanged(){
       if(wire!=NULL)
           return wire->get();
       return false;
   }
   void setWire(Wire*w){wire=dynamic_cast<OutWire*>(w);}
   void setWire(OutWire* w){wire=w;}
   OutWire* getWire(){return wire;}
};

class baseNode{
    public:
        virtual int getLevel()=0;
        virtual void output()=0;
};
template<class T>
class scheduler{
    std::vector<std::list<T*> > nList;
    int curr;
    public:
    scheduler() {
        curr=0;
    }

    void set(T*n){
        if(n->getLevel()>=nList.size()){
            nList.resize(n->getLevel()+2);
        }
        nList[n->getLevel()].push_back(n);
        if(curr>n->getLevel()){
            curr=n->getLevel();
        }
    }
    void tick(){
        while(curr<nList.size()){
            while(nList[curr].empty()&&curr<nList.size()){
                curr++;
            }
            if(curr<nList.size()){
                nList[curr].front()->output();
                nList[curr].pop_front();
            }
        }
    }
};

class node;
class Network{
    friend class node;
//    vector<Wire *>inwires,outWires,internalInWires;
/*
 *  Nodes have no inwires, but only outwires. InWire class is a wrapper for that.
 *
 *
 */
    vector<InWire*> inwires;
    vector<OutWire*> outWires;
    /*
     *  Data structure to keep track of start and end nodes
     */
    vector<node*> innodes,outnodes;
    /*
     *  Data structure to maintain list of internal connections. 
     *
     *  
     */ 
    map<node*,list<node*> > connections;
    /*
     
     Data structure to map each inport with the appropriate internal node and
     * the portid of each internal node
     
     */
    vector<vector<node*> > intConns; 
    vector<vector<int> > portId; 
    /*
     *  Data structure to maintain the list of inwires and the connections to them
     *
     *
     */ 
    scheduler<node> sch;
    typedef std::vector<node*>::iterator nodeVectorIterator ;
    typedef std::list<node*>::iterator nodeListIterator ;
    void addNode(node* nn);
    public:
    Network(int in=2,int out=1){
        inwires.resize(in);
        intConns.resize(in);
        portId.resize(in);
        for(int i=0;i<in;i++){
            inwires[i]=new InWire();
        }
        outWires.resize(out);
    }
    void output();
    /*
     Adding nodes that are neither start nodes or end nodes.
     */

    void addInternalNode(node* nn);
    /*
     * 
     * Adding start nodes, registering the in wire and setting up for scheduling. 
     * 
     */
    void addStartNode(node*endNode,int netid,int nodeid);
    /*
     * Adding node as end node, 
     * pulling wire from the node and placing on the output node. 
     * Function call: node id, network wire id, node wire id. 
     * 
     */
    void addEndNodes(node*endNode,int netid,int nodeid);
    /*
     * Connect two nodes inside the network. 
     * Function call: first node, second node, first node port, second node port. 
     * Bug: check of whether both nodes
     * are inside the network is not done. 
     * 
     */
    void connect(node*a,node*b,int id1,int idb);
    /*
     * Connect external wire to block. 
     * 
     */
    void connect(OutWire* w,int inid);
    void runBFS();
};
class node:public baseNode{
    std::vector<std::vector<node*> > next;
    int level;
    vector<InWire*> *inWires;
    vector<OutWire*> *outWires;
    scheduler<node>* sch;
    Network *internalNetwork;    
    public:
    node(int in=2, int out=1,Network*lb=NULL);
    void setNext(node* next,int xid) ;

    void setSch(scheduler<node>* sch) ;

    bool isChanged() const ;
    bool isChanged(int i) const ;

    void connect(node*nm,int id,int yid);

    OutWire* getWire(int id);
    void setWire(OutWire*w,int id);
    bool getInVal(int id){
        return (*inWires)[id]->get();
    }

    void setLevel(int level) ;
    void setVal(bool v,int id){
        (*outWires)[id]->set(v);
    }
    /* Functions to allow scheduling
    */
    int getLevel();
    virtual void output();
    void setLm(Network* lm) ;
};

#endif
