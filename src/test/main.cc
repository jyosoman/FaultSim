#include"base.hh"
#include"decoder.hh"
#include"mux.hh"
#include"flipFlop.hh"
#include<cstdio>
int main(){
    DFlipFlop f;
//    TriNandGate tj;
    OutWire arr[4];
    /* OutWire arr2[16]; */
//    Multiplexer<16,4> mux;
//    MinpNandGate<4> fin;  
//    Decoder<4> decode;
//    for(int i=0;i<16;i++){
//        mux.setWire(&arr2[i],i);
//    }
    for(int i=0;i<4;i++){
//        mux.setWire(&arr[i],i+16);
//        decode.setWire(&arr2[i],i);
//        fin.setWire(&arr[i],i);
    }
    for(int i=0;i<2;i++){
        f.setWire(&arr[i],i);
//        tj.setWire(&arr[i],i);
    }
    f.test();
//    cout<<FaultType::flist.size()<<endl;
//    FaultType::FLiterator fliter=FaultType::flist.begin();
//    for(;fliter!=FaultType::flist.end();++fliter){
//        (*fliter)->setFaulty();
//    }
//    return 0;
//    f.test();
//    fin.test();
//    decode.test();

    return 0;
    /* for(int i=0;i<16;i++){ */
    /*     arr2[i].set(true); */
    /*     for(int j=0;j<16;j++){ */
    /*         for(int k=0;k<4;k++){ */
    /*             if(j&1<<k){ */
    /*                 arr[k].set(true); */

    /*             }else{ */
    /*                 arr[k].set(false); */
    /*             } */
    /*         } */
    /*          mux.output(); */ 
    /*          std::cout<<i<<" "<<j<<" "<<std::boolalpha<<mux.getWire(0)->get()<<'\n'; */ 
    /*     } */
    /*     arr2[i].set(false); */
    /* } */

    /* return 0; */
    /* return 0; */
}

