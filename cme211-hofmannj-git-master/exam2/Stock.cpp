#include <iostream>
#include <vector>
#include "Stock.hpp"
#include <string>

Stock::Stock(std::vector<double> price_vec, std::string tckr) {
    this->price_vec = price_vec;
    this->tckr = tckr;
    //int num_returns = (int)(price_vec.size() - 1);
    //std::vector<double> dr = dailyReturn();
}

std::vector<double> Stock::dailyReturn(int num_returns){
    std::vector<double> dailret;
    for (int k = 0; k < num_returns; k++) {
        double rt = (price_vec[k+1]-price_vec[k])/price_vec[k];
        dailret.push_back(rt);
    }
    return dailret;
}

double Stock::meanReturn(int num_returns){
    std::vector<double> dr = dailyReturn(num_returns);
    double mdr = 0;
    for (int i = 0; i < num_returns; i++) {
        mdr += dr[i];
    }
    mdr = mdr / num_returns;
    return mdr;
}

double Stock::varReturn(int num_returns, double meandr){
    std::vector<double> dr = dailyReturn(num_returns);
    double vor = 0;
    for (int j = 0; j < num_returns; j++) {
        vor += (dr[j] - meandr)*(dr[j] - meandr);
    }
    vor = vor / (num_returns-1);
    return vor;
}
