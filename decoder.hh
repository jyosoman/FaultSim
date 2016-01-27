#ifndef __decoder__hh
#define __decoder__hh
#include"gates.hh"
#include"and.hh"
class Decoder:public FaultType{
    InvertorGate* igs,*ogs;
    Wire** wires;
    class gateBlock{
        AndGate* gates;
        int gc;
        public:
        gateBlock(int n){
            int b=n-1;
            gates=new AndGate[b];
            gc=b;
            for(int i=1;i<gc;i++){
                gates[i-1].connect(&gates[i]);
            }

        }
        gateBlock(){
        }
        void init(int n){
            int b=n-1;
            gates=new AndGate[b];
            gc=b;
            for(int i=1;i<gc;i++){
                gates[i-1].connect(&gates[i]);
            }
        }
        bool tick(bool*ins){
            bool last=ins[0];
            for(int i=0;i<gc;i++){
                last=gates[i].output(last,ins[i+1]);
            }
            return last;
        }
    };
    gateBlock* ngs;
    unsigned int ins,outs;
    bool*outp,*tin[2];
    public:
    Decoder(int n){
        igs=new InvertorGate[n];

        ins=n;
        outs=1<<n;
        wires=new Wire*[outs];
        for(int i=0;i<outs;i++)
            wires[i]=new Wire[n];
        igs=new InvertorGate[outs];
        ngs=new gateBlock[outs];
        for(int i=0;i<outs;i++){
            ngs[i].init(n);
        }
        outp=new bool[outs];
        tin[0]=new bool[outs];
        tin[1]=new bool[outs];
    }
    void tick(bool*inp){
        unsigned outv=0;
        bool arr[ins];

        for(int i=0;i<outs;i++){
            int sval=1;
            for(int j=0;j<ins;j++){
                if(sval&inp[ins]){
                    arr[j]=true;
                }else{
                    arr[j]=false;
                }
                sval<<=1;
            }
            outp[i]=ngs[i].tick(arr);
            wires[i].set(outp[i]);
        }
    }

};
#endif
