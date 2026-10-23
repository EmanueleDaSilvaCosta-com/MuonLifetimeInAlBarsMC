#include <iostream>
#include <random>
#include <array>
#include <fstream>
#include <string>

const int no_channels = 2048;
int mean = 1000;
int entries = no_channels * mean;

void fileWriteHist(const auto& x_data, const auto& y_data, const std::string& filename);

int main(void){	
	
	std::string filename_base = "uniform_spectra/spectrum";
	std::string extension = ".dat";

    std::random_device rd;
    std::mt19937 gen(rd());
	std::uniform_int_distribution<int> dist(0, no_channels - 1);
	
	std::array<double, no_channels> bins{};
    std::array<int, no_channels> uniform_spectrum{};
	
	for(int i=0; i<no_channels; i++){
        bins[i] = i + 0.5;
    }

	for(int i=0; i<1000; i++){
		std::string intStr = std::to_string(i);
		std::string filename = filename_base + intStr + extension;

		for(int j=0; j<entries; j++){
        	int x = dist(gen);
        	uniform_spectrum[x]++;
    	}

		fileWriteHist(bins, uniform_spectrum, filename);
	}

    

}

void fileWriteHist(const auto& x_data, const auto& y_data, const std::string& filename) {
    if(x_data.size() != y_data.size()){
        std::cerr << "Error: x_data and y_data must be the same size!" << std::endl;
        return;
    }
    
    std::ofstream outFile(filename);
    
    if (outFile.is_open()) {
        for (size_t i = 0; i < x_data.size(); i++) {
            outFile << x_data[i] << "\t" << y_data[i] << "\n";
        }
        
        outFile.close();
        std::cout << "Data saved in file '" << filename << "'." << std::endl;
    } else {
        std::cerr << "Error: impossible to create or open the file!" << std::endl;
    }
}