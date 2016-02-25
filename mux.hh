#include"gates.hh"
#include"and.hh"
#include"or.hh"
/***
 *
 * Wiring: First comes the data inputs, next comes the signal inputs
 *
 *
 */
template <unsigned int ina, unsigned int siga> class Multiplexer:public node{
    template <unsigned int in, unsigned int sig> class MultiplexerNet:public Network{
        AndGateBlock *ngs;
        InvertorGate* igs;
        OrGateBlock ob;
        public:
        MultiplexerNet<in,sig>():Network(in+sig,1){
            igs=new InvertorGate[sig];
            for(unsigned int i=0;i<sig;i++){
                addStartNode(&igs[i],in+i,0);
                igs[i].setNodeId(i);
            }
            ngs=new AndGateBlock[in];
            ob.init(in);
            for(unsigned int i=0;i<in;i++){
                ngs[i].init(sig+1);
                ngs[i].setNodeId(i);
                addStartNode(&ngs[i],i,0);
                unsigned int sv=1;
                for(unsigned int j=0;j<sig;j++){
                    if((sv&i)==sv){
                        addStartNode(&ngs[i],j+in,j+1);
                    }else{
                        connect(&igs[j],&ngs[i],0,j+1);
                    }
                    sv<<=1;
                }
                connect(&ngs[i],&ob,0,i);
            }
            addEndNode(&ob,0,0);
        }
    };
    public:
    Multiplexer():node(ina+siga,1,new MultiplexerNet<ina,siga>()){

    }
    void printName(){
        std::cout<<"Multiplexer"<<std::endl;
        node::printName();
    }
};

