# 🚀 argcfg

**argcfg** 🛠️ is a Python library for managing structured configuration parameters. It is particularly useful for **machine learning experiments** 🤖, **deep learning pipelines** 🧠, and **CLI applications** 💻, allowing users to define structured configuration objects using Python's `dataclass` and update them dynamically from command-line arguments.

📌 **GitHub Repository:** https://github.com/CrawlScript/argcfg

## ✨ Features

- ✅ **Structured Configuration Management**: Define configurations using `dataclass` for clarity and maintainability.
- 🔧 **Easy CLI Argument Parsing**: Override configuration parameters from the command line.
- 📦 **Custom Default Configurations**: Load default settings based on runtime parameters (e.g., dataset choice).
- 🔥 **Seamless Integration**: Works well for ML experiments, deep learning models, and parameter tuning.

## 📥 Installation

Install `argcfg` via pip:

```bash
pip install argcfg
```

---

## 🚀 Usage


Below is a complete example demonstrating how to use `argcfg` to define a configuration class, manually set arguments, and override default settings from the command line.



### **Example: Using `argcfg` for Training Configuration**

#### **1. Create `demo_argcfg.py`**
```python
from dataclasses import dataclass
import typing
import argcfg
import argparse
import sys

# Step 1: Define a configuration class with default hyperparameters
@dataclass
class TrainingConfig:
    learning_rate: float = 0.001
    batch_size: int = 32
    num_epochs: int = 10
    hidden_channels: typing.List[int] = None
    dropout: float = 0.2
    use_bn: bool = True  # Use batch normalization by default


# Step 2: Load a default configuration based on the dataset
def load_default_cfg(dataset):
    """Returns a dataset-specific default TrainingConfig."""
    if dataset == "mnist":
        return TrainingConfig(
            batch_size=64,  
            num_epochs=20   
        )
    elif dataset == "cifar10":
        return TrainingConfig(
            dropout=0.4,    
            learning_rate=0.01  
        )
    else:
        return TrainingConfig()  


if __name__ == "__main__":

    # Step 3: Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Training Configuration")

    # Define dataset argument first, as it determines the default config
    parser.add_argument("--dataset", type=str, help="Dataset name")

    # Dynamically add arguments based on TrainingConfig fields
    argcfg.add_args_by_config_class(parser, TrainingConfig, verbose=True)


    # Uncomment the following block if you want to test this script without manually passing CLI arguments
    # This simulates running:
    # python demo_argcfg.py --dataset cifar10 --num_epochs 50 --hidden_channels 32,64,128 --use_bn False
    # Note that, you do not need to pass all the arguments, only the ones you want to override

    # cmd = "--dataset cifar10 --num_epochs 50 --hidden_channels 32,64,128 --use_bn False"
    # sys.argv += cmd.split()


    # Step 4: Parse command-line arguments
    args = parser.parse_args()

    # Step 5: Load the default configuration based on the dataset
    config = load_default_cfg(args.dataset)

    # Step 6: Override default config values with parsed arguments
    argcfg.combine_args_into_config(config, args, verbose=True)

    # Step 7: Display the final configuration after merging defaults & parsed arguments
    print("Final Configuration:")
    print(config)
```

### **2. Running the Demo**
To run the demo script and override specific arguments, use the following command:

```bash
python demo_argcfg.py --dataset cifar10 --num_epochs 50 --hidden_channels 32,64,128 --use_bn False
```

You can omit any argument to keep its default value.



### 📌 Expected Output

After running the example code, the output will look like this:

```
generate argument --learning_rate with type <class 'float'>
generate argument --batch_size with type <class 'int'>
generate argument --num_epochs with type <class 'int'>
generate argument --hidden_channels with type <function parse_int_list at 0x7fdd66b0adc0>
generate argument --dropout with type <class 'float'>
generate argument --use_bn with type <function parse_bool at 0x7fdd66b0ad30>

set config.num_epochs based on args.num_epochs: 10 => 50
set config.hidden_channels based on args.hidden_channels: None => [32, 64, 128]
set config.use_bn based on args.use_bn: True => False

Final Configuration:
TrainingConfig(learning_rate=0.01, batch_size=32, num_epochs=50, hidden_channels=[32, 64, 128], dropout=0.4, use_bn=False)
```
