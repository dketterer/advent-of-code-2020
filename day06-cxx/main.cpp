//
// Created by daniel on 01.12.20.
//

#include <fstream>
#include <vector>
#include <iostream>
#include <algorithm>
#include <set>

using namespace std;

struct passenger_group {
    vector<set<char>> answers;

    set<char> s_intersection() {
        if (answers.size() == 1) return answers[0];
        else {
            set<char> temp_element;
            set_intersection(answers[0].begin(), answers[0].end(),
                             answers[1].begin(), answers[1].end(),
                             std::inserter(temp_element, temp_element.begin()));
            for (int i = 2; i < answers.size(); i++) {
                set<char> temp2;
                set_intersection(temp_element.begin(), temp_element.end(),
                                 answers[i].begin(), answers[i].end(),
                                 std::inserter(temp2, temp2.begin()));
                temp_element = temp2;
            }
            return temp_element;
        }
    }

    set<char> s_union() {
        set<char> temp_element;
        for(auto s : answers) {
            set_union(temp_element.begin(), temp_element.end(),
                      s.begin(), s.end(),
                      inserter(temp_element, temp_element.begin()));
        }
        return temp_element;
    }
};


int main() {
    std::ifstream infile("../input.txt");

    int part1 = 0;
    int part2 = 0;

    passenger_group group;

    std::string line;
    while (std::getline(infile, line)) {
        if (line.empty()) {
            part1 += group.s_union().size();
            part2 += group.s_intersection().size();
            group = passenger_group();
        } else {
            set<char> answers;
            for (auto c : line) {
                answers.insert(c);
            }
            group.answers.push_back(answers);
        }
    }

    part1 += group.s_union().size();
    part2 += group.s_intersection().size();

    cout << "Part 1: " << part1 << endl;
    cout << "Part 2: " << part2 << endl;

    return 0;
}