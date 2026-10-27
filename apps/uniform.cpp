#include <iostream>
#include <random>
#include <vector>
#include <string>
#include <cstdint>
#include <cstdlib>
#include <filesystem>

#include "binaryFiles.hpp"

int main(int argc, char* argv[]) {
    /* ----- cmd line args ----- */
    if (argc != 5) {
        std::cerr << "Usage: " << argv[0]
                  << " <no_channels> <mean> <no_spectra> <output_dir>" << std::endl;
        return 1;
    }

    const int no_channels = std::atoi(argv[1]);
    const int mean = std::atoi(argv[2]);
    const int no_spectra = std::atoi(argv[3]);
    const std::filesystem::path out_dir = argv[4];

    if (no_channels <= 0 || mean <= 0 || no_spectra <= 0) {
        std::cerr << "Error: no_channels, mean and no_spectra must be positive integers." << std::endl;
        return 1;
    }

    std::filesystem::create_directories(out_dir); // Create output directory if it doesn't exist
    const long long entries = static_cast<long long>(no_channels) * mean; // Total number of entries to distribute across channels

    // Random number generation setup
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dist(0, no_channels - 1);

    std::vector<uint32_t> spectrum(no_channels);

    // Generate and write spectra to binary files
    for (int i = 0; i < no_spectra; i++) {
        std::fill(spectrum.begin(), spectrum.end(), 0u); // Reset the spectrum for each iteration

        for (long long j = 0; j < entries; j++) {
            spectrum[dist(gen)]++;
        }

        std::string filename = (out_dir / ("spectrum" + std::to_string(i) + ".bin")).string();
        if (!fileWriteBinary(spectrum, filename)) return 1;
    }

    std::cout << "Done: " << no_spectra << " spectra written in '" << out_dir.string() << "'." << std::endl;
    return 0;
}