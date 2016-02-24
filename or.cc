#include"or.hh"
void MinpNorGate::output(){
    bool arr[nin];
    for(int i=0;i<nin;i++){
        arr[i]=getWire(i)->get();
    }
    setVal(output(arr),0);
}

bool MinpNorGate::output(bool *a){
    bool out=nt[0].output(a[0],true);
    for(int i=1;i<nin;i++){
        out|=nt[i].output(a[i],true);
    }
    bool out2=pt[nin-1].output(a[nin-1],false);
    for(int i=nin-2;i>=0;i--){
        out2=pt[i].output(a[i],out2);
    }
    out|=out2;
    if(faulty){
        out=getOut();
    }
    setVal(out,0);
    return out;
}

void NorGate::output(){
    setVal(output(getWire(0)->get(),getWire(1)->get()),0); 
}

bool NorGate::output(bool a, bool b){
    bool out=pb.output(b,pa.output(a,true))|na.output(a,false)|nb.output(b,false);
    if(faulty){
        out=getOut();
    }
    setVal(out,0);
    return out;
}
void OrGate::setWire(OutWire*w, int id){
    node::setWire(w,id);
    ng.setWire(w,id);
}

void OrGate::output(){
    setVal(output(getWire(0)->get(),getWire(1)->get()),0); 
}


bool OrGate::output(bool a,bool b){
    ng.output();
    ig.output();
    setVal(ig.getWire(0)->get(),0);

    return ig.getWire(0)->get();

}

