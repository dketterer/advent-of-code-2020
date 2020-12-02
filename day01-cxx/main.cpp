//
// Created by daniel on 01.12.20.
//

#include <fstream>
#include <vector>
#include <iostream>
#include <algorithm>
#include <numeric>

using namespace std;

/// Idea from https://stackoverflow.com/a/25827936
void dfs(int depth, int s, int i, std::vector<int> &c, const std::vector<int> &v, vector<vector<int>> &result) {

    if (depth == s) {
        do {
            result.push_back(c);
        } while (std::next_permutation(c.begin(), c.end()));
    } else {
        for (int j = i + 1; j < (int) v.size(); ++j) {
            c.push_back(v[j]);
            dfs(depth + 1, s, j, c, v, result);
            c.pop_back();
        }
    }
}

int main() {

    std::ifstream infile("../input.txt");

    int a;
    std::vector<int> numbers;
    while (infile >> a) {
        numbers.push_back(a);
    }

    std::sort(numbers.begin(), numbers.end());
    std::vector<int> c;
    const int length = 3;
    vector<vector<int>> combis;
    dfs(0, length, -1, c, numbers, combis);

    for (auto comb : combis) {
        if (accumulate(comb.begin(), comb.end(), 0, plus<>()) == 2020) {
            cout << accumulate(begin(comb), end(comb), 1, multiplies<>());
            break;
        }
    }

    return 0;
}