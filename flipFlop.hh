#include"and.hh"
class SRFlipFlop:public FaultType{
    NandGate clkS, clkR, outQ, outQc;
    bool qprev,qcprev;
    public:
    SRFlipFlop():clkS(),clkR(),outQ(),outQc(){
        clkS.setClocked();
        clkR.setClocked();
        outQ.setWire(clkS.getOutWire(),0);
        outQ.setWire(outQc.getOutWire(),1);
        outQc.setWire(clkR.getOutWire(),0);
        outQc.setWire(outQ.getOutWire(),1);
        outQ.setLevel(1);
        outQ.setLevel(1);

        qprev=true;
        qcprev=false;
    }
    virtual void setWire(Wire*w,int id);
    void tick(bool s, bool r, bool clk);
    void output();
    bool outputQ();
    bool outputQC();
};
class DFlipFlop:public FaultType{
    SRFlipFlop srf;
    public:
    DFlipFlop():srf(){
    }
    void tick(bool d, bool clk){
        srf.tick(d,!d,clk);
    }
    bool output(){
        return srf.outputQ();
    }
    bool outputC(){
        return srf.outputQC();
    }
};
class JKFlipFlop{
    TriNandGate tj,tk;
    NandGate outQ,outQc;
    bool qprev,qcprev;
    public:
    JKFlipFlop():tj(),tk(),outQ(),outQc(),qprev(true),qcprev(false){
        outQ.setLevel(1);
        outQc.setLevel(1);
    }
    void tick(bool j, bool k, bool clk){
        bool jout, kout;
        jout=tj.output(j,qcprev,clk);
        kout=tk.output(k,qprev,clk);
        bool qout,qcout;
        qout=outQ.output(qcprev,jout);
        qcout=outQc.output(qprev,kout);
        qprev=qout;
        qcprev=qcout;
    }
    bool output(){
        return qprev;
    }
    bool outputC(){
        return qcprev;
    }
};


