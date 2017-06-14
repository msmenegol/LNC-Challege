# LNC-Challenge
Repo with the solution for the 2017 Linx-Nemu-Chaordic Data Science Challenge

Files are not 100% clean. There is commented code and methods are not optimized. Please ignore sloppiness.

## How does it work tl;dr
1. First, all the csv files are imported and the names of the labels cleaned ('{"pid:",' -> 'pid:'). This is done on the **"import" scripts**.

2. Then, a few features to be used on a neural network are created:

- Source: [desktop? mobile?]
- Page_type: [cart? checkout? search? category? subcategory? confirm? home? brand? other? product?]
- Purchase?
- Product index

  This is done to each batapoint and then an average for all data points for each user is done. This will later become the input o the NN for each user. This is done on **processData.py**.

3. The **trainNN.py** script splits the data-set into training and test-set (70/30). TensorFlow is used to create a 3-layered neural network (input + hl1 + hl2), train it, validate it, and then run it on the target data-set. The results are saved on **"deliverable.csv"**.
