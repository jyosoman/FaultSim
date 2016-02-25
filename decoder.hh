#include"and_impl.hh"
#include"gates.hh"
#include"base.hh"
#include<vector>
using namespace std;

template<unsigned int N> class Decoder:public node{
    template <unsigned int R> class DecoderNet:public Network{
        typedef InvertorGate Invertor;
        vector<Invertor*> invs;
        vector<MinpNandGate<R>*> nands;
        vector<Invertor*> outGates;
        public:
        DecoderNet<R>():Network(R,1<<R){
            invs.resize(R);
            for(unsigned int i=0;i<R;i++){
                invs[i]=new Invertor();
                addStartNode(invs[i],i,0);
            }
            unsigned int outs=1<<R;
            nands.resize(outs);
            outGates.resize(outs);
            for(unsigned int i=0;i<outs;i++){
                nands[i]=new MinpNandGate<R>();
                outGates[i]=new Invertor();
                connect(nands[i],outGates[i],0,0);
                addEndNode(outGates[i],i,0);
                for(unsigned int j=0;j<R;j++){
                    if((i&(1<<j))==0){
                        connect(invs[j],nands[i],0,j);
                    }else{
                        //nands[i].setWire(inwires[j],j);
                        addStartNode(nands[i],j,j);
                    }
                }
            }        
        }
    };
    public:
    Decoder<N>():node(N,1<<N,new DecoderNet<N>()){
    }
};
