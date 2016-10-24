#include"parser.hh"
#include"base.hh"
#include"decoder.hh"
#include"mux.hh"
#include"flipFlop.hh"

using namespace std;
int main(){
    string x="a|(a&~b)";
    /* node*net=parseString(x); */
    cout<<x<<endl;    
    return 0;
}
