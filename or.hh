#ifndef __or__hh__
#define __or__hh__
#include"transistor.hh"
#include"gates.hh"
class MinpNorGate:public FaultType,public node{
    PMOSTransistor *pt;
    NMOSTransistor *nt;
    int nin;
    public:
    MinpNorGate(int n):node(n){
        pt=new PMOSTransistor[n];
        nt=new NMOSTransistor[n];
        nin=n;
    }
    void output();

    bool output(bool *a);
};
class NorGate:public FaultType,public node{
    PMOSTransistor pa,pb;
    NMOSTransistor na,nb;
    public:
    NorGate():node(2),pa(),pb(),na(),nb(){
    }
    void output();

    bool output(bool a, bool b);
};

class OrGate:public FaultType,public node{
    NorGate ng;
    InvertorGate ig;
    public:
    OrGate():node(2),ng(),ig(){
        OutWire *w;
        w=ng.getWire(0);
        ig.setWire(w,0);
    }
    virtual void setWire(OutWire*w, int id);
    
    void output();


    bool output(bool a,bool b);
};
class OrGateBlock:public node{
    OrGate* gates;
    int gc;
    public:
    OrGateBlock(int n){
        init(n);
    }
    OrGateBlock(){
    }
    void init(int n){
        gates=new OrGate[n];
    }
    void output(){
        bool last=ins[0].get();
        for(int i=0;i<gc;i++){
            last=gates[i].output(last,ins[i+1].get());
        }
        setVal(last,0);
    }
};   
#endif
