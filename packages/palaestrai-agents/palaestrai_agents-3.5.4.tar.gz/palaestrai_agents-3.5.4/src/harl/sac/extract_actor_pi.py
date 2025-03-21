import argparse
import os

import torch

from harl.sac.network import Actor, SquashedGaussianMLPActor


def main():
    models_path = os.getenv("MODEL_PATH", "../../../models")

    parser = argparse.ArgumentParser(
        description="Extract combined PyTorch actor model"
        "(continous, deterministic, of net and mu_layer)"
    )
    parser.add_argument(
        "--file_name",
        type=str,
        required=True,
        help="file name of actor object, relative to MODEL_PATH (env var, default: ../../../models)",
    )
    args = parser.parse_args()
    file_name = args.file_name

    model_path = os.path.join(models_path, file_name)
    model: Actor = torch.load(
        model_path, weights_only=False, map_location=torch.device("cpu")
    )  # type: ignore[annotation-unchecked]
    pi: SquashedGaussianMLPActor = model.pi  # type: ignore[annotation-unchecked]

    modules = []

    for i, (name, m) in enumerate(pi.net.named_children()):
        modules.append(m)

    modules.append(pi.mu_layer)

    net = torch.nn.Sequential(*modules)

    actor_path = os.path.join(
        models_path, file_name.replace(".", "_") + "_pi_net_mu.pt"
    )

    torch.save(net, str(actor_path))


if __name__ == "__main__":
    main()
