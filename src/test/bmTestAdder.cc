#include"adder.hh"
#include<cstdlib>
#include"testInfra.hh"
#include<string>
#include<cstring>
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
extern "C" char* runMain(int argc, char*argv[]){
    KnowlesAdder<32>*kadder;
    kadder=new KnowlesAdder<32>();
    Tester<32,32,32> T(kadder);


    int l,r;
    string retString="";
    if(argc>1){
        FILE*cFile=NULL;
        bool fromFile=false;
        if(argc==3){
            cFile=fopen("config.txt","r");
            cout<<"Config.txt"<<endl;
            fromFile=true;
        }else{
            if(argc==4){
                cFile=fopen(argv[2],"r");
                fromFile=true;
            }            
        }
        if(fromFile){
            int eNum=0;
            int retv=fscanf(cFile,"%d",&eNum);
            cout<<retv<<endl;
            for(int j=0;j<eNum;j++){
                /* int l,r; */
                fscanf(cFile,"%d %d\n",&l,&r);
                retString+=std::to_string(l)+" "+std::to_string(r)+" ";
                /* cout<<l<<" "<<r<<endl; */
                FaultType::FLiterator fliter=FaultType::flist.begin();
                std::advance(fliter, l);(*fliter)->setFaulty();
                for(int i=l;i<r;i++,++fliter){
                    (*fliter)->setFaulty();
                }
            }
        }else{
            l=atoi(argv[2]),r=atoi(argv[3]);
            retString+=to_string(l)+" "+to_string(r)+" "+string(argv[4]);
            FaultType::FLiterator fliter=FaultType::flist.begin();
            std::advance(fliter, l);(*fliter)->setFaulty();
            for(int i=l;i<r;i++,++fliter){
                (*fliter)->setFaulty();
            }
        }

        FILE*fp;
        fp=fopen(argv[1],"r");
        /* printf("%s \n",argv[1]); */
        unsigned int x=0,y=0,z=0,ec=0;
        char arr[50];
        int rv;
        while(fscanf(fp,"%s %u %u %u\n",arr,&x,&y,&z)!=EOF){
            rv=T.testVal(x,y);
            if(rv!=z){
                ec++;
                /* printf("%u %u: %u X %u\n",x,y,rv,x+y); */
            }
        }
        /* cout<<l<<" "<<r<<"\t"<<"Error Count is "<<ec<<endl; */
        retString+="Error Count: "+to_string(ec);
    }
    char* arr=(char*)malloc(retString.length());
    strcpy(arr,retString.c_str());
    delete kadder;
    return arr;

}
int main(int argc, char*argv[]){
    cout<<runMain(argc,argv)<<" "<<argv[argc-1]<<endl;
    return 0;
    /* KnowlesAdder<32>*kadder; */
    /* kadder=new KnowlesAdder<32>(); */
    /* Tester<32,32,32> T(kadder); */


    /* uint32_t x,y; */
    /* int l,r; */
    /* if(argc>1){ */
    /*     FILE*cFile=NULL; */
    /*     bool fromFile=false; */
    /*     if(argc==2){ */
    /*         cFile=fopen("config.txt","r"); */
    /*         cout<<"Config.txt"<<endl; */
    /*     }else{ */
    /*         if(argc==3){ */
    /*             cFile=fopen(argv[2],"r"); */
    /*         } */            
    /*     } */
    /*     if(fromFile){ */
    /*         int eNum=0; */
    /*         int retv=fscanf(cFile,"%d",&eNum); */
    /*         cout<<retv<<endl; */
    /*         for(int j=0;j<eNum;j++){ */
    /*             /1* int l,r; *1/ */
    /*             fscanf(cFile,"%d %d\n",&l,&r); */
    /*             /1* cout<<l<<" "<<r<<endl; *1/ */
    /*             FaultType::FLiterator fliter=FaultType::flist.begin(); */
    /*             std::advance(fliter, l);(*fliter)->setFaulty(); */
    /*             for(int i=l;i<r;i++,++fliter){ */
    /*                 (*fliter)->setFaulty(); */
    /*             } */
    /*         } */
    /*     }else{ */
    /*         l=atoi(argv[2]),r=atoi(argv[3]); */
    /*         FaultType::FLiterator fliter=FaultType::flist.begin(); */
    /*         std::advance(fliter, l);(*fliter)->setFaulty(); */
    /*         for(int i=l;i<r;i++,++fliter){ */
    /*             (*fliter)->setFaulty(); */
    /*         } */
    /*     } */

    /*     FILE*fp; */
    /*     fp=fopen(argv[1],"r"); */
    /*     /1* printf("%s \n",argv[1]); *1/ */
    /*     unsigned int x=0,y=0,z=0,ec=0; */
    /*     char arr[50]; */
    /*     int rv; */
    /*     while(fscanf(fp,"%s %u %u %u\n",arr,&x,&y,&z)!=EOF){ */
    /*         rv=T.testVal(x,y); */
    /*         if(rv!=z){ */
    /*             ec++; */
    /*             /1* printf("%u %u: %u X %u\n",x,y,rv,x+y); *1/ */
    /*         } */
    /*     } */
    /*     cout<<l<<" "<<r<<"\t"<<"Error Count is "<<ec<<endl; */
    /* } */
}
