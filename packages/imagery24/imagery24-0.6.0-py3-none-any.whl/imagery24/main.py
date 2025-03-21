from pathlib import Path
from tempfile import TemporaryDirectory
from typing import BinaryIO

from imagery24.extract import extract_webp_images
from imagery24.georeference import get_gcps
from imagery24.tags import get_metadata
from imagery24.tiff import create_tiff
from imagery24.tiles import get_tiles


def get_levels_bounds(
    metadata: list[dict[bytes, int | str]],
) -> list[tuple[int, int, int, int]]:
    TILE_GRID_TAG = b"PGD_CB"
    layers = []

    for level_metadata in metadata:
        if TILE_GRID_TAG in level_metadata:
            grid_str = str(level_metadata[TILE_GRID_TAG])
            x_min, y_min, x_max, y_max = map(int, grid_str.split(","))
            layers.append((x_min, y_min, x_max, y_max))

    return layers


def convert(input_file: Path | str, output_file: Path | str):
    input_file = Path(input_file)
    output_file = Path(output_file)

    assert input_file.exists(), f"File not found: {input_file}"
    output_dir = output_file.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(input_file, "rb") as input_io:
        geotiff_buffer = convert_io(input_io)

        with open(output_file, "wb") as output_io:
            output_io.write(geotiff_buffer.read())

            print(f"GeoTIFF saved to {output_file}")


def convert_io(input_io: BinaryIO) -> BinaryIO:
    metadata = get_metadata(input_io)
    levels_bounds = get_levels_bounds(metadata)
    tiles = list(get_tiles(levels_bounds))

    with TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        extract_webp_images(input_io, tiles, temp_dir_path)
        max_zoom = len(levels_bounds) - 1

        width = int(metadata[0][b"image_width_px"])
        height = int(metadata[0][b"image_height_px"])
        corner_coords_str = str(metadata[max_zoom][b"PGD_CO"])
        corner_coords = [
            tuple(map(float, coord.split(",")))
            for coord in corner_coords_str.split(" ")
        ]
        corner_coords = corner_coords[:4]
        gcps = get_gcps(corner_coords, width, height)

        return create_tiff(temp_dir_path, levels_bounds, max_zoom, width, height, gcps)
