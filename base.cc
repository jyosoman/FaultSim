#include"base.hh"
#include<iostream>
Wire::Wire(bool v){
    val=v;
}
Wire::Wire(){
    val=false;
}

void Wire::trigger(){
    std::cout<<"triggerred"<<std::endl;    
    std::list<logicModel*>::const_iterator iterator;
    for (iterator = lmlist.begin(); iterator != lmlist.end(); ++iterator){
//       pq.push(*iterator); 
       (*iterator)->output();     
    }
}
/*
bool Wire::Compare::operator()(logicModel* a, logicModel* b)
{
    if(a->getLevel()>b->getLevel())
        return true;
    return false;
}
*/
void Wire::addList(logicModel*lm){
    lmlist.push_back(lm);
}
void Wire::set(bool v){
    if(v!=val)
        trigger();
    val=v;
}
bool Wire::get(){
    return val;
 } 
/* logicModel::logicModel(){ *
*     wout=new Wire; 
*     inCount=0; 
* } */
bool logicModel::getOutput(){
    return wout->get();
}
logicModel::logicModel(int n=2){
    wout=new Wire;
    wins=new Wire*[n];
    inCount=0;
    level=0;
    clocked=false;
}
void logicModel::setWire(Wire* w,int id){
    w->addList(this);
    wins[id]=w;
}
void logicModel::connect(logicModel* lm){
    lm->setWire(wout);
    lm->setLevel(level+1);
}
void logicModel::setWire(Wire* w){
    w->addList(this);
    wins[inCount++]=w;
}
/* void logicModel::output(){ *
* } */
Wire* logicModel::getOutWire(){
    return wout;
}
void logicModel::setVal(bool v){
    wout->set(v);
}
int logicModel::getLevel(){
    return level;
}
void logicModel::setLevel(int l){
    if(clocked){
        level=0;
        return;
    }

    if(level<l)
        level=l;
}
Wire* logicModel::getInWire(int id){
    return wins[id];
}
/* std::priority_queue<logicModel*, std::vector<logicModel*>, Wire::Compare> Wire::pq; */
