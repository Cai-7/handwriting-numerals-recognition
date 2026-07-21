import torch
from torchvision import transforms
from PIL import Image
from my_model import SimpleNet

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = SimpleNet().to(device)
model.load_state_dict(torch.load("mnist_net.pth", map_location=device, weights_only=True))
model.eval()

transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.Grayscale(num_output_channels=1),
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])


@torch.no_grad()
def predict(image_path: str) -> int:
    img = Image.open(image_path)
    img_tensor = transform(img).unsqueeze(0).to(device)
    output = model(img_tensor)
    pred = output.argmax(1).item()
    print(f"预测结果: {pred}")
    return pred


if __name__ == "__main__":
    predict("my_test.png")
