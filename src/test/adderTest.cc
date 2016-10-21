#include"adder.hh"
#include"testInfra.hh"
int main(){
    KnowlesAdder<32> kadder;
    Tester<32,32,32> T(&kadder);
    cout<<"Testing begins"<<endl;
    /* T.testVal(0x10ff00ff,0x10ff00ff); */
    /* T.testVal(0x000001ff,0x000001ff); */
    /* T.testVal(0xefffffff,0xfefefefe); */
    uint32_t x,y;
    cin>>x;
    cin>>y;
    T.testVal(x,y);
}
