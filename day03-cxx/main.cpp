//
// Created by daniel on 01.12.20.
//

#include <fstream>
#include <vector>
#include <iostream>

using namespace std;


int main() {

    vector<int> slope_right = {1, 3, 5, 7, 1};
    vector<int> slope_down = {1, 1, 1, 1, 2};

    std::ifstream infile("../input.txt");
    std::string line;
    vector<string> lines;
    // ignore the first line
    std::getline(infile, line);
    while (std::getline(infile, line)) {
        lines.push_back(line);
    }

    long prod = 1;

    for (int slope_idx = 0; slope_idx < 5; slope_idx++) {
        int pos = 0;
        int line_count = 0;
        int tree_count = 0;

        for (auto line :lines) {
            if (++line_count % slope_down[slope_idx] != 0) continue;

            pos = (pos + slope_right[slope_idx]) % line.length();

            if (line[pos] == '#') tree_count++;
        }

        prod *= tree_count;

        if (slope_idx == 1) cout << "Part1: " << tree_count << endl;
    }
    cout << "Part2: " << prod;

    return 0;
}