import tifffile
import os
from cellpose.utils import stitch3D
from cellstitch_cuda.pipeline import full_stitch
from cellstitch_cuda.interpolate import full_interpolate


stitch_method = "cellstitch"  # "iou" or "cellstitch"
file_path_yx_masks = r"E:\1_DATA\Rheenen\tvl_jr\SP8\2024Nov22_SI_1mg_1year_3D_2D-merge\Villus_crops\2024Nov22_SI_1mg_1year_3D_2D-merge-1-2\yx_masks.tif"
file_path_yz_masks = r"E:\1_DATA\Rheenen\tvl_jr\SP8\2024Nov22_SI_1mg_1year_3D_2D-merge\Villus_crops\2024Nov22_SI_1mg_1year_3D_2D-merge-1-2\yz_masks.tif"
file_path_xz_masks = r"E:\1_DATA\Rheenen\tvl_jr\SP8\2024Nov22_SI_1mg_1year_3D_2D-merge\Villus_crops\2024Nov22_SI_1mg_1year_3D_2D-merge-1-2\xz_masks.tif"
file_path_nuclei_masks = r"E:\1_DATA\Rheenen\tvl_jr\SP8\2024Nov22_SI_1mg_1year_3D_2D-merge\Villus_crops\2024Nov22_SI_1mg_1year_3D_2D-merge-1-2\nuclei_masks.tif"
out_path = os.path.split(file_path_yx_masks)[0]

# Read YX masks
yx_masks = tifffile.imread(file_path_yx_masks)

if stitch_method == "iou":

    print("Running IoU stitching...")

    iou_masks = stitch3D(yx_masks, stitch_threshold=0.25)
    tifffile.imwrite(os.path.join(out_path, "iou_masks.tif"), iou_masks)

elif stitch_method == "cellstitch":

    # Read YZ masks
    yz_masks = tifffile.imread(file_path_yz_masks)

    # Read XZ masks
    xz_masks = tifffile.imread(file_path_xz_masks)

    nuclei = tifffile.imread(file_path_nuclei_masks)

    print("Running CellStitch stitching...")

    cellstitch_masks = full_stitch(
        yx_masks, yz_masks, xz_masks, nuclei, verbose=True
    )

    tifffile.imwrite(os.path.join(out_path, "cellstitch_masks.tif"), cellstitch_masks)

    # cellstitch_masks = full_interpolate(cellstitch_masks, anisotropy=4, n_jobs=-1, verbose=True)
    #
    # tifffile.imwrite(os.path.join(out_path, "cellstitch_masks_interpolated.tif"), cellstitch_masks)

else:
    print("Incompatible stitching method.")
