#include"base.hh"

OutWire::OutWire(bool v){
    val=v;
    changed=false;
}

OutWire::OutWire(){
    val=false;
    changed=false;
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
    for(int i=0;i<inwires.size();i++){
        if(inwires[i]->isChanged()){
            for(int j=0;j<intConns[i].size();j++){
                sch.set(intConns[i][j]);
            }
        }
    }
    sch.tick();
}


void Network::addNode(node* nn){
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
    for(int i=0;i<intConns[inid].size();i++){
        intConns[inid][i]->setWire(w,portId[inid][i]);
    }
}
void Network::runBFS(){
    /* std::cout<<"Running BFS now"<<std::endl; */
    list<node*> bfsTree,nextList;
    nodeVectorIterator iter=outnodes.begin(),end=outnodes.end();
    nodeListIterator iter2;
    int level=1;
    for(;iter!=end;iter++){
        /* std::cout<<"placing node"<<std::endl; */
        nextList.push_back(*iter);
        (*iter)->setLevel(level);
    }
    level++;
    while(true){
        for(iter2=nextList.begin();iter2!=nextList.end();iter2++){
            nodeListIterator iterm=connections[*iter2].begin(),iend=connections[*iter2].end();
            for(;iterm!=iend;iterm++){
                if((*iterm)->getLevel()==0){
                    (*iterm)->setLevel(level);
                    /* std::cout<<"placing node2"<<std::endl; */
                    bfsTree.push_back(*iterm);
                }
            }
        }
        level++;
        nextList.clear();
        for(iter2=bfsTree.begin();iter2!=bfsTree.end();iter2++){
            nodeListIterator iterm=connections[*iter2].begin(),iend=connections[*iter2].end();
            for(;iterm!=iend;iterm++){
                if((*iterm)->getLevel()==0){
                    (*iterm)->setLevel(level);
                    nextList.push_back(*iterm);
                    /* std::cout<<"placing node3"<<std::endl; */
                }
            }
        }
        if(nextList.empty())
            break;
        bfsTree.clear();
        level++;
    }
    for(map<node*,list<node*> >::iterator it = connections.begin(); it != connections.end(); ++it) {
        it->first->setLevel(level-it->first->getLevel());
        /* cout<<it->first->getLevel()<<" "<<endl; */
        it->second.clear();
    }
    connections.clear();
}
void node::resize(int in,int out){
    next.resize(out);
    if(internalNetwork!=NULL){
    }else{
        inWires=new vector<InWire*>();
//        inWires->resize(in);
        for(int i=0;i<in;i++){
            inWires->push_back(new InWire());
        }
        outWires=new vector<OutWire*>();
//        outWires->resize(out);
        for(int i=0;i<out;i++){
            outWires->push_back(new OutWire());
        }

    }
}
node::node(int in, int out,Network*lb){

    //    inWires.resize(in);
    //    outWires.resize(out);
    next.resize(out);
    //    for (int i=0;i<out;i++){
    //        outWires[i]=new Wire;
    //    }
    internalNetwork=lb;
    if(lb!=NULL){
        inWires=&lb->inwires;
        outWires=&lb->outWires;
        lb->runBFS();
    }else{
        inWires=new vector<InWire*>();
        inWires->resize(in);
        for(int i=0;i<in;i++){
            (*inWires)[i]=new InWire();
        }
        outWires=new vector<OutWire*>();
        outWires->resize(out);
        for(int i=0;i<in;i++){
            (*outWires)[i]=new OutWire();
        }

    }
}

void node::setNext(node* next,int xid) {
    if(xid<this->next.size())           {
        this->next[xid].push_back(next);
    }
}

void node::setSch(scheduler<node>* sch) {
    this->sch = sch;
}

bool node::isChanged() const {
    for(int i=0;i<outWires->size();i++)
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
    if(internalNetwork!=NULL){
        internalNetwork->connect(w,id);        
    }
}

void node::setLevel(int level) {
    this->level = level;
}

/* 
 * Functions to allow scheduling
 */

int node::getLevel() {
    return level;
}

void node::output(){
    if(internalNetwork!=NULL)
        internalNetwork->output();
    if(sch!=NULL){
        for(int i=0;i<(*outWires).size();i++){
            if((*outWires)[i]->isChanged()){
                for(int j=0;j<next[i].size();j++){
                    sch->set(next[i][j]);
                }
            }
        }
    }
}

void node::setLm(Network* lm) {
    this->internalNetwork = lm;
}

