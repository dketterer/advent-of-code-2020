//
// Created by daniel on 01.12.20.
//

#include <fstream>
#include <vector>
#include <iostream>

using namespace std;


int main() {

    std::ifstream infile("../input.txt");

    std::string line;
    std::vector<string> lines;
    while (std::getline(infile, line)) {
        lines.push_back(line);
    }


    return 0;
}