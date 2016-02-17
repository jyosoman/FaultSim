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
class AndGateBlock:public node{
    AndGate* gates;
    int gc;
    public:
    AndGateBlock(int n):node(n+1,1,NULL){
        init(n);
    }
    AndGateBlock(){
    }
    void init(int n){
        int b=n;
        gates=new AndGate[b];
        gc=b;
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
