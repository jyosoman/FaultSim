#include"gates.hh"
#include"and.hh"
#include"or.hh"
template <unsigned int in, unsigned int sig> class multiplexer:public Network{

};
template <unsigned int in, unsigned int sig> class MultiplexerNode:public node{
    class AndGateBlock{
        InWire* ins;
        AndGate* gates;
        int gc;
        public:
        AndGateBlock(int n){
            init(n);
        }
        AndGateBlock(){
        }
        void init(int n){
            int b=n;
            gates=new AndGate[b];
            gc=b;
            ins=new InWire[n+1];
        }
        bool tick(){
            bool last=ins[0].get();
            for(int i=0;i<gc;i++){
                last=gates[i].output(last,ins[i+1].get());
            }
            return last;
        }
        void connect(OutWire*w,int id){
            ins[id].setWire(w);
        }
        bool tick(bool*ins){
            bool last=ins[0];
            for(int i=0;i<gc;i++){
                last=gates[i].output(last,ins[i+1]);
            }
            return last;
        }
    };   
    class OrGateBlock{
        OrGate* gates;
        InWire* ins;
        int gc;
        public:
        OrGateBlock(int n){
            init(n);
        }
        OrGateBlock(){
        }
        void init(int n){
            int b=n;
            gates=new OrGate[b];
            gc=b;
            ins=new InWire[n+1];
        }
        void connect(OutWire*w,int id){
            ins[id].setWire(w);
        }
        bool tick(){
            bool last=ins[0].get();
            for(int i=0;i<gc;i++){
                last=gates[i].output(last,ins[i+1].get());
            }
            return last;
        }

        bool tick(bool*ins){
            bool last=ins[0];
            for(int i=0;i<gc;i++){
                last=gates[i].output(last,ins[i+1]);
            }
            return last;
        }
    };   
    AndGateBlock *ngs;
    InvertorGate* igs,*ogs;
    OrGateBlock ob;
    public:
    Multiplexer():node(in+sig,1,NULL){
        ngs=new AndGateBlock[in];
        for(int i=0;i<in;i++){
            ngs[i].init(sig+1);
        }
        ob.init(in);
        igs=new InvertorGate[sig];
        ogs=new InvertorGate[in];
        for(int i=0;i<sig;i++){

        }
    }
    void output(){
        tick();
        node::output();
    }
    bool tick(bool *inp,bool*signals);
    void output(){
                
    }

};

