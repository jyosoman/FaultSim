#include"transistor.hh"
#include"gates.hh"
class MinpNorGate:public FaultType,public logicModel{
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
class NorGate:public FaultType,public logicModel{
    PMOSTransistor pa,pb;
    NMOSTransistor na,nb;
    public:
    NorGate():logicModel(2),pa(),pb(),na(),nb(){
    }
    void output();

    bool output(bool a, bool b);
};

class OrGate:public FaultType,public logicModel{
    NorGate ng;
    InvertorGate ig;
    Wire *w;
    public:
    OrGate():logicModel(2),ng(),ig(){
        w=ng.getOutWire();
        ig.setWire(w,0);
    }
    virtual void setWire(Wire*w, int id);
    
    void output();


    bool output(bool a,bool b);
};
