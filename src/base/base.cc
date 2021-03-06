#include"base.hh"
#include <algorithm>

OutWire::OutWire(bool v){
    val=v;
    changed=false;
}

OutWire::OutWire(){
    val=false;
    changed=true;
}

void OutWire::set(bool v){
    if(val!=v){
        val=v;
        changed=true;
    }else{
        changed=false;
    }
}

bool OutWire::isChanged(){
    return changed;
}

bool OutWire::get(){
    return val;
}

void Network::output(){
    for(unsigned int i=0;i<inwires.size();i++){
        if(inwires[i]->isChanged())
        {
            for(unsigned int j=0;j<intConns[i].size();j++){
                sch.set(intConns[i][j]);
            }
        }
    }
    sch.tick();
}
Network::~Network(){
    for(int i=0;i<inwires.size();i++){
        delete inwires.at(i);
    }
    for(int i=0;i<allNodes.size();i++){
        delete allNodes[i];
    }

}

void Network::addNode(node* nn){
    if(std::find(allNodes.begin(), allNodes.end(), nn) == allNodes.end())
        allNodes.push_back(nn);
    nn->setSch(&sch);
}

void Network::addInternalNode(node* nn){
    addNode(nn);
}

void Network::addStartNode(node*inNode,int netid,int nodeid){
    addNode(inNode);
    innodes.push_back(inNode);
    inNode->setWire(inwires[netid]->getWire(),nodeid);
    intConns[netid].push_back(inNode);
    portId[netid].push_back(nodeid);
}

void Network::addEndNode(node*endNode,int netid,int nodeid){
    addNode(endNode);
    outnodes.push_back(endNode);
    (outWires)[netid]=endNode->getWire(nodeid);
}

void Network::connect(node*a,node*b,int ida,int idb){
    a->connect(b,ida,idb);
    connections[b].push_back(a);
}
void Network::connect(OutWire* w,int inid){
    inwires[inid]->setWire(w);
    for(unsigned int i=0;i<intConns[inid].size();i++){
        intConns[inid][i]->setWire(w,portId[inid][i]);
    }
}
void Network::runBFS(){
    list<node*> bfsTree,nextList;
    nodeVectorIterator iter=outnodes.begin(),end=outnodes.end();
    nodeListIterator iter2;
    unsigned int level=1;
    for(;iter!=end;iter++){
        nextList.push_back(*iter);
        (*iter)->setLevel(level);
    }
    level++;
    while(true){
        for(iter2=nextList.begin();iter2!=nextList.end();iter2++){
            nodeListIterator iterm=connections[*iter2].begin(),iend=connections[*iter2].end();
            for(;iterm!=iend;iterm++){
                if((*iterm)->getLevel()!=level){
                    (*iterm)->setLevel(level);
                    bfsTree.push_back(*iterm);
                }
            }
        }
        if(bfsTree.empty())
            break;
        level++;
        nextList.clear();
        for(iter2=bfsTree.begin();iter2!=bfsTree.end();iter2++){
            nodeListIterator iterm=connections[*iter2].begin(),iend=connections[*iter2].end();
            for(;iterm!=iend;iterm++){
                if((*iterm)->getLevel()!=level){
                    (*iterm)->setLevel(level);
                    nextList.push_back(*iterm);
                }
            }
        }
        if(nextList.empty())
            break;
        bfsTree.clear();
        level++;
    }
    level--;
    for(map<node*,list<node*> >::iterator it = connections.begin(); it != connections.end(); ++it) {
        it->first->setLevel(level-it->first->getLevel());
        addInternalNode(it->first);
        it->second.clear();
    }
    connections.clear();
}
void node::resize(int in,int out){
    next.resize(out);
    if(internalNetwork!=NULL){
    }else{
        if(inWires==NULL){
            inWires=new vector<InWire*>();
        }
        inWires->reserve(in);
        for(int i=inWires->size();i<in;i++){
            inWires->push_back(new InWire());
        }
        if(outWires==NULL)
            outWires=new vector<OutWire*>();

        outWires->reserve(out);
        for(int i=outWires->size();i<out;i++){
            outWires->push_back(new OutWire());
        }
    }
    output();
}

int node::objCount=0;
node::node(int in, int out,Network*lb){
    level=0;
    lastSched=-1;
    next.resize(out);
    nodeid=objCount;
    objCount++;
    internalNetwork=lb;
    inWires=NULL;
    outWires=NULL;
    sch=NULL;
    inc=in;
    outc=out;
    if(lb!=NULL){
        sch=&(lb->sch);
        inWires=&lb->inwires;
        outWires=&lb->outWires;
        lb->runBFS();
    }else{
        inWires=new vector<InWire*>();
        inWires->reserve(in);
        for(int i=0;i<in;i++){
            inWires->push_back(new InWire());
        }
        outWires=new vector<OutWire*>();
        outWires->reserve(out);
        for(int i=0;i<out;i++){
            outWires->push_back(new OutWire(false));
        }
    }
    output();
}

void node::setNext(node* next,int xid) {
    if(((unsigned int)xid)<this->next.size())           {
        this->next[xid].push_back(next);
    }else{
        cout<<"Something went wrong!!"<<endl;
    }
}

void node::setSch(scheduler<node>* sch) {
    this->sch = sch;
}

bool node::isChanged() const {
    for(unsigned int i=0;i<outWires->size();i++)
        if((*outWires)[i]->isChanged())
            return true;
    return false;
}

bool node::isChanged(int i) const {
    if((*outWires)[i]->isChanged())
        return true;
    return false;
}

void node::connect(node*nm,int id,int yid){
    setNext(nm,id);
    nm->setWire(getWire(id),yid);
}

OutWire* node::getWire(int id){
    return (*outWires)[id];
}

void node::setWire(OutWire*w,int id){
    (*inWires)[id]->setWire(w);
//    output();
    if(internalNetwork!=NULL){
        internalNetwork->connect(w,id);        
    }
}

void node::setLevel(unsigned int level) {
    this->level = level;
}

/* 
 * Functions to allow scheduling
 */

unsigned int node::getLevel() {
    return level;
}


void node::output(){
    if(internalNetwork!=NULL)
        internalNetwork->output();
    if(sch!=NULL){
        for(unsigned int i=0;i<(*outWires).size();i++){
            if(getWire(i)->isChanged()){
                for(unsigned int j=0;j<next[i].size();j++){
                    sch->set(next[i][j]);
                }
            }
        }
    }else{
        for(unsigned int i=0;i<(*outWires).size();i++){
            if(getWire(i)->isChanged()){
                for(unsigned int j=0;j<next[i].size();j++){
                    next[i][j]->output();
                }
            }
        }
    }
    /* cout<<"scheduling next"<<endl; */
}

void node::setLm(Network* lm) {
    this->internalNetwork = lm;
}

