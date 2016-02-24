#include"base.hh"
#include"decoder.hh"
#include"mux.hh"
#include<cstdio>
int main(){
//    DecoderNode<4> decode;
    OutWire arr[4],arr2[16];
    Multiplexer<16,4> mux;
    AndGateBlock agb(5);
    /*
    AndGate a;
    a.setWire(&arr[0],0);
    a.setWire(&arr[1],1);
    a.test();
    */
     for(int i=0;i<5;i++)
        agb.setWire(&arr2[i],i);
     agb.test();
   
    return 0;
    for(int i=0;i<16;i++)
        mux.setWire(&arr2[i],i);
    for(int i=0;i<4;i++)
        mux.setWire(&arr[i],i+16);



    for(int i=0;i<1;i++){
        arr2[i].set(true);
        for(int j=0;j<1;j++){
            for(int k=0;k<4;k++){
                if(j&1<<k){
                    /* printf("%d %d %d\n",i,j,k); */
                    arr[k].set(true);
                }
            }
            mux.output();
            std::cout<<i<<" "<<j<<" "<<std::boolalpha<<mux.getWire(0)->get()<<'\n';
            for(int k=0;k<4;k++)
                arr[k].set(false);

        }
        arr2[i].set(false);
    }
}

