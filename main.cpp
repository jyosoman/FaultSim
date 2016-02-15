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
    Decoder<4> decode;
    OutWire arr[4];
    for(int i=0;i<4;i++)
        decode.connect(&arr[i],i);
    arr[0].set(true);
    decode.output();
   
    return 0;
}
