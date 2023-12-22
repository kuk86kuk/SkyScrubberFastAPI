#from detection import MaskInpainting, BigImage


# async def run_neural_network(neuro_id, kwargs, tag_folder_path):
#          dev_opt_remove(kwargs, tag_folder_path)

async def dev_opt_remove(kwargs, tag_folder_path):
    try:
        image_dir = kwargs.get("image_dir", "../images")
        image_format = kwargs.get("image_format", "*.tif")
        save_dir = kwargs.get("save_dir", tag_folder_path)
        device = kwargs.get("device", "cuda")
        sigma = kwargs.get("sigma", 21)
        patch_shape = kwargs.get("patch_shape", [512, 512])
        step_patch = kwargs.get("step_patch", [512, 512])

        mask_inpainting =  None#MaskInpainting(device=device, sigma=sigma)
        mask_inpainting.retouch_dir(
            root_dir=image_dir,
            file_format=image_format,
            save_dir=save_dir,
            patch_shape=patch_shape,
            dx=step_patch[0],
            dy=step_patch[1]
        )
        return {"status": "success", "message": "Neural network processing completed."}
    except Exception as e:
        return {"status": "error", "message": f"Error during neural network processing: {str(e)}"} 
# =======
# async def dev_opt_remove(kwargs, tag_folder_path):
#     try:
#         image_dir = kwargs.get("image_dir", "../images")
#         image_format = kwargs.get("image_format", "*.tif")
#         save_dir = kwargs.get("save_dir", tag_folder_path)
#         device = kwargs.get("device", "cuda")
#         sigma = kwargs.get("sigma", 21)
#         patch_shape = kwargs.get("patch_shape", [512, 512])
#         step_patch = kwargs.get("step_patch", [512, 512])

#         mask_inpainting = MaskInpainting(device=device, sigma=sigma)
#         mask_inpainting.retouch_dir(
#             root_dir=image_dir,
#             file_format=image_format,
#             save_dir=save_dir,
#             patch_shape=patch_shape,
#             dx=step_patch[0],
#             dy=step_patch[1]
#         )
#         return {"status": "success", "message": "Neural network processing completed."}
#     except Exception as e:
#         return {"status": "error", "message": f"Error during neural network processing: {str(e)}"} 
