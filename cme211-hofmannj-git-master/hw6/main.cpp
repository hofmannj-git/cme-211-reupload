#include <boost/multi_array.hpp>
#include <fstream>
#include "hw6.hpp"
#include "image.hpp"
#include <iostream>
#include <iomanip>
#include <string>

int main(){
    
    std::string imagename_input = "stanford.jpg";
    Image im(imagename_input);
    
    unsigned int sharp_init = im.Sharpness(); // calculates initial sharpness
    
    // unsigned int kernelsizes[7] = {3, 7, 11, 15, 19, 23, 27};
    unsigned int sharpnesses[7];
    for (unsigned int i = 0; i < 7; i++) {
        std::string imagename_new;
        if (i < 10) {
            imagename_new = "BoxBlur0" + std::to_string(i) + ".jpg";
        }
        else {
            imagename_new = "BoxBlur" + std::to_string(i) + ".jpg";
        }
        Image new_im(imagename_input); // instantiates new image
        new_im.BoxBlur(i); // blurs image according to kernel size
        sharpnesses[i] = new_im.Sharpness(); // calculates & stores sharpness
        new_im.Save(imagename_new);
    }
    
    std::cout << "$ ./main Original image: " << sharp_init << " BoxBlur( 3): " \
        << sharpnesses[0] << " BoxBlur( 7): " << sharpnesses[1] << \
        " BoxBlur(11): " << sharpnesses[2] << " BoxBlur(15): " << \
        sharpnesses[3] << " BoxBlur(19): " << sharpnesses[4] << \
        " BoxBlur(23): " << sharpnesses[5] << " BoxBlur(27): " << \
        sharpnesses[6] << std::endl;
}

