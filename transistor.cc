#include"transistor.hh"
FaultType::FaultType(bool fault, bool fout){
    this->faulty=fault;
    this->fout=fout;
}
FaultType::FaultType(){
    faulty=false;
}
bool FaultType::getOut(){
    return fout;
}
PMOSTransistor::PMOSTransistor(bool fault):FaultType(fault, true){
}
PMOSTransistor::PMOSTransistor():FaultType(false,true){
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
}
NMOSTransistor::NMOSTransistor():FaultType(false,true){
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

