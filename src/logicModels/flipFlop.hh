#include"../gates/and.hh"
class SRFlipFlop:public node{
    NandGate clkS, clkR, outQ, outQc;
    public:
    SRFlipFlop():node(3,2,NULL),clkS(),clkR(),outQ(),outQc(){
        getWire(1)->set(true);
        getWire(0)->set(false);
    }
    void tick(bool s, bool r, bool clk);
    void output();
};
class DFlipFlop:public node{
    SRFlipFlop srf;
    InvertorGate ig;
    public:
    DFlipFlop():node(2,2),srf(),ig(){
        srf.setWire(ig.getWire(0),1);
    }
    void tick(bool d, bool clk){
        srf.tick(d,ig.output(d),clk);
        setVal(srf.getWire(0)->get(),0);
        setVal(srf.getWire(1)->get(),1);
        cout<<boolalpha<<d<<" "<<clk<<" "<<srf.getWire(0)->get()<<" "<<srf.getWire(1)->get()<<endl;
    }
    void output(){
        tick(getInVal(0),getInVal(1));
        node::output();
    }
};
class JKFlipFlop:public node{
    class JKFlipFlopNet:public Network{
        TriNandGate tj,tk;
        NandGate outQ,outQc;
        public:
        JKFlipFlopNet():Network(3,2),tj(),tk(),outQ(),outQc(){
            addStartNode(&tj,0,0);
            addStartNode(&tj,2,1);
            addStartNode(&tk,1,0);
            addStartNode(&tk,2,1);
            connect(&outQ,&tk,0,2);
            connect(&outQc,&tj,0,2);
            connect(&tj,&outQ,0,0);
            connect(&tk,&outQc,0,0);
            connect(&outQ,&outQc,0,1);
            connect(&outQc,&outQ,0,1);
            addEndNode(&outQ,0,0);
            addEndNode(&outQc,0,0);
        }
        /* void tick(bool j, bool k, bool clk){ */
        /*     bool jout, kout; */
        /*     jout=tj.output(j,getWire(1)->get(),clk); */
        /*     kout=tk.output(k,getWire(0)->get(),clk); */
        /*     bool qout,qcout; */
        /*     qout=outQ.output(getWire(1)->get(),jout); */
        /*     qcout=outQc.output(getWire(0)->get(),kout); */
        /*     setVal(qout,0); */
        /*     setVal(qcout,1); */
        /* } */
        /* void output(){ */
        /*     tick(getInVal(0),getInVal(1),getInVal(2)); */
        /*     node::output(); */
        /* } */
    };
    public:
    JKFlipFlop():node(3,2,new JKFlipFlopNet()){
        setVal(false,0);
        setVal(true,1);
    }
};


