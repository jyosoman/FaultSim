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
    void printName(){
        std::cout<<"Invertor "<<std::endl;
    }

    bool output(bool a){
        bool out=pa.output(a,true)|na.output(a,false);
        if(faulty){
            out=getOut();
        }
        setVal(out,0);
        /* std::cout<<"Invertor out "<<std::boolalpha<<out<<'\n'; */
        return out;
    }
};
class XORGate:public FaultType, public node{
    PMOSTransistor pa,pb;
    NMOSTransistor na,nb;
    XORGate():node(2,1,NULL){
    }
    void output(){
       setVal(output(getInVal(0),getInVal(1)),0); 
    }
    bool output(bool a,bool b){
        bool ab=pa.output(a,true)|na.output(a,false);
        return (pb.output(b,a)|nb.output(b,ab));
    }
};
class BufferGate:public node{
    public:
        BufferGate():node(1,1){
        }
        void output(){
            setVal(getInVal(0),0);
        }
};
#endif
