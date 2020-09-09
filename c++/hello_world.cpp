//This is purely for testing purposes
/* This comment covers multiple lines,
my player */

#include <iostream>
#include <string>
#include <fstream>
#include <cmath>

using namespace std;

class Robot {
    public:
        string brand = "Hewlett-Packard";
        void beep() {
            cout <<  "Hello world!" << endl;
        }
};

//Derived class
class mini_robot: public Robot {
    public:
        string name;
        mini_robot() {
            cout << "Please enter a name for your robot: " << endl;
            cin >> name;
        }
        string model = "Terminator 3000";
        string status_report() {
            string string1 = "My name is " + name;
            string string2 = "My brand is " + brand;
            string string3 = "My model is " + model;
            string megastring = string1 + "\n" + string2 + "\n" + string3 + "\n";
            return megastring;
        }
};

int main() {
    mini_robot Bebo;
    string my_string = Bebo.status_report();
    //Create and open .txt file!
    ofstream MyFile("test.txt");
    MyFile << my_string;
    MyFile.close();
    Bebo.beep();
    return 0;
}