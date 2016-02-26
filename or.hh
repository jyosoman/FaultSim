#ifndef __or__hh__
#define __or__hh__
#include"transistor.hh"
#include"gates.hh"
class MinpNorGate:public  node{
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
    void printName(){
        std::cout<<"M inp nor Gate"<<std::endl;
        node::printName();
    }

    bool output(bool *a);
};
class NorGate:public  node{
    PMOSTransistor pa,pb;
    NMOSTransistor na,nb;
    public:
    NorGate():node(2),pa(),pb(),na(),nb(){
    }
    void output();

    bool output(bool a, bool b);
    void printName(){
        std::cout<<"Nor Gate"<<std::endl;
        node::printName();
    }

};

class OrGate:public  node{
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
    void printName(){
        std::cout<<"Or Gate"<<std::endl;
        node::printName();
    }

};
class OrGateBlock:public node{
    OrGate* gates;
    int gc;
    public:
    OrGateBlock(int n):node(n,1,NULL){
        init(n);
    }
    OrGateBlock(){
    }
    void init(int n){
        gc=n-1;
        gates=new OrGate[n-1];
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
        std::cout<<getLevel()<<"\tOr Gate Block"<<std::endl;
        node::printName();
    }

};   
#endif
