#include"../gates/and_impl.hh"
using namespace std;

class FullAdder:public node{
    class FullAdderNet:public Network{
        NandGate* nands;
        FullAdderNet():Network(3,2){
            nands=new NandGate[9];
            addStartNode(&nands[0],0,0);
            addStartNode(&nands[0],1,0);
            addStartNode(&nands[1],0,0);
            addStartNode(&nands[2],1,1);
            addStartNode(&nands[6],2,1);
            addStartNode(&nands[4],2,1);
            connect(&nands[0],&nands[1],0,1);
            connect(&nands[0],&nands[2],0,0);
            connect(&nands[1],&nands[3],0,0);
            connect(&nands[2],&nands[3],0,1);
            connect(&nands[3],&nands[4],0,0);
            connect(&nands[4],&nands[5],0,1);
            connect(&nands[3],&nands[5],0,0);
            connect(&nands[4],&nands[6],0,1);
            connect(&nands[6],&nands[7],0,1);
            connect(&nands[5],&nands[7],0,0);
            connect(&nands[0],&nands[8],0,1);
            connect(&nands[4],&nands[8],0,0);
            addEndNode(&nands[7],0,0);
            addEndNode(&nands[8],1,0);
        }
    };
    public:
    FullAdder():node(3,2,new FullAdderNet()){
    }
};
class CLABlock:public node{
    XORGate p;
    AndGate g;
    CLABlock():node(3,2,NULL){

    }
    void output(){
        setVal(p.output(getInVal(0),getInVal(1)),0);
        setVal(g.output(getInVal(0),getInVal(1)),1);
    }
};
class BlackCell:public node{
    AndGate a,b;
    OrGate c;
    public:
    BlackCell():node(4,2){
    }
    void output(){
        setVal(c.output(getInVal(0),a.output(getInVal(1),getInVal(2))),0);
        setVal(b.output(getInVal(2),getInVal(3)),1);
    }
};
class GrayCell:public node{
    OrGate b;
    AndGate a;
    GrayCell():node(3,2){}
    void output(){
        setVal(b.output(getInVal(0),a.output(getInVal(1),getInVal(2))),0);
    }
};

class KSAdder:public Network{
    BlackCell* bcells;
    GrayCell* gcells;
    BufferGate* buffers;
    KSAdder():Network(32,33){
        gcells=new GrayCell[31];
        buffers=new BufferGate[16];
        bcells=new BlackCell[98];        

    }
};




