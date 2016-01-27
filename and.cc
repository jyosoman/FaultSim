#include"and.hh"
void NandGate::output(){
        setVal(output(getInWire(0)->get(),getInWire(1)->get())); 
    }
    bool NandGate::output(bool a, bool b){
        bool out=pa.output(a,true)|pb.output(b,true)|na.output(a,nb.output(b,false));
        if(faulty){
            out=getOut();
        }
        return out;
    }
    void TriNandGate::output(){
        setVal(output(getInWire(0)->get(),getInWire(1)->get(),getInWire(2)->get())); 
    }
    bool TriNandGate::output(bool a, bool b,bool c){
        bool out=pa.output(a,true)|pb.output(b,true)|pc.output(c,true)|na.output(a,nb.output(b,nc.output(c,false)));
        if(faulty){
            out=getOut();
        }
        setVal(out);
        return out;
    }
    void MinpNandGate::output(){
        bool arr[nin];
        for(int i=0;i<nin;i++){
            arr[i]=getInWire(i)->get();
        }
        setVal(output(arr));
    }

    bool MinpNandGate::output(bool *a){
        bool out=pt[0].output(a[0],true);
        for(int i=1;i<nin;i++){
            out|=pt[i].output(a[i],true);
        }
        bool out2=nt[nin-1].output(a[nin-1],false);
        for(int i=nin-2;i>=0;i--){
            out2=nt[i].output(a[i],out2);
        }
        out|=out2;
        if(faulty){
            out=getOut();
        }
        setVal(out);
        return out;
    }
    void AndGate::output(){
        setVal(output(getInWire(0)->get(),getInWire(1)->get())); 
    }
    void AndGate::setWire(Wire*w, int id){
        logicModel::setWire(w,id);
        ng.setWire(w,id);
    }
 

    bool AndGate::output(bool a,bool b){
        w->set(ng.output(a,b));
        bool out= ig.output(w->get());
        setVal(out);
        return out;
    }
    void AndGate::tick(){
        w->set(ng.output(wina->get(),winb->get()));
        setVal( ig.output(w->get()));
    }

