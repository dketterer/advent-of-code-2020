//
// Created by daniel on 01.12.20.
//

#include <fstream>
#include <vector>
#include <iostream>
#include <regex>
#include <set>

using namespace std;


struct Bag {
    string color;
    vector<reference_wrapper<Bag>> parents;
    vector<tuple<int, reference_wrapper<Bag>>> childs;

    Bag() {}

    Bag(string col) : parents(vector<reference_wrapper<Bag>>()), childs(vector<tuple<int, reference_wrapper<Bag>>>()) {
        color = col;
    }

    Bag(string col, Bag &bag) : childs(vector<tuple<int, reference_wrapper<Bag>>>()) {
        color = col;
        parents = {bag};
    }
};

void traverse_back(Bag &bag, set<string> &uniques) {
    uniques.insert(bag.color);
    for (auto &parent_bag : bag.parents) {
        traverse_back(parent_bag, uniques);
    }
}

int traverse_forward(Bag &bag, int this_weight) {
    int s(0);
    for (auto[weight, child_bag] : bag.childs) {
        s += this_weight * weight;
        s += traverse_forward(child_bag, this_weight * weight);
    }
    return s;
}


int main() {
    std::ifstream infile("../input.txt");

    std::map<string, Bag> bags;

    regex pattern1 = regex("(\\w+ \\w+) bags contain.*", std::regex::ECMAScript);
    regex pattern2 = regex("(\\d+) (\\w+ \\w+) bags?", std::regex::ECMAScript);

    std::string line;
    while (std::getline(infile, line)) {
        std::smatch base_match;
        std::regex_match(line, base_match, pattern1);
        string parent_name = base_match[1].str();

        if (!bags.count(parent_name)) {
            bags[parent_name] = Bag(parent_name);
        }

        for (auto i = std::sregex_iterator(line.begin(), line.end(), pattern2); i != sregex_iterator(); ++i) {
            std::smatch m = *i;
            int num = stoi(m[1]);
            string color = m[2];
            if (!bags.count(color)) {
                bags[color] = Bag(color, bags[parent_name]);
            } else {
                bags[color].parents.push_back(bags[parent_name]);
            }
            bags[parent_name].childs.push_back({num, bags[color]});
        }
    }
    set<string> uniques;
    traverse_back(bags["shiny gold"], uniques);
    cout << "Part 1: " << uniques.size() - 1 << endl;
    cout << "Part 2: " << traverse_forward(bags["shiny gold"], 1) << endl;

    return 0;
}