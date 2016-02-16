#include"transistor.hh"
#include"gates.hh"
class MinpNorGate:public FaultType,public node{
    PMOSTransistor *pt;
    NMOSTransistor *nt;
    int nin;
    public:
    MinpNorGate(int n):logicModel(n){
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
    NorGate():logicModel(2),pa(),pb(),na(),nb(){
    }
    void output();

    bool output(bool a, bool b);
};

class OrGate:public FaultType,public node{
    NorGate ng;
    InvertorGate ig;
    Wire *w;
    public:
    OrGate():node(2),ng(),ig(){
        w=ng.getWire(0);
        ig.setWire(w,0);
    }
    virtual void setWire(OutWire*w, int id);
    
    void output();


    bool output(bool a,bool b);
};
