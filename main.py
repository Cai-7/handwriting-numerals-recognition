import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from my_model import SimpleNet
from train import train_one_epoch, evaluate

if __name__ == "__main__":
    batch_size = 128
    epochs = 30
    lr = 0.001
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_transform = transforms.Compose([
        transforms.RandomRotation(15),
        transforms.RandomAffine(0, translate=(0.1, 0.1)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ])
    test_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ])

    train_dataset = datasets.MNIST(root="./data", train=True, transform=train_transform, download=True)
    test_dataset = datasets.MNIST(root="./data", train=False, transform=test_transform, download=True)

    val_size = int(len(train_dataset) * 0.1)
    train_size = len(train_dataset) - val_size
    train_subset, val_subset = random_split(train_dataset, [train_size, val_size])

    train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_subset, batch_size=batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    print(f"训练集: {len(train_subset)} 样本, {len(train_loader)} 批次")
    print(f"验证集: {len(val_subset)} 样本")
    print(f"测试集: {len(test_dataset)} 样本")
    print(f"设备: {device}")

    model = SimpleNet().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    warmup_scheduler = optim.lr_scheduler.LinearLR(optimizer, start_factor=0.1, total_iters=5)
    main_scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs - 5)
    scheduler = optim.lr_scheduler.SequentialLR(optimizer, [warmup_scheduler, main_scheduler], milestones=[5])

    best_val_acc = 0.0
    best_model_state = None
    early_stop_count = 0
    early_stop_patience = 5

    for epoch in range(epochs):
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        scheduler.step()

        print(f"Epoch [{epoch + 1}/{epochs}]  "
              f"Train Loss: {train_loss:.4f}  Acc: {train_acc:.2f}%  |  "
              f"Val Loss: {val_loss:.4f}  Acc: {val_acc:.2f}%  "
              f"LR: {optimizer.param_groups[0]['lr']:.6f}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_model_state = model.state_dict().copy()
            early_stop_count = 0
        else:
            early_stop_count += 1

        if early_stop_count >= early_stop_patience:
            print(f"早停触发，最佳验证准确率: {best_val_acc:.2f}%")
            break

    if best_model_state is not None:
        model.load_state_dict(best_model_state)

    test_loss, test_acc = evaluate(model, test_loader, criterion, device)
    print(f"\n测试集准确率: {test_acc:.2f}%")

    torch.save(model.state_dict(), "mnist_net.pth")
    print("模型已保存为 mnist_net.pth")
