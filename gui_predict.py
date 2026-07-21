import tkinter as tk
from tkinter import filedialog, messagebox
import torch
from torchvision import transforms
from PIL import Image, ImageTk
from my_model import SimpleNet

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleNet().to(device)
try:
    model.load_state_dict(torch.load("mnist_net.pth", map_location=device, weights_only=True))
    model.eval()
except FileNotFoundError:
    messagebox.showerror("错误", "找不到 mnist_net.pth，请先运行 train.py")

transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.Grayscale(num_output_channels=1),
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])


def upload_and_predict():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
    if not file_path:
        return
    try:
        img_open = Image.open(file_path)
        img_display = img_open.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img_display)
        image_label.config(image=img_tk)
        image_label.image = img_tk

        img_tensor = transform(img_open).unsqueeze(0).to(device)
        with torch.no_grad():
            output = model(img_tensor)
            pred = output.argmax(1).item()
        result_label.config(text=f"识别结果: {pred}", fg="#4CAF50")
    except Exception as e:
        messagebox.showerror("错误", f"识别失败: {e}")


root = tk.Tk()
root.title("手写数字识别")
root.geometry("400x480")
root.configure(bg="#212121")

title_label = tk.Label(
    root, text="手写数字识别", font=("Arial", 18, "bold"),
    bg="#212121", fg="#FFFFFF"
)
title_label.pack(pady=20)

image_label = tk.Label(
    root, text="请上传图片", font=("Arial", 11),
    bg="#333333", fg="#AAAAAA", width=25, height=10
)
image_label.pack(pady=10)

upload_btn = tk.Button(
    root, text="上传图片并识别", font=("Arial", 12, "bold"),
    bg="#4CAF50", fg="white", activebackground="#45a049",
    activeforeground="white", bd=0, padx=10, pady=5,
    command=upload_and_predict
)
upload_btn.pack(pady=15)

result_label = tk.Label(
    root, text="等待上传...", font=("Arial", 20, "bold"),
    bg="#212121", fg="#FF5252"
)
result_label.pack(pady=20)

root.mainloop()
