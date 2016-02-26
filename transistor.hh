#ifndef __transistor_hh__
#define __transistor_hh__

#include <cstddef>
#include"base.hh"
#include<list>
class FaultType{
    protected:
    static std::list<FaultType*> flist;
    public:
        bool faulty, fout;
        FaultType(bool fault, bool fout);
        FaultType();
        bool getOut();
        void setFaulty(bool a, bool b){
            faulty=a;
            fout=b;
        }
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
