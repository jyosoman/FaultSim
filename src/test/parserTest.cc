#include"parser.hh"
using namespace std;
int main(){
    string x="a|(a&~b)";
    cout<<parseThis(x)<<endl;
    return 0;
}
