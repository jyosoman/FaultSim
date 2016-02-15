#ifndef __gates__hh
#define __gates__hh
#include"base.hh"
#include"transistor.hh"
class InvertorGate:public FaultType,public node{
    PMOSTransistor pa;
    NMOSTransistor na;
    public:
    InvertorGate():node(1),pa(),na(){

    }
    void output(){
        output(getInVal(0)); 
    }

    bool output(bool a){
        bool out=pa.output(a,true)|na.output(a,false);
        if(faulty){
            out=getOut();
        }
        setVal(out,0);
        return out;
    }
};
#endif
