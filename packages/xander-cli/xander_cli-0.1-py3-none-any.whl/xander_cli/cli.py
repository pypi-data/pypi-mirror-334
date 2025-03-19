import argparse
from .xander import Xander

def train(task, dataset_path, target_col=None, model_name=None, epochs=None):
    new_epochs = 10 if not epochs else epochs
    
    if task == "image":
        xander_instance = Xander(dataset_path=dataset_path, task=task, model_name=model_name, hyperparameters={"epochs": new_epochs})
    else:
        xander_instance = Xander(dataset_path=dataset_path, task=task, target_col=target_col, model_name=model_name, hyperparameters={"epochs": new_epochs})
    
    xander_instance.train()

def main():
    parser = argparse.ArgumentParser(prog="xander-cli", description="Xander AI CLI")
    
    subparsers = parser.add_subparsers(dest="command")

    train_parser = subparsers.add_parser("train", help="Train an AI model")
    train_parser.add_argument("task", type=str, choices=["classification", "regression", "text", "image"], help="Type of task")
    train_parser.add_argument("dataset_path", type=str, help="Path to dataset file")
    train_parser.add_argument("model_name", type=str, help="Name you want to give to your model")
    train_parser.add_argument("epochs", type=int, nargs="?", default=10, help="Number of epochs you want to train for (default: 10)")

    train_parser.add_argument("--target_col", type=str, required=False, help="Target column name (only for text and tabular tasks)")

    args = parser.parse_args()

    if args.command == "train":
        train(args.task, args.dataset_path, args.target_col, args.model_name, args.epochs)

if __name__ == "__main__":
    main()
