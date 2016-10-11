#include"adder.hh"
#include"testInfra.hh"
int main(){
    KnowlesAdder<32> kadder;
    Tester<64,32> T(&kadder);
    T.testVal(0x00ff00ff);
}
