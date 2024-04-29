import pygame as pg
from pygame import color
from settings import *

class Patch:
    def __init__(self, asset_data, name, is_sprite=True):
        self.asset_data = asset_data
        self.name = name

        self.palette = asset_data.palette
        self.header, self.patch_columns = self.load_patch_columns(name)
        self.width = self.header.width
        self.height = self.header.height

        self.image = self.get_image()
        if is_sprite:
            self.image = pg.transform.scale(self.image, (
                self.width * SCALE, self.height * SCALE)
            )

    def load_patch_columns(self, patch_name):
        reader = self.asset_data.reader
        patch_index = self.asset_data.get_lump_index(patch_name)
        patch_offset = reader.directory[patch_index]['lump_offset']

        patch_header = self.asset_data.reader.read_patch_header(patch_offset)
        patch_columns = []

        for i in range(patch_header.width):
            offs = patch_offset + patch_header.column_offset[i]
            while True:
                patch_column, offs = reader.read_patch_column(offs)
                patch_columns.append(patch_column)
                if patch_column.top_delta == 0xFF:
                    break
        return patch_header, patch_columns

    def get_image(self):
        image = pg.Surface([self.width, self.height])
        image.fill(COLOR_KEY)
        image.set_colorkey(COLOR_KEY)

        ix = 0
        for column in self.patch_columns:
            if column.top_delta == 0xFF:
                ix += 1
                continue

            for iy in range(column.length):
                color_idx = column.data[iy]
                color = self.palette[color_idx]
                image.set_at([ix, iy + column.top_delta], color)
        return image

class AssetData:
    def __init__(self, wad_data) -> None:
        self.wad_data = wad_data
        self.reader = wad_data.reader
        self.get_lump_index = wad_data.get_lump_index

        # Palettes
        self.palettes = self.wad_data.get_lump_data(
            reader_func=self.reader.read_palette,
            lump_index=self.get_lump_index('PLAYPAL'),
            num_bytes=256 * 3
        )
        # Current Palette
        self.palette_idx = 0
        self.palette = self.palettes[self.palette_idx]
        
        # Sprites
        self.sprites = self.get_sprites()

        # Textures Patches
        self.p_names = self.wad_data.get_lump_data(
            self.reader.read_string,
            self.get_lump_index('PNAMES'),
            num_bytes=8,
            header_length=4
        )
        self.texture_patches = [
            Patch(self, p_name, is_sprite=False) for p_name in self.p_names
        ]

    def get_sprites(self, start_marker='S_START', end_marker='S_END'):
        idx1 = self.get_lump_index(start_marker) + 1
        idx2 = self.get_lump_index(end_marker)
        lumps_info = self.reader.directory[idx1: idx2]
        sprites = {
            lump['lump_name']: Patch(self, lump['lump_name']).image for lump in lumps_info
        }
        return sprites
