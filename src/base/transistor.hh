#ifndef __transistor_hh__
#define __transistor_hh__

#include <cstddef>
#include"base.hh"
#include<list>


class FaultType{
    protected:
    public:
        static std::list<FaultType*> flist;
        static int tcount;
        typedef std::list<FaultType*>::iterator FLiterator;
        bool faulty, fout;
        FaultType(bool fault, bool fout);
        FaultType();
        bool getOut();
        virtual void setFaulty(bool a=true, bool b=true){
            faulty=a;
            fout=b;
        }
        ~FaultType(){
        }
};
class PMOSTransistor:public FaultType{
    public:
        PMOSTransistor(bool fault);
        PMOSTransistor();
        bool output(bool in,bool top);
        void setFaulty(){
            FaultType::setFaulty(true,true);
        }
        ~PMOSTransistor();
};
class NMOSTransistor:public FaultType{
    public:
        NMOSTransistor(bool fault);
        NMOSTransistor();
        bool output(bool in,bool bottom);
        void setFaulty(){
            FaultType::setFaulty(true,false);
        }
        ~NMOSTransistor();

};

#endif
