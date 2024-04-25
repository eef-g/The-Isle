# H - uint16, h - int16, I - uint32, i - int32, c - char


class Linedef:
    # 14 bytes - 2H x 7
    __slots__ = [
        'start_vertex_id',
        'end_vertex_id',
        'flags',
        'line_type',
        'sector_tag',
        'front_sidedef_id',
        'back_sidedef_id'
    ]
