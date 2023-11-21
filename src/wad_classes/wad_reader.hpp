#ifndef WAD_READER_HPP
#define WAD_READER_HPP

#include <fstream>
#include <vector>
#include <string>
#include <iostream>
#include <raylib-cpp.hpp>

struct WADHeader {
    std::string wad_type;
    int lump_count;
    int init_offset;
};

struct WADLump {
    int lump_pos;
    int lump_size;
    std::string lump_name;
};

struct WADDir {
    std::vector<WADLump> lumps;
};

struct LINEDEF {
    int16_t start_vertex;
    int16_t end_vertex;
    int16_t flags;
    int16_t special_type;
    int16_t sector_tag;
    int16_t front_sidedef;
    int16_t back_sidedef;
};


class WADReader {
private:
    std::string wad_path;
    std::vector<char> buffer;

    WADHeader ReadHeader();
    WADDir ReadDir();

public:
    WADHeader header;
    WADDir dir;
    WADReader() {};
    WADReader(std::string wad_path);
    
    int32_t BytesToInt(std::vector<unsigned char> bytes);
    Vector2 ReadVertex(int offset);
    LINEDEF ReadLinedef(int offset);
    std::vector<unsigned char> ReadBytes(int offset, int num_bytes);
};
#endif