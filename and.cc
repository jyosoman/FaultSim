
/*
#include"and_impl.hh"
class AndGate:public FaultType,public node{
    NandGate ng;
    InvertorGate ig;
//    Wire *w,*wina,*winb;
    public:
    AndGate():node(2),ng(),ig(){
//        w=ng.getWire(0);
        ig.setWire(ng.getWire(0),0);
//        wina=NULL;winb=NULL;
    }
    void output();
    virtual void setWire(OutWire*w, int id);
 

    bool output(bool a,bool b);
    void tick();
};

void NandGate::output() {
    setVal(output(getInVal(0), getInVal(1)),0);
}

bool NandGate::output(bool a, bool b) {
    bool out = pa.output(a, true) | pb.output(b, true) | na.output(a, nb.output(b, false));
    if (faulty) {
        out = getOut();
    }
    return out;
}

void TriNandGate::output() {
    setVal(output(getWire(0)->get(), getWire(1)->get(), getWire(2)->get()), 0);
}

bool TriNandGate::output(bool a, bool b, bool c) {
    bool out = pa.output(a, true) | pb.output(b, true) | pc.output(c, true) | na.output(a, nb.output(b, nc.output(c, false)));
    if (faulty) {
        out = getOut();
    }
    setVal(out, 0);
    return out;
}

template<unsigned int N>
void MinpNandGate<N>::output() {
    bool arr[nin];
    for (int i = 0; i < nin; i++) {
        arr[i] = getInVal(i);
    }
    setVal(output(arr));
}

template<unsigned int N>
bool MinpNandGate<N>::output(bool *a) {
    bool out = pt[0].output(a[0], true);
    for (int i = 1; i < nin; i++) {
        out |= pt[i].output(a[i], true);
    }
    bool out2 = nt[nin - 1].output(a[nin - 1], false);
    for (int i = nin - 2; i >= 0; i--) {
        out2 = nt[i].output(a[i], out2);
    }
    out |= out2;
    if (faulty) {
        out = getOut();
    }
    setVal(out);
    return out;
}

void AndGate::output() {
    tick();
     //setVal(output(getInVal(0), getInVal(1)), 0);
}

void AndGate::setWire(OutWire*w, int id) {
    node::setWire(w, id);
    ng.setWire(w, id);
}

bool AndGate::output(bool a, bool b) {
    ng.output(a, b);
    ig.output();
    setVal(ig.getWire(0)->get(),0);

    return ig.getWire(0)->get();
}

void AndGate::tick() {
    ng.output();
    ig.output();
}
*/
