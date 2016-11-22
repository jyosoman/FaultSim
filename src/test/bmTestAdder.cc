#include"adder.hh"
#include<cstdlib>
#include"testInfra.hh"
void process(int*arr){
    KnowlesAdder<32>*kadder;
    kadder=new KnowlesAdder<32>(arr);
    Tester<32,32,32> T(kadder);
    uint32_t x,y,r;
    for(int j=0;j<5;j++){
        cout<<arr[j]<<"\t";
    }
    cout<<endl;

    for(int i=0;i<1000000;i++){
        x=rand();
        y=rand();
        r=T.testVal(x,y);
        if(r!=(x+y)){
            for(int j=0;j<5;j++){
                cout<<arr[j]<<"\t";
            }
            printf("%u %u: %u x %u\n",x,y,r,x+y);
        }
    }

}
void getLC(int l, int c,int *arr){
    if (l==5){
        process(arr);
        return ;
    }
    for(int i=c;i<=l;i++){
        arr[l]=i;
        getLC(l+1,i,arr);
    }
    return ;
}
int main(int argc, char*argv[]){
    KnowlesAdder<32>*kadder;
    kadder=new KnowlesAdder<32>();
    Tester<32,32,32> T(kadder);


    /* cout<<"Testing begins"<<endl; */
    /* T.testVal(0xffffffff,0xffffffff); */
    /* T.testVal(0x7000,0x9000); */
    /* T.testVal(0x0070,0x0090); */
    /* T.testVal(0xefffffff,0xfefefefe); */
    uint32_t x,y,r;
    /* for(int i=0;i<1000000;i++){ */
    /*     x=rand(); */
    /*     y=rand(); */
    /*     r=T.testVal(x,y); */
    /*     if(r!=(x+y)){ */
    /*         printf("%u %u: %u X %u\n",x,y,r,x+y); */
    /*     } */
    /* } */
    if(argc>1){
        FILE*cFile;
        if(argc==2){
            cFile=fopen("config.txt","r");
        }else{
            cFile=fopen(argv[2],"r");
        }
        int eNum;
        fscanf(cFile,"%d",eNum);
        for(int i=0;i<eNum;i++){
            int l,r;
            fscanf(cFile,"%d %d\n",&l,&r);
            FaultType::FLiterator fliter=FaultType::flist.begin();
            std::advance(fliter, l);(*fliter)->setFaulty();
            for(int i=l;i<r;i++,++fliter){
                (*fliter)->setFaulty();
            }
        }

        FILE*fp;
        fp=fopen(argv[1],"r");
        printf("%s \n",argv[1]);
        unsigned int x,y,z;
        char arr[50];
        while(fscanf(fp,"%s %u %u %u\n",arr,&x,&y,&z)!=EOF){
            r=T.testVal(x,y);
            if(r!=z){
                printf("%u %u: %u X %u\n",x,y,r,x+y);
            }
        }
    }
}
