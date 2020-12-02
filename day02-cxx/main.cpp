//
// Created by daniel on 01.12.20.
//

#include <fstream>
#include <vector>
#include <iostream>
#include <algorithm>

using namespace std;


struct LINE {
    int lower;
    int upper;
    char c;
    string pw;
} inp;

vector<string> split(string line, char delimiter) {
    vector<string> parts;
    size_t pos;
    std::string token;
    while ((pos = line.find(delimiter)) != std::string::npos) {
        token = line.substr(0, pos);
        parts.push_back(token);
        line.erase(0, pos + 1);
    }
    parts.push_back(line);
    return parts;
}


int main() {

    std::ifstream infile("../input.txt");

    bool part1 = false;

    std::vector<LINE> lines;
    std::string line;
    while (std::getline(infile, line)) {
        LINE this_line;

        // split
        auto parts = split(line, ' ');
        auto numbers = split(parts[0], '-');
        this_line.lower = stoi(numbers[0]);
        this_line.upper = stoi(numbers[1]);
        this_line.c = parts[1][0];
        this_line.pw = parts[2];
        lines.push_back(this_line);
    }
    int valids = 0;

    for (auto this_line : lines) {
        if (part1) {
            auto count = std::count(this_line.pw.begin(), this_line.pw.end(), this_line.c);
            if (this_line.lower <= count and count <= this_line.upper)
                valids++;

        } else {
            if (this_line.pw[this_line.lower - 1] == this_line.c xor this_line.pw[this_line.upper - 1] == this_line.c)
                valids++;
        }
    }

    cout << valids;

    return 0;
}