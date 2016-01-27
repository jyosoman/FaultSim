#include"mux.hh"
bool Multiplexer::tick(bool *inp,bool*signals){
    bool outp;
    bool outps[outs];
    bool arr[ins];
    for(int i=0;i<outs;i++){
        int sval=1;
        for(int j=0;j<ins;j++){
            if(sval&i){
                arr[j]=true;
            }else{
                arr[j]=false;
            }
            sval<<=1;
        }
        arr[outs]=
            outps[i]=ngs[i].tick(arr);
    }
    outp=ob.tick(outps);
    return outp;
}

