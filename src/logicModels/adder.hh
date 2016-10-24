#include"../gates/and_impl.hh"
#include"../gates/or.hh"
#include"../gates/gates.hh"
#include<stdint.h>
using namespace std;

class FullAdder:public node{
    class FullAdderNet:public Network{
        NandGate* nands;
        public:
        FullAdderNet():Network(3,2){
            nands=new NandGate[9];
            addStartNode(&nands[0],0,0);
            addStartNode(&nands[0],1,0);
            addStartNode(&nands[1],0,0);
            addStartNode(&nands[2],1,1);
            addStartNode(&nands[6],2,1);
            addStartNode(&nands[4],2,1);
            connect(&nands[0],&nands[1],0,1);
            connect(&nands[0],&nands[2],0,0);
            connect(&nands[1],&nands[3],0,0);
            connect(&nands[2],&nands[3],0,1);
            connect(&nands[3],&nands[4],0,0);
            connect(&nands[4],&nands[5],0,1);
            connect(&nands[3],&nands[5],0,0);
            connect(&nands[4],&nands[6],0,1);
            connect(&nands[6],&nands[7],0,1);
            connect(&nands[5],&nands[7],0,0);
            connect(&nands[0],&nands[8],0,1);
            connect(&nands[4],&nands[8],0,0);
            addEndNode(&nands[7],0,0);
            addEndNode(&nands[8],1,0);
        }
    };
    public:
    FullAdder():node(3,2,new FullAdderNet()){
    }
};
class CLABlock:public node{
    XORGate p;
    AndGate g;
    CLABlock():node(3,2,NULL){

    }
    void output(){
        setVal(p.output(getInVal(0),getInVal(1)),0);
        setVal(g.output(getInVal(0),getInVal(1)),1);
    }
};

class AdderBlocks:public node{
    public:
        static int x;
        int selfid;
        AdderBlocks(int in,int out):node(in,out){
            selfid=x;
            x++;
        }
        void printIn(int id){
            cout<<boolalpha<<getInVal(id)<<" ";
        }
        void printOut(int id){
            cout<<boolalpha<<getWire(id)->get()<<" ";
        }
        void printVals(){
            cout<<getLevel()<<" ";
            for(int i=0;i<getInCount();i++)printIn(i);//cout<<endl;
            for(int i=0;i<getOutCount();i++)printOut(i);
            cout<<endl;

        }
};

int AdderBlocks::x=0;
class BlackCell:public AdderBlocks{
    AndGate a,b;
    OrGate c;
    public:
    BlackCell():AdderBlocks(4,2){
    }
    void printName(){
        cout<<"BlackCell :"<<selfid<<"\t";
        printVals();
    }
    void output(){
        setVal(c.output(getInVal(0),a.output(getInVal(1),getInVal(2))),0);
        setVal(b.output(getInVal(1),getInVal(3)),1);
        /* printName(); */
            node::output();
        /* printName(); */
    }
};
class GrayCell:public AdderBlocks{
    OrGate b;
    AndGate a;
    public:
    GrayCell():AdderBlocks(3,1){
    }
    void printName(){
        cout<<"GrayCell :"<<selfid<<"\t";
        printVals();
    }

    void output(){
        setVal(b.output(getInVal(0),a.output(getInVal(1),getInVal(2))),0);
        /* printName(); */
        node::output();
        /* printName(); */
    }
};

class BaseCell:public AdderBlocks{
    public:
        bool arr[2];
        AndGate g;
        XORGate p;
        BaseCell():AdderBlocks(2,2){
            arr[0]=arr[1]=false;
        }
        void printName(){
            cout<<"Name:BaseCell :"<<selfid<<"\t";
            printVals();
        }

        void output(){
            setVal(g.output(getInVal(0),getInVal(1)),0);
            setVal(p.output(getInVal(0),getInVal(1)),1);
            /* printName(); */
            node::output();
            /* printName(); */
        }
};

class BufferCell:public AdderBlocks{
    BufferGate g;
    public:
    BufferCell():AdderBlocks(1,1){
    }
    void printName(){
        cout<<"BufferCell :"<<selfid<<"\t";
        printVals();
    }

    void output(){
        setVal(g.output(getInVal(0)),0);
        node::output();
        /* printName(); */
    }
};
class XORCell:public AdderBlocks{
    XORGate g;
    public:
    XORCell():AdderBlocks(2,1){
    }
    void printName(){
        cout<<"XORCell :"<<selfid<<"\t";
        printVals();
    }

    void output(){
        setVal(g.output(getInVal(0),getInVal(1)),0);
        /* printName(); */
        node::output();
        /* printName(); */
    }
};

template<int N> class KnowlesAdder:public node{
    public:
        template<int Z> class KnowlesAdderNetwork:public Network{
            void getConnections(int arr[],int connections[6][32],int minArr[7][32]){
                for(int i=0;i<32;i++){
                    minArr[0][i]=i;
                    connections[0][i]=i;
                }
                int prePitch=1;
#ifdef DEBUG
                for(int i=0;i<32;i++)
                    printf("%d\t",i+1);
                cout<<endl;
                for(int i=0;i<32;i++)
                    cout<<"=\t";
                cout<<endl;

#endif
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
#ifdef DEBUG                    
                    for(int j=0;j<32;j++){
                        printf("%d\t",connections[i][j]);
                    }
                    printf("\n");
#endif
                }
                for(int j=0;j<32;j++){
                    minArr[6][j]=0;
                }
            }
            node *blocks[7][33],*firstRow[33];
            public:
            KnowlesAdderNetwork<Z>():Network(64,32){
                firstRow[0]=new BaseCell;
                blocks[0][0]=firstRow[0];
                OutWire* wr=new OutWire(false);
                firstRow[0]->setWire(wr,0);
                firstRow[0]->setWire(wr,1);
                for(int i=0;i<32;i++){
                    firstRow[i+1]=new BaseCell;
                    blocks[0][i+1]=firstRow[i+1];
                    addStartNode(blocks[0][i+1],i,0); //A
                    addStartNode(blocks[0][i+1],i+32,1);//B
                }
                int dataArr[6];
                dataArr[0]=0;
                dataArr[1]=0;
                dataArr[2]=2;
                dataArr[3]=3;
                dataArr[4]=3;
                int connections[7][32];
                int minArr[7][32];
                getConnections(dataArr,connections,minArr);
                for(int i=0;i<32;i++){
                    connections[6][i]=i;
                }
                for(int i=1;i<6;i++){
                    for(int j=0;j<32;j++){
                        if(connections[i][j]==j&&minArr[i][j]==0){
                            blocks[i][j]=new BufferCell;
                            connect(blocks[i-1][j],blocks[i][j],0,0);
                        }else{
                            if(connections[i+1][j]==j&&minArr[i][j]==0){
                                blocks[i][j]=new GrayCell;
                                connect(blocks[i-1][j],blocks[i][j],0,0);
                                connect(blocks[i-1][j],blocks[i][j],1,1);
                                connect(blocks[i-1][connections[i][j]],blocks[i][j],0,2);
                            }else{
                                blocks[i][j]=new BlackCell;
                                connect(blocks[i-1][j],blocks[i][j],0,0);
                                connect(blocks[i-1][j],blocks[i][j],1,1);
                                connect(blocks[i-1][connections[i][j]],blocks[i][j],0,2);
                                connect(blocks[i-1][connections[i][j]],blocks[i][j],1,3);
                            }
                        }
                    }
                }
                for(int j=0;j<32;j++){
                    blocks[6][j]=new XORCell;
                    connect(blocks[5][j],blocks[6][j],0,0); //G
                    connect(firstRow[j+1],blocks[6][j],1,1); //P
                    addEndNode(blocks[6][j],j,0);
                }
            }
        };
        KnowlesAdder<N>():node(2*N,N,new KnowlesAdderNetwork<N>()){
        }

};

class KSAdder:public Network{
    BlackCell* bcells;
    GrayCell* gcells;
    BufferGate* buffers;
    public:
    KSAdder():Network(32,33){
        gcells=new GrayCell[31];
        buffers=new BufferGate[16];
        bcells=new BlackCell[98];        

    }
};





