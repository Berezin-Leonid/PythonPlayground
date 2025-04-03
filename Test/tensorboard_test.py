import torch
from torch.utils.tensorboard import SummaryWriter

exp = "exp2"
train_writer = SummaryWriter(comment=f"{exp}_train_loss", log_dir=f"runs/{exp}")


for i in range(1000):
    train_writer.add_scalar("Loss", (1/(i + 1)), i)

train_writer.close()