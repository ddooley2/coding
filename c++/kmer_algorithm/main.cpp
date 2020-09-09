#include <sstream>
#include <iostream>
#include <fstream>
#include "kmer_functions.h"

using namespace std;

// Function for printing out vector contents
void print(std::vector <int> const &a) {
   for(int i=0; i < a.size(); i++) {
       if (i == a.size()-1) {
        cout << a.at(i);
       }
       else {
        cout << a.at(i) << ',';
       }
   };
}

int main(int argc, char** argv) 
{ 
    string query = argv[2]; //This will be a short string to query

    //Open text file and read its contents (should be nothing but a sequence file)
    ifstream f(argv[1]);
    stringstream buffer;
    buffer << f.rdbuf();
    
    vector<int> ind = bitap_bitwise_search(buffer.str().c_str(), query.c_str()); //Perform bitap search
    print(ind); //Print indices of all substring matches
    return 0; 
} 