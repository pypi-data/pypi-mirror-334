import tifffile
from cellstitch_cuda.pipeline import cellstitch_cuda, correction
# from cellstitch_cuda.interpolate import full_interpolate

img = r"E:\1_DATA\Rheenen\tvl_jr\SP8\2025Mar6_2516017_DiLiCre-4mg-2d_2W_Ileum\2025Mar6_2516017_DiLiCre-4mg-2d_2W_Ileum-1\output.tif"

cellstitch_cuda(
    img,
    output_masks=True,
    verbose=True,
    seg_mode="nuclei_cells",
    interpolation=False,
    n_jobs=-1,
)
#
# masks = tifffile.imread(r"E:\1_DATA\Rheenen\tvl_jr\SP8\2025Feb19_Ileum_8d_fresh_3D\2025Feb19_Ileum_8d_fresh_3D-1\cellstitch_masks.tif")
#
# masks = correction(masks)

# masks = full_interpolate(masks, anisotropy=8, n_jobs=-1, verbose=True)

# tifffile.imwrite(r"E:\1_DATA\Rheenen\tvl_jr\SP8\2025Feb19_Ileum_8d_fresh_3D\2025Feb19_Ileum_8d_fresh_3D-1\cellstitch_masks_split.tif", masks)
