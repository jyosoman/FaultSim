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
            std::cout<<"creating invertors"<<std::endl;
            igs=new InvertorGate[sig];
            for(int i=0;i<sig;i++){
                addStartNode(&igs[i],in+i,0);
            }
            std::cout<<"creating and gates"<<std::endl;
            ngs=new AndGateBlock[in];
            std::cout<<"creating or gate block gates"<<std::endl;
            ob.init(in);
            std::cout<<"completed creating or gate block gates"<<std::endl;
            for(int i=0;i<in;i++){
                ngs[i].init(sig+1);
                addStartNode(&ngs[i],i,0);
                int sv=1;
                for(int j=0;j<sig;j++){
                    if((sv&i)==sv){
                        addStartNode(&ngs[i],j+in,j);
                    }else{
                        connect(&igs[j],&ngs[i],0,j);
                    }
                    sv<<=1;
                }
                connect(&ngs[i],&ob,0,i);
            }

            addEndNode(&ob,0,0);
            std::cout<<"completed creating or gate block gates"<<std::endl;
        }
    };
    public:
    Multiplexer():node(ina+siga,1,new MultiplexerNet<ina,siga>()){
    }
    void printName(){
        std::cout<<"Multiplexer"<<std::endl;
    }
};

