#ifndef __newwire_hh__
#define __newwire_hh__
class logicModel;
class WireNew{
    bool val;
    std::list<logicModel*> lmlist;
    void trigger();
    public:

    Wire(bool v);
    Wire();

    void set(bool v);
    void addList(logicModel* lm);
    bool get();
};
