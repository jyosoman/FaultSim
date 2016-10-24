#include"adder.hh"
#include<cstdlib>
#include"testInfra.hh"
int main(int argc, char*argv[]){
    KnowlesAdder<32> kadder;
    Tester<32,32,32> T(&kadder);
    cout<<"Testing begins"<<endl;
    /* T.testVal(0xffffffff,0xffffffff); */
    /* T.testVal(0x7000,0x9000); */
    /* T.testVal(0x0070,0x0090); */
    /* T.testVal(0xefffffff,0xfefefefe); */
    uint32_t x,y;
    if(argc>1){
        x=strtol(argv[1],NULL,16);
        y=strtol(argv[2],NULL,16);
        T.testVal(x,y);
    }
}
