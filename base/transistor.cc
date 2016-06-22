#include"transistor.hh"

FaultType::FaultType(bool fault, bool fout){
    this->faulty=fault;
    this->fout=fout;
}

std::list<FaultType*> FaultType::flist(0);

FaultType::FaultType(){
    faulty=false;
}

bool FaultType::getOut(){
    return fout;
}

PMOSTransistor::PMOSTransistor(bool fault):FaultType(fault, true){
    flist.push_back(this);
}

PMOSTransistor::PMOSTransistor():FaultType(false,true){
    flist.push_back(this);
}

bool PMOSTransistor::output(bool in,bool top){
    bool v=false;
    if(!in){
        v=top;
    }
    if(faulty){
        v=top;
    }
    return v;
}

NMOSTransistor::NMOSTransistor(bool fault):FaultType(fault, false){
    flist.push_back(this);
}

NMOSTransistor::NMOSTransistor():FaultType(false,true){
    flist.push_back(this);
}

bool NMOSTransistor::output(bool in,bool bottom){
    bool v=false;
    if(in){
        v=bottom;
    }
    if(faulty){
        v=bottom;
    }
    return v;
}

