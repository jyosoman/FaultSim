#include"base.hh"
#include"decoder.hh"
int main(){
    DecoderNode<4> decode;
    OutWire arr[4];
    for(int i=0;i<4;i++)
        decode.setWire(&arr[i],i);
    arr[0].set(true);
    decode.output();
}

