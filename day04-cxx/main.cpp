//
// Created by daniel on 01.12.20.
//

#include <fstream>
#include <vector>
#include <iostream>
#include <regex>
#include <string>

using namespace std;


int main() {

    std::ifstream infile("../input.txt");
    std::string line;
    vector<string> lines;

    std::string buffer;
    while (std::getline(infile, line)) {
        if (line.empty()) {
            lines.push_back(buffer);
            buffer = "";
        } else {
            if (!buffer.empty()) buffer.append(" ");
            buffer.append(line);
        }
    }
    int valid1 = 0;
    int valid2 = 0;
    vector<regex> patterns1 = {regex("(\\s|^)byr:\\S"), regex("(\\s|^)iyr:\\S"),
                               regex("(\\s|^)eyr:\\S"), regex("(\\s|^)hcl:\\S"),
                               regex("(\\s|^)ecl:\\S"), regex("(\\s|^)pid:\\S"),
                               regex("(\\s|^)hgt:\\S")};

    vector<regex> patterns2 = {regex("byr:(19[2-9][0-9]|200[0-2])"),
                               regex("iyr:(201[0-9]|2020)"),
                               regex("eyr:(202[0-9]|2030)"),
                               regex("hgt:((1[5-8][0-9]|19[0-3])cm|(59|6[0-9]|7[0-6])in)"),
                               regex("hcl:#[0-9a-f]{6}(?!\\w)"),
                               regex("ecl:(amb|blu|brn|gry|grn|hzl|oth)"),
                               regex("pid:[0-9]{9}(?!\\w)")
    };
    for (const auto &s : lines) {
        int matches1 = 0;
        int matches2 = 0;
        for (const auto &pattern : patterns2) {
            if (std::regex_search(s, pattern)) matches2++;
        }
        for (const auto &pattern : patterns1) {
            if (std::regex_search(s, pattern)) matches1++;
        }
        if (matches1 == patterns1.size()) valid1++;
        if (matches2 == patterns2.size()) valid2++;
    }
    cout << valid1 << endl;
    cout << valid2;
    return 0;
}