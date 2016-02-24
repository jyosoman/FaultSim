#include"flipFlop.hh"
void SRFlipFlop::setWire(OutWire*w,int id){
    switch (id){
        case 0:
            clkS.setWire(w,0);
            break;
        case 1:
            clkR.setWire(w,0);
            break;
        case 2:
            clkS.setWire(w,1);
            clkR.setWire(w,1);
    }
}
void SRFlipFlop::tick(bool s, bool r, bool clk){
    bool sout, rout;
    sout=clkS.output(s,clk);
    rout=clkR.output(r,clk);
    bool qout,qcout;
    qout=outQ.output(qcprev,sout);
    qcout=outQc.output(qprev,rout);
    qprev=qout;
    qcprev=qcout;
}
void SRFlipFlop::output(){
}
bool SRFlipFlop::outputQ(){
    return qprev;
}
bool SRFlipFlop::outputQC(){
    return qcprev;
}
