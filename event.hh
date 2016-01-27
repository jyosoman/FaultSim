#ifndef __event_hh__
#define __event_hh__
#include"base.hh"
#include <queue>
template<class lm>
class eventManager{
    class Compare
    {
        public:
            bool operator() (lm* a, lm* b);
    };
    std::array<queue<lm*>> arrqueues;

    std::priority_queue<lm*, std::vector<lm*>, Compare> pq;
    void push(lm* x){
        pq.push(x);
    }
    lm* top(){
        return pq.top();
    }
    void pop(){
        pq.pop();
    }
    bool empty(){
        return pq.empty();   
    }

    public:

};
#endif
