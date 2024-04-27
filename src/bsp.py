from settings import *
import math
from pygame.math import Vector2 as vec2

class BSP:
    SUB_SECTOR_IDENTIFIER = 0x8000  # 2^15 = 32768

    def __init__(self, engine):
        self.engine = engine
        self.player = engine.player
        self.nodes = engine.wad_data.nodes
        self.sub_sectors = engine.wad_data.sub_sectors
        self.segs = engine.wad_data.segments
        self.root_node_id = len(self.nodes) - 1

    def update(self):
        self.render_bsp_node(node_id=self.root_node_id)

    @staticmethod
    def angle_to_x(angle):
        if angle > 0:
            x = SCREEN_DIST - math.tan(math.radians(angle)) * H_WIDTH
        else:
            x = -math.tan(math.radians(angle)) * H_WIDTH + SCREEN_DIST
        return int(x)

    def add_segment_to_fov(self, vertex1, vertex2):
        angle1 = self.point_to_angle(vertex1)
        angle2 = self.point_to_angle(vertex2)

        span = self.norm(angle1 - angle2)
        # Backface culling
        if span >= 180.0:
            return False

        rw_angle1 = angle1

        angle1 -= self.player.angle
        angle2 -= self.player.angle

        span1 = self.norm(angle1 + H_FOV)
        if span1 > FOV:
            if span1 >= span + FOV:
                return False
            # Clip the segment to only within FOV
            angle1 = H_FOV

        span2 = self.norm(H_FOV - angle2)
        if span2 > FOV:
            if span2 >= span + FOV:
                return False
            # Clip the segment to only within FOV
            angle2 = -H_FOV

        x1 = self.angle_to_x(angle1)
        x2 = self.angle_to_x(angle2)
        return x1, x2, rw_angle1

    def render_sub_sector(self, sub_sector_id):
        sub_sector = self.sub_sectors[sub_sector_id]
        for i in range(sub_sector.seg_count):
            seg = self.segs[sub_sector.first_seg_id + i]
            if self.add_segment_to_fov(seg.start_vertex, seg.end_vertex):
                self.engine.map_renderer.draw_seg(seg)

    @staticmethod
    def norm(angle):
        angle %= 360
        return angle + 360 if angle < 0 else angle

    def check_bbox(self, bbox):
        a, b = vec2(bbox.left, bbox.bottom), vec2(bbox.left, bbox.top)
        c, d = vec2(bbox.right, bbox.top), vec2(bbox.right, bbox.bottom)

        px, py = self.player.pos
        if px < bbox.left:
            if py > bbox.top:
                bbox_sides = (b, a), (c, b)
            elif py < bbox.bottom:
                bbox_sides = (b, a), (a, d)
            else:
                bbox_sides = (b, a),
        elif px > bbox.right:
            if py > bbox.top:
                bbox_sides = (c, b), (d, c)
            elif py < bbox.bottom:
                bbox_sides = (a, d), (d, c)
            else:
                bbox_sides = (d, c), 
        else:
            if py > bbox.top:
                bbox_sides = (c, b), 
            elif py < bbox.bottom:
                bbox_sides = (a, d), 
            else:
                return True
        
        for v1, v2 in bbox_sides:
            angle1 = self.point_to_angle(v1)
            angle2 = self.point_to_angle(v2)

            span = self.norm(angle1 - angle2)
            
            angle1 -= self.player.angle
            span1 = self.norm(angle1 + H_FOV)
            if span1 > FOV:
                if span1 >= span + FOV:
                    continue
            return True
        return False

    def point_to_angle(self, vertex):
        delta = vertex - self.player.pos
        return math.degrees(math.atan2(delta.y, delta.x))

    def render_bsp_node(self, node_id):
        if node_id >= self.SUB_SECTOR_IDENTIFIER:
            sub_sector_id = node_id - self.SUB_SECTOR_IDENTIFIER
            self.render_sub_sector(sub_sector_id)
            return None
        node = self.nodes[node_id]

        is_on_back = self.is_on_back_side(node)
        if is_on_back:
            self.render_bsp_node(node.back_child_id)
            if self.check_bbox(node.bbox['front']):
                self.render_bsp_node(node.front_child_id)
        else:
            self.render_bsp_node(node.front_child_id)
            if self.check_bbox(node.bbox['back']):
                self.render_bsp_node(node.back_child_id)

    def is_on_back_side(self, node):
        dx = self.player.pos.x - node.x_partition
        dy = self.player.pos.y - node.y_partition
        return dx * node.dy_partition - dy * node.dx_partition <= 0
