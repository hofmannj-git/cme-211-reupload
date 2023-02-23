#ifndef IMAGE_HPP
#define IMAGE_HPP

#include <boost/multi_array.hpp>
#include "hw6.hpp"
#include <string>

class Image {
  public:
    std::string jpegname;
    std::string jpegtowrite;
    boost::multi_array<unsigned char, 2> imagedata{boost::extents[1][1]};
    Image(std::string jpegname);
    void Save(std::string jpegtowrite);
    void ConvMult(unsigned int i, unsigned int j,
                  boost::multi_array<unsigned char,2>& input,
                  boost::multi_array<unsigned char,2>& output,
                  boost::multi_array<float,2>& kernel);
    void ExtendConvMult(unsigned int i, unsigned int j,
                        boost::multi_array<unsigned char,2>& input,
                        boost::multi_array<unsigned char,2>& output,
                        boost::multi_array<float,2>& kernel);
    void Convolution(boost::multi_array<unsigned char,2>& input,
                     boost::multi_array<unsigned char,2>& output,
                     boost::multi_array<float,2>& kernel);
    void BoxBlur(unsigned int kernelsize);
    unsigned int Sharpness(void);
};

#endif /* IMAGE_HPP */
