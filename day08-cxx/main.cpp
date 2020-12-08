//
// Created by daniel on 01.12.20.
//

#include <fstream>
#include <vector>
#include <iostream>
#include <tuple>
#include <algorithm>
#include <regex>

using namespace std;

enum OpCode {
    nop,
    jmp,
    acc
};

class GameConsole {
public:
    int r_accumulator;

    GameConsole() : r_accumulator(0) {};

    int execute(tuple<OpCode, int> &instruction) {
        OpCode op;
        int arg;
        tie(op, arg) = instruction;
        switch (op) {
            case acc:
                r_accumulator += arg;
                return 1;
            case nop:
                return 1;
            case jmp:
                return arg;
            default:
                cout << "Problem" << endl;
                return 0;
        }
    }

    bool run_program(vector<tuple<OpCode, int>> &instructions) {
        vector<int> visited;
        int index = 0;
        while (1) {
            visited.push_back(index);
            index += execute(instructions[index]);
            if (std::count(visited.begin(), visited.end(), index)) return false;
            if (index == instructions.size()) return true;
        }

    }

    static tuple<OpCode, int> parse_program_line(string line) {
        static regex pattern("(jmp|acc|nop) \\+?(-?\\d+)", std::regex::ECMAScript);
        std::smatch match;
        std::regex_match(line, match, pattern);
        static std::unordered_map<std::string, OpCode> const table = {{"acc", OpCode::acc},
                                                                      {"nop", OpCode::nop},
                                                                      {"jmp", OpCode::jmp}};
        return make_tuple(table.find(match[1].str())->second, stoi(match[2].str()));
    }
};

int main() {
    std::ifstream infile("../input.txt");

    std::string line;
    std::vector<tuple<OpCode, int>> instructions;
    while (std::getline(infile, line)) {
        instructions.push_back(GameConsole::parse_program_line(line));
    }

    auto game_console = GameConsole();
    game_console.run_program(instructions);
    cout << "Part 1: " << game_console.r_accumulator << endl;

    for (size_t i = 0; i < instructions.size(); i++) {
        if (get<0>(instructions[i]) == nop) {
            instructions[i] = make_tuple(OpCode::jmp, get<1>(instructions[i]));
            auto console = GameConsole();
            if (console.run_program(instructions)) {
                cout << "Part 2: " << console.r_accumulator << endl;
                break;
            }
            instructions[i] = make_tuple(OpCode::nop, get<1>(instructions[i]));
        } else if (get<0>(instructions[i]) == jmp) {
            instructions[i] = make_tuple(OpCode::nop, get<1>(instructions[i]));
            auto console = GameConsole();
            if (console.run_program(instructions)) {
                cout << "Part 2: " << console.r_accumulator << endl;
                break;
            }
            instructions[i] = make_tuple(OpCode::jmp, get<1>(instructions[i]));
        }
    }
    return 0;
}
