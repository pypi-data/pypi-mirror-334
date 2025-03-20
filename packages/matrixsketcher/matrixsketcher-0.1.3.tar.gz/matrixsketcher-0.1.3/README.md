# MatrixSketcher: Efficient Matrix Sketching for Large-Scale Computations

[![PyPI](https://img.shields.io/pypi/v/matrixsketcher?color=blue)](https://pypi.org/project/matrixsketcher/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/matrixsketcher.svg)](https://pypi.org/project/matrixsketcher/)
[![License](https://img.shields.io/github/license/luke-brosnan-cbc/matrixsketcher)](LICENSE)

MatrixSketcher is a high-performance Python library for **matrix sketching**, enabling scalable and memory-efficient approximations for large matrices. It provides a suite of randomized algorithms for **dimensionality reduction, kernel approximation, leverage score sampling, and compressed linear algebra.**

---

## 🚀 **What is Matrix Sketching? Why is it Useful?**
Matrix sketching is a technique used to **approximate large matrices with a much smaller representation**, making computations significantly **faster and more memory-efficient**.<br><br>

Instead of processing an entire large dataset, matrix sketching allows you to:
- **Reduce storage requirements** by keeping only a compressed form of the data.
- **Speed up machine learning and econometrics models** without losing key information.
- **Approximate costly transformations** like covariance matrices and kernel functions.<br><br>

### 🔥 **Where is Matrix Sketching Used?**
- **Machine Learning (ML)**: Speeding up PCA, kernel methods, and regression models.
- **Econometrics & Finance**: Handling massive datasets efficiently in regressions and covariance estimation.
- **Natural Language Processing (NLP)**: Compressing large word embedding matrices.
- **Graph & Network Analysis**: Speeding up computations on social networks, blockchain transactions, and recommendation system*.<br><br>


## 🏗 **How Do Different Sketching Methods Differ?**
Each method in MatrixSketcher serves a different purpose:
- **Leverage Score Sampling**: Smart sampling that keeps **important** data points.
- **CUR Decomposition**: Selects **actual rows and columns** for interpretability.
- **Bicriteria CUR**: Joint optimization of row and column selection for better reconstruction.
- **CountSketch**: Compresses matrices using hashing techniques.
- **Fast Walsh-Hadamard Transform (FWHT)**: Structured projections for efficient compression.<br><br>

---


## 🔢 **Core Algorithms and use cases**
  
### **1. CountSketch**
A **hashing-based** technique that efficiently compresses large matrices while preserving inner products.

**Use Cases:**
- Feature hashing in NLP (e.g., compressing word embeddings).
- Reducing dimensionality in large-scale regression.
- Fast feature engineering in high-dimensional datasets.

#### **Mathematical Formulation**
Given a matrix $X \in \mathbb{R}^{N \times P}$, we define:

1. A hash function: $h$: $[1,P] \to [1,D]$ which maps each column $j$ to a sketch bucket.
2. A sign function: $\sigma$: $[1,P] \to \{+1,-1 \}$ whichassigns each column a random sign.<br><br>

The **sketch matrix** $S$ is constructed as:

<div align="center"; margin: 0>

### $S_{j,h(j)} = \sigma(j), \quad S_{j,k} = 0 \quad \text{for } k \neq h(j)$

</div>

The **CountSketch transformation** is then:

<div align="center"; margin: 0>

### $X' = X S^T, \quad \text{where } X' \in \mathbb{R}^{N \times D}$

</div>


#### Why Does CountSketch Work?
CountSketch approximates **inner products** between vectors efficiently:

<div align="center"; margin: 0>

### $\langle x_i, x_j \rangle \approx \langle x_i S^T, x_j S^T \rangle$

</div>

Due to the randomized hashing mechanism, the **error introduced by CountSketch** is bounded by:

<div align="center"; margin: 0>

### $\mathbb{E} \left[ \| X - X S^T S \|_F^2 \right] \leq \frac{1}{D} \| X \|_F^2$

</div>

This means that increasing \( D \) **reduces the error** while keeping computations **efficient**.<br><br><br><br>
 

<details>
<summary>Example usage</summary>
<br>

## Function: ```countsketch(X, sketch_size, random_state=None, sparse_output=True)```

### Inputs & Explanation
#### ```X``` (array or sparse matrix):

- The input data matrix of shape (n, p), where n is the number of samples and p is the number of features.
- Can be dense (numpy array) or sparse (scipy.sparse).

#### ```sketch_size``` (int):

- The target dimensionality (d) of the sketch.
- The function will project the p original features into d hashed features (d < p for compression).

#### ```random_state``` (int, optional):

- Sets the seed for reproducibility.

#### ```sparse_output``` (bool, default=```True```):

- If True, constructs S as a sparse matrix for efficiency.
- If False, builds S as a dense array (slower for large p).

```python
import numpy as np
from matrixsketcher.countsketch import countsketch

# Create a large data matrix (1000 samples, 5000 features)
X = np.random.rand(1000, 5000)

# Apply CountSketch to reduce feature dimension to 500
X_sketch = countsketch(X, sketch_size=500, random_state=42)

print("Original shape:", X.shape)  # (1000, 5000)
print("Sketched shape:", X_sketch.shape)  # (1000, 500)
```

</details>

---


### **2. Leverage Score Sampling**
Leverage Score Sampling picks rows (or columns) with probabilities proportional to their importance in the SVD. This gives a better approximation than purely random selection.

**The method also supports**:

_Uniform sampling_: Rows (or columns) chosen randomly.

_Weighted sampling_: Probability proportional to row (or column) norms.

**Use Cases**:
- Efficient econometric model estimation with fewer data points.
- Faster large-scale ML by discarding low-importance rows.
- Spectral clustering and graph analytics on huge datasets.<br><br>


#### **Mathematical Formulation**
1️⃣ **Uniform Sampling (Random Selection):**

Columns and rows are selected randomly without weighting.<br><br>


2️⃣ **Leverage Score Sampling:**

**STEP 1:Compute a $k$-Rank Approximation of X using SVD**
<div align="center"; margin: 0>

### $X \in \mathbb{R}^{N \times P}, \quad X \approx {U_k  S_k  V_k}^T$

</div>

Where:
- $U \in \mathbb{R}^{N \times k}$ is the top k left singular vectors of $X$ (for row sampling).
- $S \in \mathbb{R}^{k \times k}$ is the Diagonal of top $k$ singular values of $X$.
- $V \in \mathbb{R}^{k \times P}$ is the top k right singular vectors of $X$ (for column sampling).

**STEP 2: Leverage Scores**

- For rows:
  - Each row $U_i$ in $U \in \mathbb{R}^{N \times k}$ is $k$-dimensional.
  - Probabilities ${p_i}^{(\text{row})}$ sum to 1 over $N$ rows.
  - Probability of choosing row $i$:

<div align="center"; margin: 0>

### $p_i^{(\text{row})} = \frac{\|\mathbf{U}_ {i,:}\|^2}{\sum_{i=1}^{N}\|\mathbf{U}_{i,:}\|^2}\quad\text{for } i=1,\dots,N.$

</div>

- For columns:
  - Each column $V_i$ in $V \in \mathbb{R}^{k \times P}$ is $k$-dimensional.
  - Probabilities ${p_j}^{(\text{col})}$ sum to 1 over $P$ columns.
  - Probability of choosing column $j$:

<div align="center"; margin: 0>

### $p_j^{(\text{column})} = \frac{\|\mathbf{V}_ {:,j}\|^2}{\sum_{j=1}^{P}\|\mathbf{V}_{:,j}\|^2}\quad\text{for } j=1,\dots,P.$

</div>

**STEP 3: Select $D_{row}$ or $D_{col}$**

- Row sampling: Draw $D_{row}$ indcices $\{{i_1},{i_2}, \dots\}$ w.r.t. $p_i^{(\text{row})}$
- Column sampling: Draw $D_{col}$ indcices $\{{j_1},{j_2}, \dots\}$ w.r.t. $p_j^{(\text{col})}$<br><br>

3️⃣ **Weighted Row Sampling:**

For weighted row sampling by norms

<div align="center"; margin: 0>

### $p_i = \frac{\|\mathbf{X}_ {i,:}\|^2}{\sum_{r=1}^{P}\|\mathbf{X}_{i,:}\|^2}$,

</div>

the dimension deatils are straightforward:
- $X_{i,:} \in \mathbb{R}^{P}$
- $\|\mathbf{X}_ {i,:}\|^2$ is a scalar for each of the N rows.<br><br><br><br>

<details>
<summary>Example usage</summary>
<br>

## Function: ```leverage_score_sampling(X, sample_size, rank=None, random_state=None, scale=True, sampling="leverage", axis=0)```

### Inputs & Explanation
#### ```X``` (array or sparse matrix):

- The input data matrix of shape (n, p), where n is the number of rows (samples) and p is the number of columns (features).
- Supports both dense (numpy array) and sparse (scipy.sparse) formats.

#### ```sample_size``` (int):

- The number of rows (if axis=0) or columns (if axis=1) to sample.

#### ```rank``` (int, optional):

- The rank used for SVD decomposition if sampling="leverage".
- If None, defaults to min(n, p).

#### ```random_state``` (int, optional):

- Sets the seed for reproducibility.

#### ```scale``` (bool, default=```True```):

- If True, scales the selected rows/columns by 1/sqrt(probability).
- Helps maintain unbiased estimates when performing leverage score sampling.

#### ```sampling``` (str, default=```"leverage"```):

- "leverage": Uses leverage scores computed via SVD.
- "uniform": Samples rows uniformly at random (only for axis=0).
- "weighted": Samples rows based on squared row norms (only for axis=0).

#### ```axis``` (int, default=```0```):

- 0: Sample rows.
- 1: Sample columns.
- Note: "uniform" and "weighted" sampling are only supported for rows (axis=0).


```python
import numpy as np
from matrixsketcher.leverage_score_sampling import leverage_score_sampling

# Create a large data matrix (1000 samples, 500 features)
X = np.random.rand(1000, 500)

# Sample 100 rows using leverage scores
X_sampled_rows = leverage_score_sampling(X, sample_size=100, sampling="leverage", axis=0, random_state=42)

# Sample 50 columns using leverage scores
X_sampled_cols = leverage_score_sampling(X, sample_size=50, sampling="leverage", axis=1, random_state=42)

print("Original shape:", X.shape)  # (1000, 500)
print("Sampled rows shape:", X_sampled_rows.shape)  # (100, 500)
print("Sampled columns shape:", X_sampled_cols.shape)  # (1000, 50)
```


</details>

---


### **3. CUR Decomposition (Interpretable Low-Rank Approximation)**
CUR selects actual rows and columns instead of abstract components (like SVD), making results more interpretable.

**Use Cases:**
- Feature selection in high-dimensional data.
- Recommendation systems (selecting key users/items).
- Econometrics (identifying important factors in large datasets).<br><br>


**Why does CUR use $W^{\dagger}$?**

- The inverse $W^{\dagger}$ corrects for correlations between those interactions, ensuring a better low-rank reconstruction.
- f you apply leverage score sampling separately to rows and columns, you do not get the interaction matrix $W^{\dagger}$,
- leading to a less structured approximation


#### **Mathematical Formulation**
Given a matrix $X \in \mathbb{R}^{N \times K}$, CUR approximates $X$ by:
<div align="center"; margin: 0>

### $X \approx C W^{\dagger} R$

</div>

Where:
- $C \in \mathbb{R}^{N \times D_{col}}$ is a selection of $D_{col}$ columns from $X$.
- $R \in \mathbb{R}^{D_{row} \times K}$ is a selection of $D_{row}$ rows from $X$.
- $W \in \mathbb{R}^{D_{row} \times D_{col}}$ is the core submatrix at the intersection of selected rows and columns.
- $W^{\dagger}$ is the pseudoinverse of $W$.

CUR ensures that the selected rows and columns preserve key structural information by using the intersection matrix $W$.<br><br>

#### **Column and Row Selection Methods**
MatrixSketcher
 provides two strategies:

1. **Leverage Score Sampling**:  
Select columns and rows based on statistical importance via the SVD of $X$ (as presented above).

1. **Uniform Sampling**:  
Select rows randomly, each with equal probability, and uses leverage scores to select columns.


<details>
<summary>Example usage</summary>
<br>

## Function: ```cur_decomposition(X, d_rows, d_cols, rank=None, random_state=None, sampling="uniform", regularization=0.0)```

### Inputs & Explanation
#### ```X``` (array or sparse matrix):

- The input matrix of shape (n, p), where n is the number of rows (samples) and p is the number of columns (features).
- Supports both dense (numpy array) and sparse (scipy.sparse) formats.

#### ```d_rows``` (int):

- The number of rows to select for the decomposition.

#### ```d_cols``` (int):

- The number of columns to select for the decomposition.

#### ```rank``` (int, optional):

- The rank used for leverage score computation during SVD.
- If None, defaults to min(n, p) - 1.

#### ```random_state``` (int, optional):

- Sets the seed for reproducibility.

#### ```sampling``` (str, default=```"uniform"```):

- "uniform": Selects rows uniformly at random.
- "leverage": Selects rows based on leverage scores from SVD.
- Note: Columns are always selected using leverage scores.

#### ```regularization``` (float, default=```0.0```):

- Adds a small diagonal value to W before computing its pseudoinverse.
- Helps prevent numerical instability when W is nearly singular.

```python
import numpy as np
from matrixsketcher.cur_decomposition import cur_decomposition

# Generate a random matrix (1000 x 500)
X = np.random.rand(1000, 500)

# Apply Bicriteria CUR selecting 50 rows, 40 columns, with rank 20
C, W, R = cur_decomposition(X, d_rows=50, d_cols=40, rank=20, random_state=42, sampling="leverage")

# Check output shapes
print("C shape:", C.shape)  # Expected: (1000, 40) → Selected columns
print("W shape:", W.shape)  # Expected: (50, 40)  → Intersection submatrix
print("R shape:", R.shape)  # Expected: (50, 500) → Selected rows
```

</details>

---

### **4. Bicriteria CUR (Joint Optimization for Rows & Columns)**

Bicriteria CUR **optimizes both row and column selection jointly**, balancing sampling quality and computational cost.  
This method provides **near-optimal guarantees** on the resulting low-rank approximation, ensuring that the selected rows and columns capture the global structure of \( X \).

#### **Use Cases**
- **Large-scale recommendation systems** where both user (row) and item (column) choices matter.
- **Data with strong row-column dependencies** (e.g., gene expression, adjacency matrices).
- **When you need a single step** to pick key rows and columns simultaneously.

#### **Mathematical Formulation**
Given $X \in \mathbb{R}^{N \times K}$, Bicriteria CUR selects:
- $d_{\text{rows}}$ rows and $d_{\text{cols}}$ columns
- Form the submatrix $W \in \mathbb{R}^{d_{\text{rows}} \times d_{\text{cols}}}$ at the intersection
- Then reconstruct:
  
<div align="center"; margin: 0>

### $X \approx C W^{\dagger} R$

</div>

where:
- $C \in \mathbb{R}^{N \times d_{\text{cols}}}$ are the chosen columns,
- $R \in \mathbb{R}^{d_{\text{rows}} \times K}$ are the chosen rows,
- $W^{\dagger}$ is the Moore-Penrose pseudoinverse of $W$.<br><br>

The **bicriteria** part comes from maximizing the “volume” or determinant of $W$ while keeping row/column choices minimal.

1️⃣ What Does "Maximizing Volume" Mean?

In matrix approximation, the volume of a subset of rows and columns is given by the determinant of the Gram matrix:

<div align="center"; margin: 0>

### $\text{Vol}(W) = \det(W^T W)$

</div>

where:


- $W \in \mathbb{R}^{d_{\text{rows}} \times d_{\text{cols}}}$ is the intersection of the selected rows and columns.

- $W^T W$ is the Gram matrix of the selected subset.

The determinant measures how well the selected rows/columns span the space.<br><br>

2️⃣ Objective: Maximizing Volume While Controlling Selection Size

The goal of Bicriteria CUR is to select row and column indices $S_r$ and $S_c$ such that:

<div align="center"; margin: 0>

### $(S_r^{\ast}, S_c^{\ast}) = \arg\max_{S_r, S_c} \det(W_{S_r, S_c}^T W_{S_r, S_c})$

</div>

Subject to:

<div align="center"; margin: 0>

### $|S_r| = d_{\text{rows}}, \quad |S_c| = d_{\text{cols}}$

</div>

where:

- $S_r$ and $S_c$ are index sets of selected rows and columns.

- $d_{\text{rows}} $ and $ d_{\text{cols}}$ control the approximation size.

Since computing the best $W$ directly is NP-hard, a greedy approximation is used.<br><br>

3️⃣ Greedy Row-Column Selection Strategy

1. Compute leverage scores for rows and columns using SVD.

2. Sample $d_{\text{rows}}$ rows and $d_{\text{cols}}$ columns.

3. Iteratively swap rows/columns to maximize $\det(W^T W)$.

4. Ensures that the determinant remains large for optimal reconstruction.<br><br>

4️⃣ Bounded Approximation Error Guarantee

Bicriteria CUR ensures provable near-optimal reconstruction compared to the best rank-$k$ approximation $X_k$:

<div align="center"; margin: 0>

### $\| X - C W^{\dagger} R \|_F \leq (1 + \epsilon) \| X - X_k \|_F$

</div>

where:

- $\epsilon$ is a small constant that depends on the number of selected rows and columns.

This guarantee ensures that **even with greedy selection**, we achieve a **near-optimal CUR decomposition**, making it an **efficient alternative** to full-rank SVD while preserving interpretability.<br><br><br><br>

<details>
<summary>Example usage</summary>
<br>

## Function: ```bicriteria_cur(X, d_rows, d_cols, rank=None, random_state=None, regularization=0.0, max_iter=6)```

### Inputs & Explanation
#### ```X``` (array or sparse matrix):

- The input matrix of shape (n, p), where n is the number of rows (samples) and p is the number of columns (features).
- Supports both dense (numpy array) and sparse (scipy.sparse) formats.

#### ```d_rows``` (int):

- The number of rows to select for the decomposition.

#### ```d_cols``` (int):

- The number of columns to select for the decomposition.

#### ```rank``` (int, optional):

- The rank used for leverage score computation during SVD.
- If None, defaults to min(n, p) - 1.

#### ```random_state``` (int, optional):

- Sets the seed for reproducibility.

#### ```regularization``` (float, default=```0.0```):

- Adds a small diagonal value to W before computing its pseudoinverse.
- Helps prevent numerical instability when W is nearly singular.

#### ```max_iter``` (int, default=```6```):
- Number of iterations for greedy row/column swapping.
- Higher values lead to better selection but increase runtime.

```python
import numpy as np
from matrixsketcher.bicriteria_cur import bicriteria_cur

# Generate a random matrix (1000 x 500)
X = np.random.rand(1000, 500)

# Apply Bicriteria CUR selecting 50 rows, 40 columns, with rank 20
C, W, R = bicriteria_cur(X, d_rows=50, d_cols=40, rank=20, random_state=42, max_iter=6)

# Check output shapes
print("C shape:", C.shape)  # Expected: (1000, 40) → Selected columns
print("W shape:", W.shape)  # Expected: (50, 40)  → Intersection submatrix
print("R shape:", R.shape)  # Expected: (50, 500) → Selected rows
```

</details>

---


### **5. Fast Walsh-Hadamard Transform (FWHT)**
The Fast Walsh-Hadamard Transform (FWHT) is a structured, deterministic transform that is similar to the Fast Fourier Transform (FFT) but operates over binary ±1 values instead of complex exponentials.

**Use Cases:**
- Accelerating High-Dimensional Regressions:

- Preconditioning Large Econometric Models:

- Fast Data Compression in ML Pipelines:


**Mathematical Formulation:**
The Walsh-Hadamard matrix of size $H_n$ is recursively defined as follows:

<div align="center"; margin: 0>

$$H_1 = \begin{bmatrix} 1 \end{bmatrix}$$

</div>

For $n = 2^k$ , the Hadamard matrix is built recursively:

<div align="center"; margin: 0>

$$H_{2n} =\begin{bmatrix} H_n & H_n \\\ H_n & -H_n \end{bmatrix}$$

</div>

Where:  
- $H_n$ is the Hadamard matrix of size $n$.  
- The recursive structure ensures fast computation in **$O(n \log n)$ time**, similar to FFT.  

#### **2️⃣ Applying FWHT to a Matrix $X$**
For a matrix $X \in \mathbb{R}^{N \times P}$, FWHT transforms each row as:

<div align="center"; margin: 0>

### $X' = H_N \cdot X$

</div>

where:
- $H_N$ is the Walsh-Hadamard matrix of size $N$, assuming $N$ is a power of 2.
- The transform preserves inner products up to a scaling factor.<br><br><br><br>

<details>
<summary>Example usage</summary>
<br>

## Function: ```fwht(X, random_state=None, pad_or_error="error")```

### Inputs & Explanation

#### ```X``` (array or sparse matrix):

- The input matrix of shape (n, p), where n is the number of rows (samples) and p is the number of columns (features).(must be a power of 2 for direct application).
- If X is a sparse matrix, it is first converted to a dense NumPy array.

#### ```random_state``` (int, optional):

- Sets the seed for reproducibility when generating random signs for the transformation.

#### ```pad_or_error``` (str, default=```"error"```):

- "error": Raises an error if N is not a power of 2.
- "pad": Zero-pads X so that N becomes the next power of 2.

```python
import numpy as np
from matrixsketcher.Fast_Walsh_Hadamard_Transform import fwht

# Create a random matrix with a power-of-2 number of rows
X = np.random.rand(1024, 50)

# Apply Fast Walsh-Hadamard Transform (FWHT)
X_fwht = fwht(X, pad_or_error="pad", random_state=42)

print("FWHT-transformed shape:", X_fwht.shape)  # Expected: (1024, 50)
```

</details>


## 🔧 **Installation**
To install MatrixSketcher, simply run:

```python
pip install matrixsketcher
```
