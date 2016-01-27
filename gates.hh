#ifndef __gates__hh
#define __gates__hh
#include"base.hh"
#include"transistor.hh"
class InvertorGate:public FaultType,public logicModel{
    PMOSTransistor pa;
    NMOSTransistor na;
    public:
    InvertorGate():logicModel(1),pa(),na(){

    }
    void output(){
        setVal(output(getInWire(0)->get())); 
    }

    bool output(bool a){
        bool out=pa.output(a,true)|na.output(a,false);
        if(faulty){
            out=getOut();
        }
        setVal(out);
        return out;
    }
};
#endif
