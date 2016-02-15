#include"and.hh"
#include"decoder.hh"
#include<iostream>
using namespace std;
int main(){
    Wire a(true);
    Wire b(true);
    NandGate g;
    g.setWire(&a);
    g.setWire(&b);
    cout<<a.get()<<endl;
    a.set(false);
    cout<<a.get()<<endl;
    Decoder d(4);
    
    return 0;
}
