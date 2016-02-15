#include"and.hh"
#include"decoder.hh"
#include<iostream>
using namespace std;
int main(){
    OutWire a(true);
    OutWire b(true);
    NandGate g;
    g.setWire(&a,0);
    g.setWire(&b,1);
    cout<<a.get()<<endl;
    a.set(false);
    cout<<a.get()<<endl;
    Decoder<4> d;
    
    return 0;
}
