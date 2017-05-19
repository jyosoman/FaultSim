#include"adder.hh"
#include<cstdlib>
#include"testInfra.hh"
#include<string>
#include<cstring>

extern "C" char* runMain(int argc, char*argv[]){
    KnowlesAdder<32,5>*kadder;
    kadder=new KnowlesAdder<32,5>();
    Tester<32,32,32> T(kadder);


    int l,r;
    string retString=" ";
    if(argc>1){
        FILE*cFile=NULL;
        bool fromFile=false;
        if(argc==2){
            cFile=fopen("config.txt","r");
            cout<<"Config.txt"<<endl;
            fromFile=true;
        }else{
            if(argc==3){
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
            retString+=to_string(l)+" "+to_string(r)+" ";
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
        unsigned int rv;
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
    cout<<FaultType::flist.size()<<endl;
    char* arr=(char*)malloc(retString.length());
    strcpy(arr,retString.c_str());
    delete kadder;
    return arr;
}

extern "C" int getFlistSize(){
    return FaultType::flist.size();
}

