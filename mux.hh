#include"gates.hh"
#include"and.hh"
#include"or.hh"
class Multiplexer{
    class AndGateBlock{
        AndGate* gates;
        int gc;
        public:
        AndGateBlock(int n){
            int b=n;
            gates=new AndGate[b];
            gc=b;
        }
        AndGateBlock(){
        }
        void init(int n){
            int b=n;
            gates=new AndGate[b];
            gc=b;
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
        int gc;
        public:
        OrGateBlock(int n){
            int b=n;
            gates=new OrGate[b];
            gc=b;
        }
        OrGateBlock(){
        }
        void init(int n){
            int b=n;
            gates=new OrGate[b];
            gc=b;
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
    int ins,outs;
    bool outp;
    public:
    Multiplexer(int n){
        ngs=new AndGateBlock[outs];
        for(int i=0;i<outs;i++){
            ngs[i].init(n);
        }

        ob.init(n);
        ins=n;
        int x=1<<n;
        outs=x;
        igs=new InvertorGate[x];
        ogs=new InvertorGate[x];
    }
    bool tick(bool *inp,bool*signals);

};
