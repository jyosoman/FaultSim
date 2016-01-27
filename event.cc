#include"event.hh"
template <class lm>
bool eventManager<lm>::Compare::operator()(lm* a, lm* b)
{
    if(a->getLevel()>b->getLevel())
        return true;
    return false;
}
