#include"base.hh"
#include"decoder.hh"
#include"mux.hh"
int main(){
//    DecoderNode<4> decode;
    Multiplexer<16,4> mux;
    OutWire arr[4],arr2[16];
    for(int i=0;i<16;i++)
        mux.setWire(&arr2[i],i);
    for(int i=0;i<4;i++)
        mux.setWire(&arr[i],i+16);

//    arr[0].set(true);
//    decode.output();
}

