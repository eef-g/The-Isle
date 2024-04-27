from reader import WADReader


class WADData:
    LUMP_INDICIES = {
        'THINGS': 1, 'LINEDEFS': 2, 'SIDEDEFS': 3, 'VERTEXES': 4, 'SEGS': 5,
        'SSECTORS': 6, 'NODES': 7, 'SECTORS': 8, 'REJECT': 9, 'BLOCKMAP': 10
    }

    def __init__(self, engine, map_name):
        self.reader = WADReader(engine.wad_path)
        self.map_index = self.get_lump_index(lump_name=map_name)
        self.vertexes = self.get_lump_data(
            reader_func=self.reader.read_vertex,
            lump_index=self.map_index + self.LUMP_INDICIES['VERTEXES'],
            num_bytes=4  # Number of bytes in a vertex
        )
        self.linedefs = self.get_lump_data(
            reader_func=self.reader.read_linedef,
            lump_index=self.map_index + self.LUMP_INDICIES['LINEDEFS'],
            num_bytes=14
        )
        self.nodes = self.get_lump_data(
            reader_func=self.reader.read_node,
            lump_index=self.map_index + self.LUMP_INDICIES['NODES'],
            num_bytes=28
        )
        self.sub_sectors = self.get_lump_data(
            reader_func=self.reader.read_sub_sector,
            lump_index=self.map_index + self.LUMP_INDICIES['SSECTORS'],
            num_bytes=4
        )
        self.segments = self.get_lump_data(
            reader_func=self.reader.read_segment,
            lump_index=self.map_index + self.LUMP_INDICIES['SEGS'],
            num_bytes=12
        )
        self.things = self.get_lump_data(
            reader_func=self.reader.read_thing,
            lump_index=self.map_index + self.LUMP_INDICIES['THINGS'],
            num_bytes=10
        )
        
        self.update_data()
        self.reader.close()


    def update_data(self):
        self.update_segs()

    def update_segs(self):
        for seg in self.segments:
            seg.start_vertex = self.vertexes[seg.start_vertex_id]
            seg.end_vertex = self.vertexes[seg.end_vertex_id]
            seg.linedef = self.linedefs[seg.linedef_id]

            # Convert angles from binary to degrees
            seg.angle = (seg.angle << 16) * 8.38190317e-8
            seg.angle = seg.angle + 360 if seg.angle < 0 else seg.angle

    def get_lump_data(self, reader_func, lump_index,
                      num_bytes, header_length=0):
        lump_info = self.reader.directory[lump_index]
        count = lump_info['lump_size'] // num_bytes
        data = []
        for i in range(count):
            offset = lump_info['lump_offset'] + i * num_bytes + header_length
            data.append(reader_func(offset))
        return data

    def get_lump_index(self, lump_name) -> int:
        for index, lump_info in enumerate(self.reader.directory):
            if lump_name in lump_info.values():
                return index
        return -1
