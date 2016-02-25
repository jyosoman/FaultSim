#include"base.hh"
#include"decoder.hh"
#include"mux.hh"
#include<cstdio>
int main(){
//    DecoderNode<4> decode;
    
    OutWire arr[4],arr2[16];
    Multiplexer<16,4> mux;
   
    
    for(int i=0;i<16;i++){
        mux.setWire(&arr2[i],i);
        arr2[i].set(false);
    }
    for(int i=0;i<4;i++){
        mux.setWire(&arr[i],i+16);
        arr[i].set(true);
    }

    for(int i=0;i<16;i++){
        arr2[i].set(true);
        for(int j=0;j<16;j++){
            for(int k=0;k<4;k++){
                if(j&1<<k){
                    arr[k].set(true);
                }else{
                    arr[k].set(false);
                }
            }
            mux.output();
            std::cout<<i<<" "<<j<<" "<<std::boolalpha<<mux.getWire(0)->get()<<'\n';
            for(int k=0;k<4;k++)
                arr[k].set(false);

        }
        arr2[i].set(false);
    }
    return 0;
}

