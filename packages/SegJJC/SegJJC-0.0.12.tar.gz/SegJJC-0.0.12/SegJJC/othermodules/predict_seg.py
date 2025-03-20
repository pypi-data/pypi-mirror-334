import os
import json
import time
import torch
from torchvision import transforms
import numpy as np
from PIL import Image
import torchvision.models.segmentation as models
from pathlib import Path

from SegJJC.fcn.src import fcn_resnet50,fcn_resnet18,fcn_resnet34,deeplabv3_resnet18,deeplabv3_resnet34
try:
    from ultralytics.utils.plotting import colors
    ULTRALYTICS_COLORS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_COLORS_AVAILABLE = False

class PredictSahi_fcn:
    def __init__(self, model_path,params):
        self.modelpath=model_path
        self.trueimgsize = params["inferimgsz"]
        self.testimg_dir = params['testimg']
        self.saveimg_dir = params['inferedimg']
        self.aux=False
        self.inferdevicehandle=params.get("inferdevicehandle",0)
        # if self.inferdevicehandle=='gpu':
        #     self.inferdevicehandle=0
        # 加载 palette
        self.palette = self.load_palette()
        self.yolocolors=True##是否使用yolo自带的掩膜color颜色盘，用于标记目标区域
        self.infer_format=params.get("infer_format","pt")
    def load_palette(self):
        """ 从 JSON 文件加载颜色映射 """
        json_path = os.path.join(os.path.dirname(__file__), "..", "fcn", "palette.json")
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"颜色映射文件 {json_path} 不存在！")

        with open(json_path, "r") as f:
            return json.load(f)
    def time_synchronized(self):
        torch.cuda.synchronize() if torch.cuda.is_available() else None
        return time.time()

    def mask_to_color(self,mask,palette=None):
        """
        将语义分割得到的 mask（每个像素为类别ID）转换成彩色图
        """
        if not palette:
            palette=colors.palette
            h, w = mask.shape
            color_mask = np.zeros((h, w, 3), dtype=np.uint8)
            cls_id=0
            for color in palette:
                color_mask[mask == cls_id] = color
                cls_id+=1
            return color_mask
        else:
            """
            将语义分割得到的 mask（每个像素为类别ID）转换成彩色图
            """
            h, w = mask.shape
            color_mask = np.zeros((h, w, 3), dtype=np.uint8)
            for cls_id, color in palette.items():
                cls_id = int(cls_id)  # 将字符串类型的类别ID转换为整数
                color_mask[mask == cls_id] = color
            return color_mask

    def blend_mask_region(self,original_img, color_mask, mask, alpha=0.3):
        """
        仅对 mask 区域进行半透明叠加
          - original_img：原始RGB图像 (PIL Image)
          - color_mask：彩色mask (numpy数组，形状(H,W,3))
          - mask：语义分割结果 (numpy数组，像素值代表类别ID, 背景通常为0)
          - alpha：混合因子，在目标区域使用
        """
        # 转换为 numpy 数组（float32）
        original = np.array(original_img).astype(np.float32)
        overlay = color_mask.astype(np.float32)

        # 构造布尔 mask，将其沿通道重复3次，形状变为 (H, W, 3)
        mask_bool = np.repeat((mask > 0)[:, :, None], 3, axis=2)

        # 使用 np.where 只在 mask 区域混合，否则保持原图
        blended = np.where(mask_bool, original * (1 - alpha) + overlay * alpha, original)
        blended = np.clip(blended, 0, 255).astype(np.uint8)
        return Image.fromarray(blended)

    def process_image(self,model, device, img_path, output_path):
        # pt/pth模式推理
        if self.infer_format in ['pt', 'pth']:
            # 加载图像
            original_img = Image.open(img_path)
            if original_img.mode != 'RGB':
                original_img = original_img.convert('RGB')

            # 图像预处理
            data_transform = transforms.Compose([
                transforms.Resize(self.trueimgsize[0]),
                transforms.ToTensor(),
                transforms.Normalize(mean=(0.485, 0.456, 0.406),
                                     std=(0.229, 0.224, 0.225))
            ])
            img_tensor = data_transform(original_img)
            img_tensor = torch.unsqueeze(img_tensor, dim=0).to(device)

            model.eval()
            with torch.no_grad():
                t_start = self.time_synchronized()
                output = model(img_tensor)
                t_end = self.time_synchronized()
                print(f"Inference time for {os.path.basename(img_path)}: {t_end - t_start:.3f}s")

            # 假设模型输出 'out' 为分割结果
            prediction = output['out'].argmax(1).squeeze(0)
            mask = prediction.cpu().numpy().astype(np.uint8)

            # 将 mask 转为彩色图
            # 生成彩色 mask
            if ULTRALYTICS_COLORS_AVAILABLE and self.yolocolors:
                color_mask = self.mask_to_color(mask)
            else:
                color_mask = self.mask_to_color(mask, self.palette)
            # color_mask = self.mask_to_color(mask, self.palette)
            # 仅在 mask 区域进行半透明叠加
            blended_img = self.blend_mask_region(original_img, color_mask, mask, alpha=0.5)
            blended_img.save(output_path)
            print("Saved result to", output_path)
        # onnx模式推理
        if self.infer_format in ['onnx']:
            # 加载图像
            original_img = Image.open(img_path)
            if original_img.mode != 'RGB':
                original_img = original_img.convert('RGB')

            # 图像预处理
            data_transform = transforms.Compose([
                transforms.Resize(self.trueimgsize[0]),
                transforms.ToTensor(),
                transforms.Normalize(mean=(0.485, 0.456, 0.406),
                                     std=(0.229, 0.224, 0.225))
            ])
            img_tensor = data_transform(original_img).unsqueeze(0).numpy()  # 转换为 numpy

            # 获取 ONNX 输入名
            input_name = model.get_inputs()[0].name
            output_name = model.get_outputs()[0].name
            t_start = self.time_synchronized()
            output = model.run([output_name], {input_name: img_tensor})[0]
            t_end = self.time_synchronized()
            print(f"Inference time for {os.path.basename(img_path)}: {t_end - t_start:.3f}s")
            # 获取最大概率类别
            prediction = np.argmax(output, axis=1).squeeze(0).astype(np.uint8)

            # 将 mask 转为彩色图
            # 生成彩色 mask
            if ULTRALYTICS_COLORS_AVAILABLE and self.yolocolors:
                color_mask = self.mask_to_color(prediction)
            else:
                color_mask = self.mask_to_color(prediction, self.palette)
            # color_mask = self.mask_to_color(mask, self.palette)
            # 仅在 mask 区域进行半透明叠加
            blended_img = self.blend_mask_region(original_img, color_mask, prediction, alpha=0.5)
            blended_img.save(output_path)
            print("Saved result to", output_path)
        # openvino模式推理
        if self.infer_format in ['openvino']:
            # 加载图像
            original_img = Image.open(img_path)
            if original_img.mode != 'RGB':
                original_img = original_img.convert('RGB')

            # 图像预处理
            data_transform = transforms.Compose([
                transforms.Resize(self.trueimgsize[0]),
                transforms.ToTensor(),
                transforms.Normalize(mean=(0.485, 0.456, 0.406),
                                     std=(0.229, 0.224, 0.225))
            ])
            img_tensor = data_transform(original_img).unsqueeze(0).numpy()  # 转换为 numpy

            # 获取模型输入输出名称
            input_name = model.inputs[0].get_any_name()
            output_name = model.outputs[0].get_any_name()
            # 创建推理请求，并执行推理
            infer_request = model.create_infer_request()
            t_start = self.time_synchronized()
            results = infer_request.infer({input_name: img_tensor})
            t_end = self.time_synchronized()
            print(f"Inference time for {os.path.basename(img_path)}: {t_end - t_start:.3f}s")
            # 获取输出（假定输出形状为 (1, num_classes, 256, 256)）
            output = results[output_name]
            prediction = np.argmax(output, axis=1).squeeze(0).astype(np.uint8)

            # 将 mask 转为彩色图
            # 生成彩色 mask
            if ULTRALYTICS_COLORS_AVAILABLE and self.yolocolors:
                color_mask = self.mask_to_color(prediction)
            else:
                color_mask = self.mask_to_color(prediction, self.palette)
            # color_mask = self.mask_to_color(mask, self.palette)
            # 仅在 mask 区域进行半透明叠加
            blended_img = self.blend_mask_region(original_img, color_mask, prediction, alpha=0.5)
            blended_img.save(output_path)
            print("Saved result to", output_path)
    def predict_normal(self):
        #pt/pth模式推理
        if self.infer_format in ['pt','pth']:
            #获取所有设备
            # 获取所有 GPU 设备
            num_gpus = torch.cuda.device_count()
            gpu_list = [f"{i}: {torch.cuda.get_device_name(i)}" for i in range(num_gpus)]

            print(f"Available GPUs: {gpu_list}")
            # 配置设备
            if self.inferdevicehandle == 'cpu' :
                device = torch.device("cpu")
            elif self.inferdevicehandle == 'gpu':
                device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            else:
                device = torch.device(f"cuda:{self.inferdevicehandle}" if torch.cuda.is_available() else "cpu")
            print("Using device:", device)
            # 创建模型（使用 FCN-ResNet50）
            model_dict = torch.load(self.modelpath, map_location='cpu')
            diymodel_dict = {
                "fcn_resnet50": fcn_resnet50,
                "fcn_resnet18": fcn_resnet18,
                "fcn_resnet34": fcn_resnet34,
                "deeplabv3_resnet18": deeplabv3_resnet18,
                "deeplabv3_resnet34": deeplabv3_resnet34,
            }

            model_arch = model_dict["model_type"]
            if model_arch in diymodel_dict:
                model = diymodel_dict[model_arch](aux=self.aux, num_classes=model_dict['num_classes'] + 1)
            else:
                model = models.__dict__[model_arch](pretrained=False, pretrained_backbone=False,
                                                          num_classes=model_dict['num_classes'] + 1,
                                                          aux_loss=self.aux)
            weights_dict = model_dict['model'].state_dict()
            for k in list(weights_dict.keys()):
                if "aux" in k:
                    del weights_dict[k]
            model.load_state_dict(weights_dict)
            model.to(device)
            # from pathlib import Path
            Path(self.saveimg_dir).mkdir(parents=True, exist_ok=True)
            # os.makedirs(self.saveimg_dir, exist_ok=True)#传统创建
            # # 遍历文件夹中的所有图像
            # for filename in os.listdir(self.testimg_dir):
            #     if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            #         img_path = os.path.join(self.testimg_dir, filename)
            #         output_path = os.path.join(self.saveimg_dir, filename)
            #         print(f"Processing {img_path} ...")
            #         self.process_image(model, device, img_path, output_path)

            # 遍历 self.testimg_dir 下的所有子文件夹和图片
            for root, _, files in os.walk(self.testimg_dir):
                for filename in files:
                    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                        img_path = os.path.join(root, filename)  # 输入图像路径
                        # 计算相对路径
                        relative_path = os.path.relpath(root, self.testimg_dir)
                        # 生成输出目录，并保持相对路径结构
                        output_dir = os.path.join(self.saveimg_dir, relative_path)
                        os.makedirs(output_dir, exist_ok=True)
                        output_path = os.path.join(output_dir, filename)  # 输出路径

                        print(f"Processing {img_path} ...")
                        self.process_image(model, device, img_path, output_path)
        # onnx模式推理
        if self.infer_format in['onnx']:
            import onnxruntime as ort
            # 获取所有设备
            providers = ort.get_available_providers()
            print("Available ONNX Runtime providers:", providers)
            num_gpus = torch.cuda.device_count()
            gpu_list = [f"{i}: {torch.cuda.get_device_name(i)}" for i in range(num_gpus)]
            print(f"Available GPUs: {gpu_list}")
            #配置设备
            if self.inferdevicehandle == 'cpu':
                device = ['CPUExecutionProvider']
            elif self.inferdevicehandle == 'gpu':
                device = ['CUDAExecutionProvider' if torch.cuda.is_available() else 'CPUExecutionProvider']
            else:
                device = [('CUDAExecutionProvider',
                           {'device_id': int(self.inferdevicehandle)}) if torch.cuda.is_available() else 'CPUExecutionProvider']
                # device = torch.device(f"cuda:{self.inferdevicehandle}" if torch.cuda.is_available() else "cpu")
            print("Using device:", device)
            # 创建模型（使用 FCN-ResNet50）
            # 加载 ONNX 模型
            onnx_session = ort.InferenceSession(self.modelpath, providers=[
                'CUDAExecutionProvider' if torch.cuda.is_available() else 'CPUExecutionProvider'])

            # from pathlib import Path
            Path(self.saveimg_dir).mkdir(parents=True, exist_ok=True)
            # os.makedirs(self.saveimg_dir, exist_ok=True)#传统创建
            # # 遍历文件夹中的所有图像
            # for filename in os.listdir(self.testimg_dir):
            #     if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            #         img_path = os.path.join(self.testimg_dir, filename)
            #         output_path = os.path.join(self.saveimg_dir, filename)
            #         print(f"Processing {img_path} ...")
            #         self.process_image(model, device, img_path, output_path)

            # 遍历 self.testimg_dir 下的所有子文件夹和图片
            for root, _, files in os.walk(self.testimg_dir):
                for filename in files:
                    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                        img_path = os.path.join(root, filename)  # 输入图像路径
                        # 计算相对路径
                        relative_path = os.path.relpath(root, self.testimg_dir)
                        # 生成输出目录，并保持相对路径结构
                        output_dir = os.path.join(self.saveimg_dir, relative_path)
                        os.makedirs(output_dir, exist_ok=True)
                        output_path = os.path.join(output_dir, filename)  # 输出路径

                        print(f"Processing {img_path} ...")
                        self.process_image(onnx_session, device, img_path, output_path)
        # openvino模式推理
        if self.infer_format in['openvino']:
            from openvino.runtime import Core
            #获取所有设备
            core = Core()
            devices = core.available_devices
            device_info = {device: core.get_property(device, "FULL_DEVICE_NAME") for device in devices}
            print("Available OpenVINO devices:", device_info)
            # 配置设备
            if self.inferdevicehandle == 'cpu':
                device = "CPU"
            elif self.inferdevicehandle == 'gpu':
                # device = "GPU"
                device = "GPU.0"
            else:
                device = f"GPU.{self.inferdevicehandle}" if torch.cuda.is_available() else "CPU"
                # device = torch.device(f"cuda:{self.inferdevicehandle}" if torch.cuda.is_available() else "cpu")
            print("Using device:", device)

            # 创建模型（使用 FCN-ResNet50）
            model = core.read_model(self.modelpath)
            compiled_model = core.compile_model(model, device)
            # from pathlib import Path
            Path(self.saveimg_dir).mkdir(parents=True, exist_ok=True)
            # os.makedirs(self.saveimg_dir, exist_ok=True)#传统创建
            # # 遍历文件夹中的所有图像
            # for filename in os.listdir(self.testimg_dir):
            #     if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            #         img_path = os.path.join(self.testimg_dir, filename)
            #         output_path = os.path.join(self.saveimg_dir, filename)
            #         print(f"Processing {img_path} ...")
            #         self.process_image(model, device, img_path, output_path)

            # 遍历 self.testimg_dir 下的所有子文件夹和图片
            for root, _, files in os.walk(self.testimg_dir):
                for filename in files:
                    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                        img_path = os.path.join(root, filename)  # 输入图像路径
                        # 计算相对路径
                        relative_path = os.path.relpath(root, self.testimg_dir)
                        # 生成输出目录，并保持相对路径结构
                        output_dir = os.path.join(self.saveimg_dir, relative_path)
                        os.makedirs(output_dir, exist_ok=True)
                        output_path = os.path.join(output_dir, filename)  # 输出路径

                        print(f"Processing {img_path} ...")
                        self.process_image(compiled_model, device, img_path, output_path)
    # def predict_normal_onnx(self):
    #     # 配置设备
    #     if self.inferdevicehandle == 'cpu' :
    #         device = ['CPUExecutionProvider']
    #     elif self.inferdevicehandle == 'gpu':
    #         device = ['CUDAExecutionProvider' if torch.cuda.is_available() else 'CPUExecutionProvider']
    #     else:
    #         device = [('CUDAExecutionProvider', {'device_id': f"{self.inferdevicehandle}"}) if torch.cuda.is_available() else 'CPUExecutionProvider']
    #         # device = torch.device(f"cuda:{self.inferdevicehandle}" if torch.cuda.is_available() else "cpu")
    #     print("Using device:", device)
    #
    #     # 创建模型（使用 FCN-ResNet50）
    #     # 加载 ONNX 模型
    #     onnx_session = ort.InferenceSession(self.modelpath, providers=[
    #         'CUDAExecutionProvider' if torch.cuda.is_available() else 'CPUExecutionProvider'])
    #
    #     # from pathlib import Path
    #     Path(self.saveimg_dir).mkdir(parents=True, exist_ok=True)
    #     # os.makedirs(self.saveimg_dir, exist_ok=True)#传统创建
    #     # # 遍历文件夹中的所有图像
    #     # for filename in os.listdir(self.testimg_dir):
    #     #     if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
    #     #         img_path = os.path.join(self.testimg_dir, filename)
    #     #         output_path = os.path.join(self.saveimg_dir, filename)
    #     #         print(f"Processing {img_path} ...")
    #     #         self.process_image(model, device, img_path, output_path)
    #
    #     # 遍历 self.testimg_dir 下的所有子文件夹和图片
    #     for root, _, files in os.walk(self.testimg_dir):
    #         for filename in files:
    #             if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
    #                 img_path = os.path.join(root, filename)  # 输入图像路径
    #                 # 计算相对路径
    #                 relative_path = os.path.relpath(root, self.testimg_dir)
    #                 # 生成输出目录，并保持相对路径结构
    #                 output_dir = os.path.join(self.saveimg_dir, relative_path)
    #                 os.makedirs(output_dir, exist_ok=True)
    #                 output_path = os.path.join(output_dir, filename)  # 输出路径
    #
    #                 print(f"Processing {img_path} ...")
    #                 self.process_image(onnx_session, device, img_path, output_path)