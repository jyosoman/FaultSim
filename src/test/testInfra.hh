#include"base.hh"
template <unsigned int in,unsigned int out>class Tester{
    node* nd;
    OutWire arr[in];
    public:
    void testVal(uint64_t v){
        unsigned int m=1;
        for(unsigned int i=0;i<in;i++){
            arr[i].set(v&m);
            m=m<<1;
        }
        nd->output();
        uint64_t r=0;
        for(unsigned int i=0;i<out;i++){
            r|=nd->getWire(i)->get()?1<<i:0;
        }
        printf("%lu %lu\n",v,r);
    }
    Tester<in,out>(node* n){
        nd=n;
        for(unsigned int i=0;i<in;i++)
            nd->setWire(&arr[i],i);

    }
};
