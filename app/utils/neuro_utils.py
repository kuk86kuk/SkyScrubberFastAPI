from celery import Celery
#import detection
from concurrent.futures import ThreadPoolExecutor
import asyncio
import concurrent.futures
import time
from celery.utils.log import get_task_logger

celery = Celery('tasks', broker='redis://localhost:6379', backend='redis://localhost:6379')
logger = get_task_logger(__name__)

@celery.task(bind=True)
def run_neural_network(self, neuro_id, kwargs, tag_folder_path):
    try:
        # Ваш код задачи
        time.sleep(5)
        logger.info(f"Task {self.request.id} completed successfully.")
        return {"status": "completed"}
    except Exception as e:
        logger.error(f"Task {self.request.id} failed with error: {str(e)}")
        raise

# def dev_opt_remove(kwargs, tag_folder_path):
#     try:
#         image_dir = kwargs.get("image_dir", "images")
#         image_format = kwargs.get("image_format", "*.tif")
#         save_dir = kwargs.get("save_dir", tag_folder_path)
#         device = kwargs.get("device", "cuda")
#         sigma = kwargs.get("sigma", 21)
#         patch_shape = kwargs.get("patch_shape", [512, 512])
#         step_patch = kwargs.get("step_patch", [512, 512])

#         mask_inpainting = detection.MaskInpainting(device=device, sigma=sigma)
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