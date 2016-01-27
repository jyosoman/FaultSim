#include"or.hh"
void MinpNorGate::output(){
    bool arr[nin];
    for(int i=0;i<nin;i++){
        arr[i]=getInWire(i)->get();
    }
    setVal(output(arr));
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
    setVal(out);
    return out;
}

void NorGate::output(){
    setVal(output(getInWire(0)->get(),getInWire(1)->get())); 
}

bool NorGate::output(bool a, bool b){
    bool out=pb.output(b,pa.output(a,true))|na.output(a,false)|nb.output(b,false);
    if(faulty){
        out=getOut();
    }
    setVal(out);
    return out;
}
void OrGate::setWire(Wire*w, int id){
    logicModel::setWire(w,id);
    ng.setWire(w,id);
}

void OrGate::output(){
    setVal(output(getInWire(0)->get(),getInWire(1)->get())); 
}


bool OrGate::output(bool a,bool b){
    w->set(ng.output(a,b));
    bool out= ig.output(w->get());
    setVal(out);
    return out;
}

