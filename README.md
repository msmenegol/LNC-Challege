# LNC-Challenge
Repo with the solution for the 2017 Linx-Nemu-Chaordic Data Science Challenge.

The project was run on Python 3.5.2. It uses no external modules, with exception to **trainNN.py**, that uses numpy and TensorFlow.

Files are not 100% clean. There are commented lines of code and methods are not optimized. Please ignore sloppiness.

## How does it work tl;dr
1. First, all the csv files are imported and the names of the labels cleaned ('{"pid:",' -> 'pid:'). This is done on the **"import" scripts**.

2. Then, a few features to be used on a neural network are created:

- Source: [desktop? mobile?]
- Page_type: [cart? checkout? search? category? subcategory? confirm? home? brand? other? product?]
- Purchase?
- Product_index

  This is done to each batapoint and then an average for all data points for each user is done. This will later become the input o the NN for each user. This is done on **processData.py**.

3. The **trainNN.py** script splits the data-set into training and test-set (70/30). TensorFlow is used to create a 3-layered neural network (input + hl1 + hl2), train it, validate it, and then run it on the target data-set. The results are saved on **"deliverable.csv"**.

## importX.py
The importing scripts all do roughtly the same: import a csv, clean a few labels if needed. **importCat.py** imports the catalog, **importData.py** imports the data file, **importTargets.py** imports the targets.

Maybe more importantly, a few methods for quick analysis and check on data were declared in this import files (for agility during the early stages of development). The first 3 are declared on **importData.py**, the last one is on **importTargets.py** Each will be shortly explained bellow:

- **getLabels(data, label)**: returns all values data a gien label assume. Made to work on the data and target sets.
  - getLabels(san_data, 'source') -> ['NaN', 'Desktop', 'Mobile']

- **findWith(data, value, n)**: returns a list of the n first indexes of the entries that contain a given value. After that, you can check each entry if you want to get some sort of information on when or how that information is present on a given data entry.
  - findWith(san_data, 'pid', 3) -> [100000, 100001, 100020]
  
- **nOccur(data, label)**: returns the number of occurences of each value for a given label.
  - nOccur(san_data, 'source') -> {{'NaN' : 10000}, {'Desktop' : 20000}, {'Mobile' : 30000}}
  
- **check_all(ids, label, data, value)**: returns how many data-point with the given ids on the data-set have a given value, as well as a list of the ids that don't have said label.
  - check_all([100,200,173], 'source', san_data, 'NaN') -> (2, [173])
  
## processData.py
This script executes all the 3 import scripts. The first thing that it does is calculate a gender-based index for every product on the catalog based on what users bought on the data set. The index is an average of genders that bought said item. For example, if 3 men and 1 women bought item X, its index would be (3\*(0)+1\*(1))/4 = 0.25

After that, each data point (user-generated event on the database) is transformed into a vector containing:
- The used ID.
- A sumary of the event, of the format:
  - Source \<boolean\>: [desktop? mobile?]. A 'NaN' would become a [0 0]
  - Page_type \<boolean\>: [cart? checkout? search? category? subcategory? confirm? home? brand? other? product?]
  - Purchase? \<boolean\>: is this a purchase?
  - Product_Index \<-1:1\>: what was bought? What's its index?
- Gender \<boolean\>: 1 for female, 0 for male.

As this gets done, each entry is put in a dictionary, with the used ID as key. Then, a list is produced from the dictionary, with each entry being the aerage of all the navigation data of each user. This is what will be used for the training process.

A similar processing is done witht he targets, but without the gender attached at the end, obiously.

## trainNN.py
This builds, trains and validates the neural network. Then, it is used to run predictions on the target data and the results are saed on a csv file.
  



  
  
  
