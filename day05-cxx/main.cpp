//
// Created by daniel on 01.12.20.
//

#include <fstream>
#include <vector>
#include <iostream>
#include <algorithm>
#include <boost/algorithm/string.hpp>


int main() {
    std::ifstream infile("../input.txt");

    std::vector<int> seat_ids;

    std::string line;
    while (std::getline(infile, line)) {
        boost::replace_all(line, "F", "0");
        boost::replace_all(line, "B", "1");
        boost::replace_all(line, "L", "0");
        boost::replace_all(line, "R", "1");
        seat_ids.push_back(stoi(line, 0, 2));
    }

    std::sort(seat_ids.begin(), seat_ids.end());
    std::cout << "Part 1: " << seat_ids.back() << std::endl;

    int last = seat_ids.back();
    seat_ids.pop_back();
    while (!seat_ids.empty()) {
        int i = seat_ids.back();
        seat_ids.pop_back();
        if (last - 1 != i and last - 2 == i) {
            std::cout << "Part 2: " << last - 1 << std::endl;
        }
        last = seat_ids.back();
        seat_ids.pop_back();
    }
    return 0;
}