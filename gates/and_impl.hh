#ifndef __and_impl__hh
#define __and_impl__hh

#include"and.hh"



void NandGate::output() {
    output(getInVal(0), getInVal(1));
    node::output();
}

bool NandGate::output(bool a, bool b) {
    bool out = pa.output(a, true) | pb.output(b, true) | na.output(a, nb.output(b, false));
    setVal(out,0);
    return out;
}

void TriNandGate::output() {
    output(getInVal(0),getInVal(1),getInVal(2));// getWire(1)->get(), getWire(2)->get());
        node::output();
}

bool TriNandGate::output(bool a, bool b, bool c) {
    bool out = pa.output(a, true) | pb.output(b, true) | pc.output(c, true) | na.output(a, nb.output(b, nc.output(c, false)));
    setVal(out, 0);
    return out;
}

template<unsigned int N>
void MinpNandGate<N>::output() {
    bool a1=false,a2=false;
    for(int i=0;i<nin;i++){
        a1=pt[i].output(getInVal(i),true)|a1;
        a2=nt[i].output(getInVal(i),a2);
    }
    bool res=a1|a2;
    setVal(res,0);
    node::output();
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
    setVal(out);
    return out;
}


void AndGate::output() {
     output(getInVal(0), getInVal(1));
        node::output();
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
    setVal(ig.getWire(0)->get(),0);
}

#endif
