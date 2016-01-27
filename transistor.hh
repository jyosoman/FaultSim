#ifndef __transistor_hh__
#define __transistor_hh__

#include <cstddef>
#include"base.hh"
class logicLevel{
    char x;
    public:
    logicLevel(char v){
        x=v;
    }
    logicLevel operator&(logicLevel b) const{
        logicLevel xv(0);
        char v =b.val()*x,retv;
        switch(v){
            case -1:

                break;
            case 0:
                break;
            case 1:
                break;
            default:
                ;

        }
    }

    char val(){
        return x;
    }
};
class FaultType{
    public:
        bool faulty, fout;
        FaultType(bool fault, bool fout);
        FaultType();
        bool getOut();
};
class PMOSTransistor:public FaultType{
    public:
        PMOSTransistor(bool fault);
        PMOSTransistor();
        bool output(bool in,bool top);
};
class NMOSTransistor:public FaultType{
    public:
        NMOSTransistor(bool fault);
        NMOSTransistor();
        bool output(bool in,bool bottom);

};

#endif
