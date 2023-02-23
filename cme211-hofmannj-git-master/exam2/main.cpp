#include <vector>
#include <string>
#include <fstream>
#include <iostream>

#include "Stock.hpp"

int main(int argc, char * argv[]) {
    
    if (argc < 3) {
        std::cout << "Usage: \n ./main <input file name> <ticker name>" \
                << std::endl;
        return 0;
    }

    /* Read in command line arguments */
    std::string filename = argv[1];
    std::string stockname = argv[2];

    /* Import prices to std::vector<double> */
    std::vector<double> all_prices;
    std::ifstream f;
    f.open (filename);
    if (f.is_open()) {
        double price;
        while (f >> price) {
            all_prices.push_back(price);
        }
        f.close();
    }

    /* Call the Stock class constructor */
    Stock msft_stock(all_prices, stockname);

    /* Perform reqired calculations */
    int num_returns = (int)(all_prices.size() - 1);
    double mean_return = msft_stock.meanReturn(num_returns);
    double var_return = msft_stock.varReturn(num_returns, mean_return);

    /* Write out to results.txt */
    std::ofstream g("results.txt");
    g << stockname << std::endl;
    g << mean_return << std::endl;
    g << var_return << std::endl;
    g.close();

    return 0;
}

