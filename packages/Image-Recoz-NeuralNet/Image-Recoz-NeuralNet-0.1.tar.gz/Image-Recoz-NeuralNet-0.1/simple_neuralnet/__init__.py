import numpy as np
from sklearn.preprocessing import OneHotEncoder
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

class NeuralNetwork:
    def __init__(self, layers, activation='relu', output_activation='softmax'):
        self.layers = layers
        self.activation = activation
        self.output_activation = output_activation
        self.weights = []
        self.biases = []
        # He initialization for better convergence
        for i in range(1, len(layers)):
            self.weights.append(np.random.randn(layers[i - 1], layers[i]) * np.sqrt(2.0 / layers[i - 1]))
            self.biases.append(np.zeros((1, layers[i])))

    def _activation_function(self, x, activation):
        if activation == 'relu':
            return np.maximum(0, x)
        elif activation == 'sigmoid':
            return 1 / (1 + np.exp(-np.clip(x, -500, 500)))  # Prevent overflow
        elif activation == 'tanh':
            return np.tanh(x)
        elif activation == 'softmax':
            exp = np.exp(x - np.max(x, axis=1, keepdims=True))
            return exp / np.sum(exp, axis=1, keepdims=True)
        return x

    def _activation_derivative(self, x, activation):
        if activation == 'relu':
            return np.where(x > 0, 1, 0)
        elif activation == 'sigmoid':
            sig = self._activation_function(x, 'sigmoid')
            return sig * (1 - sig)
        elif activation == 'tanh':
            return 1 - np.tanh(x) ** 2
        return x

    def forward_propagation(self, X):
        self.a = [X]
        self.z = []
        for i in range(len(self.weights)):
            z = np.dot(self.a[-1], self.weights[i]) + self.biases[i]
            self.z.append(z)
            if i == len(self.weights) - 1:
                a = self._activation_function(z, self.output_activation)
            else:
                a = self._activation_function(z, self.activation)
            self.a.append(a)
        return self.a[-1]

    def backward_propagation(self, X, y, output):
        m = X.shape[0]
        self.dweights = []
        self.dbiases = []
        error = output - y
        dZ = error
        self.dweights.append(np.dot(self.a[-2].T, dZ) / m)
        self.dbiases.append(np.sum(dZ, axis=0, keepdims=True) / m)
        for i in range(len(self.weights) - 1, 0, -1):
            dZ = np.dot(dZ, self.weights[i].T) * self._activation_derivative(self.z[i - 1], self.activation)
            self.dweights.insert(0, np.dot(self.a[i - 1].T, dZ) / m)
            self.dbiases.insert(0, np.sum(dZ, axis=0, keepdims=True) / m)

    def update_parameters(self, learning_rate):
        for i in range(len(self.weights)):
            self.weights[i] -= learning_rate * self.dweights[i]
            self.biases[i] -= learning_rate * self.dbiases[i]

    def train(self, X, y, learning_rate=0.01, epochs=100, batch_size=32):
        for epoch in range(epochs):
            indices = np.random.permutation(X.shape[0])  # Shuffle data
            X_shuffled = X[indices]
            y_shuffled = y[indices]
            for i in range(0, X.shape[0], batch_size):
                X_batch = X_shuffled[i:i + batch_size]
                y_batch = y_shuffled[i:i + batch_size]
                output = self.forward_propagation(X_batch)
                self.backward_propagation(X_batch, y_batch, output)
                self.update_parameters(learning_rate)
            if epoch % 50 == 0:
                loss = np.mean(np.square(output - y_batch))
                print(f'Epoch {epoch}, Loss: {loss:.6f}')

    def predict(self, X):
        output = self.forward_propagation(X)
        return np.argmax(output, axis=1), output  # Return both class and probabilities

class NeuralUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Neural Recognizer")
        self.nn = None
        self.classes = None
        self.input_size = 784  # Default for 28x28 images
        self.show_dataset_page()

    def show_dataset_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Select Dataset Type:").pack(pady=5)
        self.data_type = tk.StringVar(value="image")
        tk.Radiobutton(self.root, text="Image Dataset (folder of labeled subfolders)", variable=self.data_type, value="image").pack()
        tk.Radiobutton(self.root, text="Text Dataset (CSV file)", variable=self.data_type, value="text").pack()

        tk.Button(self.root, text="Choose Dataset", command=self.load_and_train).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)

        self.root.mainloop()

    def load_and_train(self):
        X, y = None, None
        if self.data_type.get() == "image":
            folder = filedialog.askdirectory(title="Select Image Dataset Folder")
            if folder:
                X, y, self.classes = self.load_image_dataset(folder)
                self.input_size = 784
            else:
                messagebox.showerror("Error", "No folder selected!")
                return
        else:
            file = filedialog.askopenfilename(title="Select Text Dataset CSV", filetypes=[("CSV files", "*.csv")])
            if file:
                X, y, self.classes = self.load_text_dataset(file)
                self.input_size = X.shape[1] if X is not None else 0
            else:
                messagebox.showerror("Error", "No file selected!")
                return

        if X is not None and y is not None and len(X) > 0 and len(y) > 0:
            enc = OneHotEncoder(sparse_output=False)
            y_onehot = enc.fit_transform(y.reshape(-1, 1))
            # Improved architecture: 2 hidden layers
            self.nn = NeuralNetwork(layers=[self.input_size, 256, 128, len(self.classes)])
            self.nn.train(X, y_onehot, learning_rate=0.05, epochs=500, batch_size=64)  # Adjusted parameters
            # Evaluate on training data
            pred, probs = self.nn.predict(X[:10])
            print("Sample predictions on training data:", pred)
            print("Actual labels:", y[:10])
            messagebox.showinfo("Training Complete", "Model trained successfully!")
            self.show_recognition_page()
        else:
            messagebox.showerror("Error", "Failed to load dataset or dataset is empty!")

    def load_image_dataset(self, folder):
        X, y = [], []
        self.classes = sorted([d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))])
        if not self.classes:
            return None, None, None
        for idx, class_name in enumerate(self.classes):
            class_path = os.path.join(folder, class_name)
            for img_name in os.listdir(class_path):
                img_path = os.path.join(class_path, img_name)
                try:
                    img = Image.open(img_path).convert('L').resize((28, 28))
                    X.append(np.array(img).flatten() / 255.0)
                    y.append(idx)
                except:
                    continue
        X = np.array(X)
        y = np.array(y)
        if len(X) == 0 or len(y) == 0:
            return None, None, None
        return X, y, self.classes

    def load_text_dataset(self, file):
        try:
            data = np.genfromtxt(file, delimiter=',', skip_header=1)
            X = data[:, :-1]
            y = data[:, -1].astype(int)
            self.classes = np.unique(y).astype(str).tolist()
            return X, y, self.classes
        except:
            return None, None, None

    def show_recognition_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Recognition Page").pack(pady=5)
        tk.Label(self.root, text="Select an input to recognize:").pack()
        tk.Button(self.root, text="Choose Image/Text File", command=self.recognize_input).pack(pady=10)
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_dataset_page).pack(pady=5)

    def recognize_input(self):
        if self.data_type.get() == "image":
            file = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
            if file:
                img = Image.open(file).convert('L').resize((28, 28))
                X = np.array(img).flatten() / 255.0
                pred, probs = self.nn.predict(X.reshape(1, -1))
                confidence = np.max(probs) * 100
                self.result_label.config(text=f"Predicted: {self.classes[pred[0]]} (Confidence: {confidence:.2f}%)")
                print(f"Prediction probabilities: {probs}")
        else:
            file = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text files", "*.txt *.csv")])
            if file:
                X = np.genfromtxt(file, delimiter=',')
                pred, probs = self.nn.predict(X.reshape(1, -1))
                confidence = np.max(probs) * 100
                self.result_label.config(text=f"Predicted: {self.classes[pred[0]]} (Confidence: {confidence:.2f}%)")
                print(f"Prediction probabilities: {probs}")

def start_ui():
    NeuralUI()

if __name__ == "__main__":
    start_ui()