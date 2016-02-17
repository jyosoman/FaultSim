#include"gates.hh"
#include"and.hh"
#include"or.hh"
template <unsigned int in, unsigned int sig> class multiplexer:public Network{
    AndGateBlock *ngs;
    InvertorGate* igs;
    OrGateBlock ob;
    multiplexer<in,sig>():Network(in+sig,1){
        igs=new InvertorGate[sig];
        for(int i=0;i<sig;i++){
            addStartNode(&igs[i],in+i,0);
        }
        ngs=new AndGateBlock[in];
        ob.init(in);
        for(int i=0;i<in;i++){
            ngs[i].init(sig+1);
            addStartNode(&ngs[i],i,0);
            int sv=1;
            for(int j=0;j<sig;j++){
                if((sv&i)==sv){
                    addStartNode(&ngs[i],i+in,j);
                }else{
                    connect(&igs[i],&ngs[i],0,j);
                }
                sv<<=1;
            }
            connect(&igs[i],&ob,0,i);
        }

        addEndNode(&ob,0,0);
        runBFS();
    }
};
template <unsigned int in, unsigned int sig> class MultiplexerNode:public node{
    MultiplexerNode():node(in+sig,1,new multiplexer<in,sig>()){
    }
};

