#include<list>
#include <queue>
#include<vector>
#ifndef __base_hh__
#define __base_hh__
class logicModel;
class Wire{
    bool val;
    std::list<logicModel*> lmlist;
    logicModel*lm;
    void trigger();
    public:
    Wire(bool v,logicModel*lm=0);
    Wire();
    void setMaster(logicModel*m){
        lm=m;
    }
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
class logicBlock{
    Wire**wouts,**wins;
    int inCount, outCount;
    bool clocked;
    std::vector< <std::list<logicModel*> > levels;
    std::vector<logicBlock*> nextBlocks;
public:
    
};
#endif
