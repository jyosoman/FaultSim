#ifndef __transistor_hh__
#define __transistor_hh__

#include <cstddef>
#include"base.hh"
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
