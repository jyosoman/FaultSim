#include"adder.hh"
#include<cstdlib>
#include"testInfra.hh"
#include<string>
#include<cstring>
#include<ctime>
#include<functional>

extern "C" char* runMain(int argc, char*argv[]){
    KnowlesAdder<32,5>*kadder;
int larr[42][5]={
    {0,0,0,0,0},
{0,0,0,0,1},
{0,0,0,0,2},
{0,0,0,0,3},
{0,0,0,0,4},
{0,0,0,1,1},
{0,0,0,1,2},
{0,0,0,1,3},
{0,0,0,1,4},
{0,0,0,2,2},
{0,0,0,2,3},
{0,0,0,2,4},
{0,0,0,3,3},
{0,0,0,3,4},
{0,0,1,1,1},
{0,0,1,1,2},
{0,0,1,1,3},
{0,0,1,1,4},
{0,0,1,2,2},
{0,0,1,2,3},
{0,0,1,2,4},
{0,0,1,3,3},
{0,0,1,3,4},
{0,0,2,2,2},
{0,0,2,2,3},
{0,0,2,2,4},
{0,0,2,3,3},
{0,0,2,3,4},
{0,1,1,1,1},
{0,1,1,1,2},
{0,1,1,1,3},
{0,1,1,1,4},
{0,1,1,2,2},
{0,1,1,2,3},
{0,1,1,2,4},
{0,1,1,3,3},
{0,1,1,3,4},
{0,1,2,2,2},
{0,1,2,2,3},
{0,1,2,2,4},
{0,1,2,3,3},
{0,1,2,3,4}};
    int l,r;
    string retString="";
    if(argc>4){
        int index=atoi(argv[4]);
        int dataArr[6];
        for(int i=0;i<6;i++){
            dataArr[i]=larr[index][i];
        }


        kadder=new KnowlesAdder<32,5>(dataArr);
        Tester<32,32,32> T(kadder);
        long int varPos[32],varMax[32];
        for(int i=0;i<32;i++){
            varPos[i]=0;
            varMax[i]=0;
        }

        FILE*cFile=NULL;
        bool fromFile=false;
        /* if(argc==3){ */
        /*     cFile=fopen("config.txt","r"); */
        /*     cout<<"Config.txt"<<endl; */
        /*     fromFile=true; */
        /* }else{ */
        /*     if(argc==4){ */
        /*         cFile=fopen(argv[2],"r"); */
        /*         fromFile=true; */
        /*     } */            
        /* } */
        /* if(fromFile){ */
        /*     int eNum=0; */
        /*     int retv=fscanf(cFile,"%d",&eNum); */
        /*     cout<<retv<<endl; */
        /*     for(int j=0;j<eNum;j++){ */
        /*         /1* int l,r; *1/ */
        /*         fscanf(cFile,"%d %d\n",&l,&r); */
        /*         retString+=std::to_string(l)+" "+std::to_string(r)+" "; */
        /*         /1* cout<<l<<" "<<r<<endl; *1/ */
        /*         FaultType::FLiterator fliter=FaultType::flist.begin(); */
        /*         std::advance(fliter, l);(*fliter)->setFaulty(); */
        /*         for(int i=l;i<r;i++,++fliter){ */
        /*             (*fliter)->setFaulty(); */
        /*         } */
        /*     } */
        /* }else */
        {
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
                unsigned int bitDiff=(unsigned int)rv^z;
                unsigned int strtIndex=31-__builtin_clz(bitDiff);
                unsigned int mask=1<<strtIndex;
                for(int i=strtIndex;i>=0;i--){
                    if((bitDiff&mask)!=0)
                        varPos[i]++;
                    mask>>=1;
                }
                if(rv!=0&&z!=0){
                    varMax[abs(__builtin_clz(rv)-__builtin_clz(z))]++;
                }
                else{
                    if(rv==0)
                        varMax[__builtin_clz(z)]++;
                    if(z==0)
                        varMax[__builtin_clz(rv)]++;
                }
            }
        }
        retString+="Error Count: "+to_string(ec)+ " ";
        for(int i=31;i>=0;i--){
            retString+=to_string(varPos[i])+","+to_string(varMax[i])+"; ";
        }
    }
    cerr<<"Finishing Task"<<endl;
    char* arr=(char*)malloc(retString.length());
    strcpy(arr,retString.c_str());

    delete kadder;
    return arr;
}
double elapsed(clock_t begin){
    clock_t end = clock();
    return ( double(end - begin) / CLOCKS_PER_SEC);

}
int main(int argc, char*argv[]){
    clock_t begin = clock();
    cout<<runMain(argc,argv)<<" "<<argv[argc-1]<<" ";
    cout<<elapsed(begin)<<endl;

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
