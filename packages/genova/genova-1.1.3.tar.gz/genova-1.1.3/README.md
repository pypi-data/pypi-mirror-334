# Genova - A General-Purpose Python Library

**Genova** is a versatile Python library designed to offer easy-to-use utilities for a variety of domains such as mathematics, machine learning, finance, and more. With its modular structure, **Genova** makes it simple to access and apply mathematical operations, machine learning models, financial tools, and more, making it an essential library for both professionals and enthusiasts.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Math Module](#math-module)
  - [AI Models Module](#ai-models-module) - Coming soon
  - [Finance Module](#finance-module) - Coming soon
- [Examples](#examples)
  - [Math Examples](#math-examples)
  - [AI Models Examples](#ai-models-examples)
  - [Finance Examples](#finance-examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install **Genova** via **pip**:

```bash
pip install genova
```

````

Alternatively, if you want to install the latest version directly from GitHub, use the following command:

```bash
pip install git+https://github.com/egegvner/genova.git
```

## Usage

Once installed, you can use the library to perform various tasks. Here are some examples of how to get started with different modules:

### Math Module

The **`genova.math`** module offers utilities for mathematical operations, such as polynomial derivatives, turning points, and gradients.

#### Derivative of a Polynomial

```python
from genova.math import calculus

coefficients = [2, -3, 5]  # 2x^2 - 3x + 5
derivative = calculus.derivative(coefficients)
print(derivative)  # Output: "4x - 3"
```

#### Turning Points of a Polynomial

```python
coefficients = [1, -3, 2]  # x^2 - 3x + 2
turning_points, derivative_str = calculus.turning_points(2, 1, -3, 2)
print(turning_points)  # Output: [(1.0, 0.0)]
print(derivative_str)  # Output: "2x - 3"
```

#### Gradient at a Point

```python
x = 1
gradient = calculus.gradient_at_point(coefficients, x)
print(gradient)  # Output: 3
```

### AI Models Module

The **`genova.models`** module provides utilities to work with machine learning models, including training, evaluating, and making predictions.

#### Simple Neural Network for MNIST

```python
from genova.models import neural_networks

model = neural_networks.build_mnist_model()
model.summary()  # Displays the model architecture
```

### Finance Module

The **`genova.finance`** module offers tools for financial calculations, including stock price analysis and basic financial tools.

#### Get Latest Stock Price

```python
from genova.finance import stocks

stock_price = stocks.get_stock_price("AAPL")
print(stock_price)  # Output: Latest Apple stock price
```

## Examples

### Math Examples

- **Derivative**: Calculate the derivative of polynomials and express it in human-readable format.
- **Turning Points**: Find the turning points (local minima and maxima) of a polynomial function.
- **Gradient**: Compute the gradient (slope) of a polynomial at any given point.

### AI Models Examples

- **Model Building**: Build machine learning models with ease using predefined functions.
- **Training**: Quickly set up neural networks for training on datasets (e.g., MNIST).
- **Prediction**: Use trained models for making predictions or classification tasks.

### Finance Examples

- **Stock Data**: Fetch real-time stock prices using `yfinance`.
- **Financial Calculations**: Work with basic finance-related calculations, such as loan repayments, stock price trends, etc.

## Contributing

We welcome contributions to **Genova**! If you have ideas for new features, improvements, or bug fixes, please follow the steps below:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request with a detailed description of your changes.

Please ensure that your code follows the existing style and includes tests where applicable.

## License

**Genova** is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Feel free to explore the library, contribute, or contact the maintainers if you need further help or have any questions.
````
