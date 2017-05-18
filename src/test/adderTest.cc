#include"adder.hh"
#include<cstdlib>
#include"testInfra.hh"
void process(int*arr){
    KnowlesAdder<32,5>*kadder;
    kadder=new KnowlesAdder<32,5>(arr);
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
    int*arr=(int*)calloc(5,sizeof(int));
    getLC(0,0,arr);
    return 0;


}
