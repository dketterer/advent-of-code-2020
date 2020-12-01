//
// Created by daniel on 01.12.20.
//

#include <fstream>
#include <vector>
#include <iostream>

using namespace std;


int main() {

    std::ifstream infile("../input.txt");

    int a;
    std::vector<int> numbers;
    while (infile >> a) {
        numbers.push_back(a);
    }

    return 0;
}