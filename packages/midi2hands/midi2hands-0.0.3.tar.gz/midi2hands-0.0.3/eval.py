from models.lstm import LSTMModel
from typing import Callable
import pandas as pd
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import torch
from torch import nn
from torch.utils.data import DataLoader
import argparse
import json
from pathlib import Path
import utils as U
import numpy as np


def get_model(model_dir, h_params, device):
    """Try to read the model from the state_dict file"""

    model = eval(h_params["model_func"])(h_params)
    model.load_state_dict(torch.load(model_dir / "model.pth", map_location=device))
    model.eval()
    return model


def get_test_files():
    return list(Path("data/test").glob("*.mid"))


def accuracy_loss_plot(save_dir: Path, filename: str, results: dict, fold=0):
    val_acc = results[f"fold_{fold}"]["val_acc"]
    val_loss = results[f"fold_{fold}"]["val_loss"]
    train_acc = results[f"fold_{fold}"]["train_acc"]
    train_loss = results[f"fold_{fold}"]["train_loss"]
    fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(12, 6))
    ax[0].plot(val_acc, label="Validation accuracy")
    ax[0].plot(train_acc, label="Train accuracy")
    ax[0].set_title("Accuracy")
    ax[0].legend()

    ax[1].plot(val_loss, label="Validation loss")
    ax[1].plot(train_loss, label="Train loss")
    ax[1].set_title("Loss")
    ax[1].legend()

    plt.show()
    # save fig
    fig.savefig(save_dir / filename)


def to_onnx(model_dir, filename, window_size, input_size, **h_params):
    # convert to onnx
    model = get_model(model_dir, h_params, "cpu")
    model.eval()
    dummy_input = torch.randn(1, window_size, input_size)
    torch.onnx.export(model, dummy_input, model_dir / filename)


def get_test_acc(model, h_params):
    test_paths = get_test_files()
    y_true, y_pred = [], []
    for mid_path in test_paths:
        events, y_true, y_pred = eval(h_params["inference_func"])(
            mid_path, model, h_params["window_size"], h_params["device"]
        )
        print(f"accuracy: {U.accuracy(y_true, y_pred)}")
    print(classification_report(y_true, y_pred))


def get_k_fold_results(model_dir, results):
    # get the results of the k-fold

    with open(model_dir / "results.json", "r") as f:
        results = json.load(f)
    # create a pandas dataframe with the results
    data = {
        "fold": [],
        "train_acc": [],
        "train_loss": [],
        "val_acc": [],
        "val_loss": [],
        "generative_acc_mean": [],
        "generative_acc_std": [],
    }
    fold_keys = [key for key in results.keys() if "fold" in key]
    for fold in fold_keys:
        data["fold"].append(fold)
        data["train_acc"].append(np.max(results[fold]["train_acc"]))
        data["train_loss"].append(np.min(results[fold]["train_loss"]))
        data["val_acc"].append(np.max(results[fold]["val_acc"]))
        data["val_loss"].append(np.min(results[fold]["val_loss"]))
        data["generative_acc_mean"].append(
            np.mean(results[fold]["generative_accuracy"])
        )
        data["generative_acc_std"].append(np.std(results[fold]["generative_accuracy"]))

    df = pd.DataFrame(data)

    # print the results
    print(df)
    # print a latex table of the results, use 4 decimal places
    print(df.to_latex(float_format="%.4f"))


def generate_videos(mid_path: Path, model_dir: Path, model, **h_params):
    """
    Saves a rendered video of the predicted events, the original events and video of error events marked red
    """
    print(mid_path)
    import os

    try:
        import src.main as M  # type: ignore
    except ModuleNotFoundError:
        print("You have not installed the video generator package")
        return

    from pathlib import Path

    model = model.to(h_params["device"])

    out_dir = model_dir / str(mid_path.name)
    if not out_dir.exists():
        out_dir.mkdir()

    events, y_true, y_pred = eval(h_params["inference_func"])(
        mid_path, model, h_params["window_size"], h_params["device"]
    )
    print(y_true[:10], y_pred[:10])
    print(f"accuracy: {U.accuracy(y_true, y_pred)}")

    midi2vid_program = os.getenv("MIDI2VID_PROGRAM")
    # the binary is yet
    # get the test data

    # 1. Create the predicted events
    U.note_events_to_json(events, output_file_path=out_dir / "original.json")

    predicted_events = events.copy()
    for i in range(len(predicted_events)):
        predicted_events[i].hand = "left" if y_pred[i] == 0 else "right"
    U.note_events_to_json(predicted_events, output_file_path=out_dir / "predicted.json")

    # 2. Create a combined version where a wrong assignment is marked with None
    merged_events = events.copy()
    for i in range(len(merged_events)):
        if y_pred[i] != y_true[i]:
            merged_events[i].hand = None
        else:
            merged_events[i].hand = "left" if y_true[i] == 0 else "right"
    U.note_events_to_json(merged_events, output_file_path=out_dir / "merged.json")

    M.convert_video(
        mid_path, out_dir / "original.mp4", events_path=out_dir / "original.json"
    )
    M.convert_video(
        mid_path,
        out_dir / "predicted.mp4",
        events_path=out_dir / "predicted.json",
    )
    M.convert_video(
        mid_path,
        out_dir / "merged.mp4",
        events_path=out_dir / "merged.json",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", type=str, required=True)
    args = parser.parse_args()

    # results and h_params
    model_dir = Path(args.model_dir)
    with open(model_dir / "results.json", "r") as f:
        results = json.load(f)
    h_params = results["h_params"]

    video = False
    to_onnex = False
    inference_acc = False
    train_stats = False
    k_fold_results = True

    device = U.get_device()
    h_params["device"] = str(device)

    model = get_model(model_dir, h_params, device).to(device)
    test_paths = get_test_files()

    if video:
        generate_videos(
            mid_path=test_paths[1],
            model_dir=model_dir,
            model=model,
            **h_params,
        )
    if inference_acc:
        get_test_acc(model, h_params)
    if to_onnex:
        to_onnx(model_dir, "model.onnx", **h_params)
    if train_stats:
        accuracy_loss_plot(model_dir, "training.png", results, fold=0)
    if k_fold_results:
        get_k_fold_results(model_dir, results)
