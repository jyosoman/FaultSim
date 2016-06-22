#ifndef __gates__hh
#define __gates__hh
#include"../base/base.hh"
#include"../base/transistor.hh"
class InvertorGate:public node{
    PMOSTransistor pa;
    NMOSTransistor na;
    public:
    InvertorGate():node(1),pa(),na(){
    }
    void output(){
        output(getInVal(0));
        node::output();
    }
    void printName(){
        cout<<getLevel()<<'\t';
        std::cout<<"Invertor "<<'\t';
        node::printName();
    }

    bool output(bool a){
        bool out=pa.output(a,true)|na.output(a,false);
        setVal(out,0);
        return out;
    }
};
class XORGate:public  node{
    PMOSTransistor pa,pb;
    NMOSTransistor na,nb;
    XORGate():node(2,1,NULL){
    }
    void output(){
       setVal(output(getInVal(0),getInVal(1)),0); 
    }
    bool output(bool a,bool b){
        bool ab=pa.output(a,true)|na.output(a,false);
        return (pb.output(b,a)|nb.output(b,ab));
    }
    void printName(){
        cout<<getLevel()<<'\t';
        std::cout<<"XOR Gate "<<std::endl;
        node::printName();
    }

};
class BufferGate:public node{
    public:
        BufferGate():node(1,1){
        }
        void output(){
            setVal(getInVal(0),0);
        }
        void printName(){
            cout<<getLevel()<<'\t';
            std::cout<<"Buffer Gate "<<std::endl;
            node::printName();
        }

};
#endif
