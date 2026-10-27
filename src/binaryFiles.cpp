#include "binaryFiles.hpp"

#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdint>

bool fileWriteBinary(const std::vector<uint32_t>& y_data, const std::string& filename) {
    std::ofstream outFile(filename, std::ios::binary);
    if (!outFile) {
        std::cerr << "Error: impossible to create or open '" << filename << "'!" << std::endl;
        return false;
    }
    outFile.write(reinterpret_cast<const char*>(y_data.data()),
                  static_cast<std::streamsize>(y_data.size() * sizeof(uint32_t)));
    return outFile.good();
}