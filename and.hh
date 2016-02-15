#ifndef __and__hh
#define __and__hh
#include"transistor.hh"
#include"gates.hh"
class NandGate:public FaultType,public node{
    PMOSTransistor pa,pb;
    NMOSTransistor na,nb;
    public:
    NandGate():node(2),pa(),pb(),na(),nb(){
    }
    void output();
    bool output(bool a, bool b);
};
class TriNandGate:public FaultType,public node{
    PMOSTransistor pa,pb,pc;
    NMOSTransistor na,nb,nc;
    public:
    TriNandGate():node(3),pa(),pb(),pc(),na(),nb(),nc(){

    }
    void output();
    bool output(bool a, bool b,bool c);
};
template<unsigned int N> class MinpNandGate:public FaultType,public node{
    PMOSTransistor *pt;
    NMOSTransistor *nt;
    bool in;
    int nin;
    public:
    MinpNandGate():node(N){
        pt=new PMOSTransistor[N];
        nt=new NMOSTransistor[N];
        nin=N;
    }
    void output();
    bool output(bool *a);
    void setVal(bool a){
        in=a;
    }
    void setVal(bool a,int i){
        setVal(a);
    }
};

#endif
