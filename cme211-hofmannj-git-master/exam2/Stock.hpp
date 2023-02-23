#ifndef STOCK_HPP
#define STOCK_HPP

#include <iostream>
#include <string>
#include <vector>

class Stock {
    private:

        /* private member variables */
        std::vector<double> dr;
        std::vector<double> price_vec;
        std::string tckr;
    
        //calculate daily return
        std::vector<double> dailyReturn(int num_returns);

    public:

        /* public member variables */

        //constructor
        Stock( std::vector<double> price_vec, std::string tckr);

        //calculate mean return 
        double meanReturn( int num_returns );
        
        //calcualte return variance
        double varReturn( int num_returns, double meandr );
        
        /* add additional methods as needed */        
};

#endif /* STOCK_HPP */
