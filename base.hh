#include<list>
#include <queue>
#ifndef __base_hh__
#define __base_hh__
class logicModel;
class Wire{
    bool val;
    std::list<logicModel*> lmlist;
    void trigger();
    public:
    /* class Compare */
    /* { */
    /*     public: */
    /*         bool operator() (logicModel* a, logicModel* b); */
    /* }; */

    /* static std::priority_queue<logicModel*, std::vector<logicModel*>, Compare> pq; */

    Wire(bool v);
    Wire();

    void set(bool v);
    void addList(logicModel* lm);
    bool get();
};

class logicModel{
    Wire *wout,**wins;
    int inCount,level;
    bool clocked;
    public:
    logicModel();
    bool getOutput();
    logicModel(int n);
    void setLevel(int l);
    int getLevel();
    bool isClocked(){
        return clocked;
    }
    void setClocked(){
        clocked=true;
    }
    virtual void setWire(Wire* w,int id);
    virtual void setWire(Wire* w);
    virtual void output()=0;
    Wire* getOutWire();
    void connect(logicModel*lm);
    void setVal(bool v);
    Wire* getInWire(int id);
};
#endif
