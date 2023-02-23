#include <boost/multi_array.hpp>
#include <cmath>
#include "hw6.hpp"
#include "image.hpp"
#include <iostream>
#include <string>

Image::Image(std::string jpegname) {
    this->jpegname = jpegname;
    //imagedata[1][1] = (unsigned char)1;
    ReadGrayscaleJPEG(jpegname, imagedata);
}

void Image::Save(std::string jpegtowrite) {
    std::string jpeg;
    if (jpegtowrite.empty()){
        jpeg = jpegtowrite;
    }
    else{
        jpeg = jpegname;
    }
    WriteGrayscaleJPEG(jpeg, imagedata);
}

void Image::ConvMult(unsigned int i, unsigned int j,
              boost::multi_array<unsigned char,2>& input,
              boost::multi_array<unsigned char,2>& output,
              boost::multi_array<float,2>& kernel){
    // multiply each value in kxk block around input (i,j) by each value in
    // kernel, and sum -- then change value in output (i,j) to this value
    float sum_out = 0;
    unsigned int kernel_shape = (unsigned int)kernel.shape()[0];
    unsigned int ksmin1div2 = (kernel_shape - 1)/2;
    unsigned int count_row = 0;
    unsigned int count_col = 0;
    for (unsigned int k = (i - ksmin1div2); k < (i + ksmin1div2); k++) {
        for (unsigned int l = (j - ksmin1div2); l < (j + ksmin1div2); l++) {
            sum_out += input[k][l] * kernel[count_row][count_col];
            count_col++; // col index is l
        }
        count_col = 0;
        count_row++; // row index is k
    }
    output[i][j] = (unsigned char)sum_out;
    
}

void Image::ExtendConvMult(unsigned int i, unsigned int j,
                    boost::multi_array<unsigned char,2>& input,
                    boost::multi_array<unsigned char,2>& output,
                    boost::multi_array<float,2>& kernel){
    // create kxk block around input (i,j) extending past bounds of input, then:
    // multiply each value in kxk block around input (i,j) by each value in
    // kernel, and sum -- then change value in output (i,j) to this value
    enum direction{
        NW_corn,
        NE_corn,
        SW_corn,
        SE_corn,
        North,
        South,
        East,
        West
    };
    direction d = North; // initializing the enumerator
    unsigned int km1d2 = (unsigned int)(kernel.shape()[0] - 1)/2;
    unsigned int dmk = (unsigned int)(input.shape()[0] - 1 - km1d2);
    unsigned int finind = (unsigned int)(input.shape()[0] - 1);
    if (j < km1d2){ // NEEDS TO EXTEND NORTH (or NW or NE)
        if (i > dmk){ // check for NE
            d = NE_corn;
        }
        else if (i < km1d2){ // check for NW
            d = NW_corn;
        }
        else { // goes north
            d = North;
        }
    }
    else if (j > dmk){ // NEEDS TO EXTEND SOUTH (or SW or SE)
        if (i > dmk){ // check for SE
            d = SE_corn;
        }
        else if (i < km1d2){ // check for SW
            d = SW_corn;
        }
        else { // goes south
            d = South;
        }
    }
    else if (i > dmk) { // NEEDS TO EXTEND EAST
        d = East;
    }
    else if (i < km1d2){ // NEEDS TO EXTEND WEST
        d = West;
    }
    
    unsigned int k_shape = (unsigned int)kernel.shape()[0];
    boost::multi_array<unsigned char,2> tempm(boost::extents[k_shape][k_shape]);
    
    // switch to make the extended temporary matrix
    switch(d){
        case NE_corn:
            for (unsigned int k = 0; k < k_shape; k++){
                for (unsigned int m = 0; m < k_shape; m++){
                    tempm[k][m] = input[i][j];
                }
            }
            
            //            // copy existing part of matrix
            //            for (unsigned int k = 0; k < (i + km1d2); k++) {
            //                for (unsigned int l = (j - km1d2); l < finind; l++) {
            //                    tempm[km1d2-i+k][l-j+km1d2] = input[k][l];
            //                }
            //            }
            //            // extend boundaries
            //            for (unsigned int m = (j - km1d2); m < finind; m++){
            //                for (unsigned int n = 0; n < (km1d2-i-1); n++){
            //                    tempm[m-j+km1d2][n] = input[0][m];
            //                }
            //                for (unsigned int o = 0; o < (i+km1d2); o++){
            //                    tempm[m-j+km1d2][] = input[o][finind];
            //                }
            //            }
            break;
        case NW_corn:
            for (unsigned int k = 0; k < k_shape; k++){
                for (unsigned int m = 0; m < k_shape; m++){
                    tempm[k][m] = input[i][j];
                }
            }
            break;
        case SE_corn:
            for (unsigned int k = 0; k < k_shape; k++){
                for (unsigned int m = 0; m < k_shape; m++){
                    tempm[k][m] = input[i][j];
                }
            }
            break;
        case SW_corn:
            for (unsigned int k = 0; k < k_shape; k++){
                for (unsigned int m = 0; m < k_shape; m++){
                    tempm[k][m] = input[i][j];
                }
            }
            break;
        case North:
            // copy existing part of matrix
            for (unsigned int k = 0; k < (i + km1d2); k++) {
                for (unsigned int l = (j - km1d2); l < (j + km1d2); l++) {
                    tempm[km1d2-i+k][l-j+km1d2] = input[k][l];
                }
            }
            // extend boundaries
            for (unsigned int m = (j - km1d2); m < (j + km1d2); m++){
                for (unsigned int n = 0; n < (km1d2-i-1); n++){
                    tempm[n][m-j+km1d2] = input[0][m];
                }
            }
            break;
        case South:
            // copy existing part of matrix
            for (unsigned int k = (i-km1d2); k < finind; k++) {
                for (unsigned int l = (j - km1d2); l < (j + km1d2); l++) {
                    tempm[k-finind-km1d2][l-j+km1d2] = input[k][l];
                }
            }
            // extend boundaries
            for (unsigned int m = (j - km1d2); m < (j + km1d2); m++){
                for (unsigned int n=(k_shape-1-km1d2-finind+i); n<(k_shape-1); n++){
                    tempm[n][m-j+km1d2] = input[finind][m];
                }
            }
            break;
        case East:
            // copy existing part of matrix
            for (unsigned int k = 0; k < (j + km1d2); k++) { //col
                for (unsigned int l = (i - km1d2); l < (i + km1d2); l++) { //row
                    tempm[l][km1d2-j+k] = input[l][k];
                }
            }
            // extend boundaries
            for (unsigned int m = (i - km1d2); m < (i + km1d2); m++){ //row
                for (unsigned int n = 0; n < (km1d2-j-1); n++){ //col
                    tempm[m-i+km1d2][n] = input[m][0];
                }
            }
            break;
        case West:
            // copy existing part of matrix
            for (unsigned int k = (j-km1d2); k < finind; k++) { //col
                for (unsigned int l = (i - km1d2); l < (i + km1d2); l++) { //row
                    tempm[l-i+km1d2][k-finind-km1d2] = input[l][k];
                }
            }
            // extend boundaries
            for (unsigned int m = (i - km1d2); m < (i + km1d2); m++){ //row
                for (unsigned int n=(k_shape-1-km1d2-finind+j); n<(k_shape-1); n++){
                    tempm[m-i+km1d2][n] = input[m][finind];
                }
            }
            break;
    }
    
    // convolution of the extended matrix with the kernel
    float sum_out = 0;
    for (unsigned int k = 0; k < k_shape; k++) {
        for (unsigned int l = 0; l < k_shape; l++) {
            sum_out += tempm[k][l] * kernel[k][l];
        }
    }
    unsigned char sum_tot = static_cast<unsigned char>(sum_out);
    //std::cout << sum_out << std::endl;
    output[i][j] = sum_tot;
    //output[i][j] = (unsigned char)1;
    // static_cast<unsigned char>
    // (unsigned char)
}


void Image::Convolution(boost::multi_array<unsigned char,2>& input,
                 boost::multi_array<unsigned char,2>& output,
                 boost::multi_array<float,2>& kernel){
    //std::cout << output.shape()[0] << std::endl;
    //std::cout << output.shape()[1] << std::endl;
    if (input.shape()[0] != output.shape()[0]) {
        std::cout << "Input & output arrays are different sizes." << std::endl;
        exit(1);
    }
    else if (kernel.shape()[0] % 2 == 0) {
        std::cout << "Kernel size is not odd." << std::endl;
        exit(1);
    }
    else if (kernel.shape()[0] != kernel.shape()[1]) {
        std::cout << "Kernel is not square." << std::endl;
        exit(1);
    }
    else if (kernel.shape()[0] < 3) {
        std::cout << "Kernel is not at least of size 3." << std::endl;
        exit(1);
    }
    unsigned int km1d2 = (unsigned int)((kernel.shape()[0] - 1)/2);
    unsigned int dmk = (unsigned int)(input.shape()[0] - 1 - km1d2);
    // loop over all values in input image
    for (unsigned int i = 0; i < input.shape()[0]; i++) {
        for (unsigned int j = 0; j < input.shape()[1]; j++) {
            if ((i >= km1d2) and (i <= dmk) and (j >= km1d2) and (j <= dmk)) {
                // if pixel values DO NOT need to be extended, calculate convol.
                ConvMult(i, j, input, output, kernel);
            }
            else {  // if pixel values DO need to be extended
                ExtendConvMult(i, j, input, output, kernel);
            }
        }
    }
    
}

void Image::BoxBlur(unsigned int kernelsize) {
    // creates (kernelsize x kernelsize) of 1s multiplied by 1/(kernelsize)^2
    boost::multi_array<float,2> kernel(boost::extents[kernelsize][kernelsize]);
    for (unsigned int i = 0; i < kernelsize; i++) {
        for (unsigned int j = 0; j < kernelsize; j++) {
            kernel[i][j] = float(1/pow(float(kernelsize), 2.0));
        }
    }
    unsigned int s = (unsigned int)imagedata.shape()[0];
    boost::multi_array<unsigned char,2> output(boost::extents[s][s]);
    
    // uses Convolution() to smooth image
    Convolution(imagedata, output, kernel);
    imagedata = output;
}

unsigned int Image::Sharpness(void) {
    // create Laplacian kernel
    boost::multi_array<float,2> kernel(boost::extents[3][3]);
    kernel[0][0] = 0.0;
    kernel[0][1] = 1.0;
    kernel[0][2] = 0.0;
    kernel[1][0] = 1.0;
    kernel[1][1] = -4.0;
    kernel[1][2] = 1.0;
    kernel[2][0] = 0.0;
    kernel[2][1] = 1.0;
    kernel[2][2] = 0.0;
    
    unsigned int s = (unsigned int)imagedata.shape()[0];
    boost::multi_array<unsigned char,2> output(boost::extents[s][s]);
    
    // use Colvolution() on kernel and image data
    Convolution(imagedata, output, kernel);
    
    // return the maximum of the output array as the sharpness value
    // referenced: https://stackoverflow.com/questions/17207777/how-to-get-max-min-element-from-a-boost-multiarray
    unsigned int maxval = static_cast<unsigned
                            int>(*std::max_element(output.origin(),
                                                   output.origin() +
                                                   output.num_elements()));
    return maxval;
}
