#include"base.hh"
template <unsigned int in1,unsigned int in2,unsigned int out>class Tester{
    node* nd;
    OutWire arr[in1+in2];
    public:
    void testVal(uint32_t v1,uint32_t v2){
        unsigned int m=1;
        for(unsigned int i=0;i<in1;i++){
            arr[i].set(v1&m);
            m=m<<1;
        }
        m=1;
        for(unsigned int i=in1;i<in1+in2;i++){
            arr[i].set(v2&m);
            m=m<<1;

        }
        uint32_t r=0;

        nd->output();
        for(unsigned int i=0;i<out;i++){
            r|=nd->getWire(i)->get()?1<<i:0;
        }
        printf("Result: %u %u %u\n",v1,v2,r);
        printf("Result: %x %x %x\n",v1,v2,r);
    }
    Tester<in1,in2,out>(node* n){
        nd=n;
        for(unsigned int i=0;i<in1+in2;i++){
            nd->setWire(&arr[i],i);
        }

    }
};
