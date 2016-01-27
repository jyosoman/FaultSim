#ifndef __and__hh
#define __and__hh
#include"transistor.hh"
#include"gates.hh"
class NandGate:public FaultType,public logicModel{
    PMOSTransistor pa,pb;
    NMOSTransistor na,nb;
    public:
    NandGate():logicModel(2),pa(),pb(),na(),nb(){
    }
    void output();
    bool output(bool a, bool b);
};
class TriNandGate:public FaultType,public logicModel{
    PMOSTransistor pa,pb,pc;
    NMOSTransistor na,nb,nc;
    public:
    TriNandGate():logicModel(3),pa(),pb(),pc(),na(),nb(),nc(){

    }
    void output();
    bool output(bool a, bool b,bool c);
};
class MinpNandGate:public FaultType,public logicModel{
    PMOSTransistor *pt;
    NMOSTransistor *nt;
    int nin;
    public:
    MinpNandGate(int n):logicModel(n){
        pt=new PMOSTransistor[n];
        nt=new NMOSTransistor[n];
        nin=n;
    }
    void output();
    bool output(bool *a);
};


class AndGate:public FaultType,public logicModel{
    NandGate ng;
    InvertorGate ig;
    Wire *w,*wina,*winb;
    public:
    AndGate():logicModel(2),ng(),ig(){
        w=ng.getOutWire();
        ig.setWire(w,0);
        wina=NULL;winb=NULL;
    }
    void output();
    virtual void setWire(Wire*w, int id);
 

    bool output(bool a,bool b);
    void tick();
};
#endif
