#include"flipFlop.hh"

void SRFlipFlop::tick(bool s, bool r, bool clk){
    bool sout, rout;
    sout=clkS.output(s,clk);
    rout=clkR.output(r,clk);
    bool qout,qcout;
    qout=outQ.output(getWire(0)->get(),sout);
    qcout=outQc.output(getWire(1)->get(),rout);
    setVal(qout,0);
    setVal(qcout,1);
}

void SRFlipFlop::output(){
    tick(getInVal(0),getInVal(1),getInVal(2));
    node::output();
}

