#include"adder.hh"
#include<cstdlib>
#include"testInfra.hh"
#include<string>
#include<cstring>
#include<ctime>
/*
 * Function to run a specific Adder design against a given input file.
 *  argv[1]: Data File containing the adder inputs, format: instruction, inpit1, input2, result
 *  argv[2]: Left value of error
 *  argv[3]: right value of error
 *  argv[4]: adder design
 *
 */

double elapsed(clock_t begin){
    clock_t end = clock();
    return ( double(end - begin) / CLOCKS_PER_SEC);

}
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


        l=atoi(argv[2]),r=atoi(argv[3]);
        retString+=to_string(l)+" "+to_string(r)+" "+string(argv[4]);
        FaultType::FLiterator fliter=FaultType::flist.begin();
        std::advance(fliter, l);
        for(int i=l;i<r;i++,++fliter){
            (*fliter)->setFaulty();
        }

       //  kadder->updateFaulty(); 
        int numTest=atoi(argv[1]);
        unsigned int x=0,y=0,z=0,ec=0;
        char arr[50];
        int rv;
        clock_t begin = clock();
        for(int i=0;i<numTest;i++){
            x=rand();
            y=rand();
            z=(x+y);
            rv=T.testVal(x,y);
            if(rv!=z){
                
                ec++;
            }
            
        }
        double timeTaken=elapsed(begin);
        retString+=" Error Count: "+to_string(ec)+" "+to_string(timeTaken);
    }
    cerr<<"Finishing Task"<<endl;
    char* arr=(char*)malloc(retString.length());
    strcpy(arr,retString.c_str());
    return arr;
}
int main(int argc, char*argv[]){
    cout<<runMain(argc,argv)<<endl;

    return 0;
}
