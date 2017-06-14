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

## importX.py
The importing scripts all do roughtly the same: import a csv, clean a few labels if needed.

Maybe more importantly, a few methods for quick analysis and check on data were declared in this import files (for agility during the early stages of development). Each will be shortly explained bellow:

- **getLabels(data, label)**: return all values data a gien label assume. Made to work on the data and target sets.
  - getLabels(san_data, 'source') -> ['NaN', 'Desktop', 'Mobile']

- **findWith(data, value, n)**: return a list of the n first indexes of the entries that contain a given value. After that, you can check each entry if you want to get some sort of information on when or how that information is present on a given data entry.
  - findWith(san_data, 'pid', 3) -> [1000000, 1000010, 1000200]
  
  
  
