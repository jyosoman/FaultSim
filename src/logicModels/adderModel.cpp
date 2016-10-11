#include<iostream>
#include<algorithm>
#include<cstdio>
using namespace std;
/* struct node_t; */

typedef struct node_t{
    struct node_t* prev,*next;
}node_t;
class redBox{
    public:
void redBoxFunc(bool outArr[],bool a, bool b){
    outArr[0]=a^b;
    outArr[1]=a&b;
}
};
class yellowBox{

    public:
void yellowBoxFunc(bool outArr[],bool pga[],bool pgb[]){
    outArr[0]=pga[0]&pgb[0];
    outArr[1]=(pga[0]&pgb[1])|pga[1];
}
};

class buffer{
    bool p,g;
    public:
        void bufferFunc(bool p, bool g){
            this->p=p;
            this->g=g;
        }
};
void getConnections(int arr[],int connections[6][32]){
    int minArr[6][32];
    for(int i=0;i<32;i++){
        minArr[0][i]=i;
        connections[0][i]=i;
    }
    int prePitch=1;
    for(int i=1;i<=5;i++){
        int pitch=1<<arr[i-1];
        for(int j=0;j<pitch;j++){
            minArr[i][j]=minArr[i-1][j];
        }
        for(int k=0;k<pitch;k++){
            connections[i][k]=k;
        }
        for(int j=1;j<32/pitch;j++){
            for(int k=0;k<pitch;k++){
                if(minArr[i-1][j*pitch+k]!=0){
                    connections[i][j*pitch+k]=minArr[i-1][pitch-1+j*pitch]-1;
                    minArr[i][j*pitch+k]=minArr[i-1][minArr[i-1][pitch-1+j*pitch]-1];
                }else{
                    minArr[i][j*pitch+k]=0;
                    connections[i][j*pitch+k]=j*pitch+k;
                }
            }
            for(int k=0;k<pitch/prePitch;k++){
                bool flag=false;
                for(int l=0;l<prePitch;l++){
                    if(connections[i][j*pitch+k*prePitch+l]!=connections[i-1][j*pitch+k*prePitch+l]){
                        flag=true;
                    }
                }
                if(flag==false){
                    /* printf("%d %d %d %d\n",i,j*pitch+k,prePitch,pitch); */
                    for(int l=0;l<prePitch;l++){
                        connections[i-1][j*pitch+k*prePitch+l]=j*pitch+k*prePitch+l;
                    }

                }
            }
        }
        prePitch=pitch;
        for(int j=0;j<32;j++){
            /* printf("%d\t",connections[i][j]); */
        }
        /* printf("\n"); */
    }

}


class BlackCell{
    public:
    bool arr[2]; //g,p
    BlackCell(){
    }
    void process(bool iarr[],bool jarr[]){
        arr[0]=iarr[0]|(iarr[1]&jarr[0]);
        arr[1]=iarr[1]|jarr[1];
    }

};
class GrayCell{
    public:
    bool arr; //g
    
    GrayCell(){
        arr=false;
    }
    
    void process(bool iarr[],bool jarr[]){
        arr=iarr[0]|(iarr[1]&jarr[0]);
    }

};


void process(int arr[]){
    int connections[6][32];
    getConnections(arr,connections);    
    






    




    /* printf("Result:\n"); */
    /* printf("0 \t"); */
    /* for(int j=0;j<32;j++){ */
    /*     printf("%d\t",connections[0][j]); */
    /* } */
    /* printf("\n"); */

    /* for(int i=1;i<6;i++){ */
    /*     cout<<(1<<arr[i-1])<<"\t"; */
    /*     for(int j=0;j<32;j++){ */
    /*         if(connections[i][j]!=j){ */
    /*             printf("%d\t",connections[i][j]); */
    /*         }else{ */
    /*             printf("X\t"); */
    /*         } */
    /*     } */
    /*     printf("\n"); */
    /* } */
    /* printf("\n"); */
    
}
void getLC(int l, int c,int arr[]){
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
int main(){

    //Enumerate
    int dataArr[5];     
    dataArr[0]=0;
    dataArr[1]=0;
    dataArr[2]=2;
    dataArr[3]=3;
    dataArr[4]=3;
    process(dataArr);
//    getLC(0,0,dataArr);
    //Validate
    //
    //Count


    return 0;
}
