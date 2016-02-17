#include"and_impl.hh"
#include"gates.hh"
#include"base.hh"
#include<vector>
using namespace std;
template <unsigned int N> class Decoder:public Network{
    typedef InvertorGate Invertor;
    vector<Invertor*> invs;
    vector<MinpNandGate<N>*> nands;
    vector<Invertor*> outGates;
    public:
    Decoder<N>():Network(N,1<<N){
        invs.resize(N);
        for(unsigned int i=0;i<N;i++){
            invs[i]=new Invertor();
            addStartNode(invs[i],i,0);
        }
        int outs=1<<N;
        nands.resize(outs);
        for(unsigned int i=0;i<outs;i++){
            nands[i]=new MinpNandGate<N>();
            addEndNodes(nands[i],i,0);
            for(int j=0;j<N;j++){
                if((i&(1<<j))!=0){
                    connect(invs[j],nands[i],0,j);
                }else{
                    //nands[i].setWire(inwires[j],j);
                    addStartNode(nands[i],j,j);
                }
            }
        }        
    }
};
template<unsigned int N> class DecoderNode:public node{
    DecoderNode<N>():node(N,1<<N,new Decoder<N>()){
    }
};
