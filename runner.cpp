#include"baseBlocks.hh"
int main(){
    eventQueue<empty> eq(10);
    for(int i=0;i<100;i++){
        for(int j=5;j<10;j++){
            empty* a=new empty;            
            eq.place(a,j);
        }
    }
    eq.getNext();
}