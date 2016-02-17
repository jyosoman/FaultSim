#include"and_impl.hh"
using namespace std;
class FullAdder:public Network{
    NandGate* nands;
    FullAdder():Network(3,1){
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
       runBFS();
    }
};
class FullAdderNode:public node{
    public:
    FullAdderNode():node(3,1,new FullAdder()){
    }
};
