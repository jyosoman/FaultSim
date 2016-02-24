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
    void printName(){
        std::cout<<"Nand Gate"<<std::endl;
    }


};
class TriNandGate:public FaultType,public node{
    PMOSTransistor pa,pb,pc;
    NMOSTransistor na,nb,nc;
    public:
    TriNandGate():node(3),pa(),pb(),pc(),na(),nb(),nc(){

    }
    void output();
    bool output(bool a, bool b,bool c);
    void printName(){
        std::cout<<"TriNand Gate"<<std::endl;
    }

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
    void printName(){
        std::cout<<"M inp Nand Gate"<<std::endl;
    }

    void setVal(bool a){
        in=a;
    }
    void setVal(bool a,int i){
        setVal(a);
    }
};
class AndGate:public FaultType,public node{
    NandGate ng;
    InvertorGate ig;
    public:
    AndGate():node(2),ng(),ig(){
        ig.setWire(ng.getWire(0),0);
    }
    void output();
    virtual void setWire(OutWire*w, int id);
     void printName(){
        std::cout<<"And Gate"<<std::endl;
    }


    bool output(bool a,bool b);
    void tick();
};
class AndGateBlock:public node{
    AndGate* gates;
    int gc;
    public:
    AndGateBlock(int n):node(n,1,NULL){
        init(n);
    }
    AndGateBlock(){
    }
    void init(int n){
        gc=n-1;
        gates=new AndGate[gc];
        node::resize(n,1);
    }
    void output(){
        bool last=getInVal(0);
        for(int i=0;i<gc;i++){
            last=gates[i].output(last,getInVal(i+1));
        }
        setVal(last,0);
    }
    void printName(){
        std::cout<<"And Gate Block"<<std::endl;
    }

}; 
#endif
