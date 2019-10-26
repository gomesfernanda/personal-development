# Summary for the book "Feature Engineering for Machine Learning"
[(Book on O'Reilly)](http://shop.oreilly.com/product/0636920049081.do)

Chapters:

- [X] [1. The Machine Learning Pipeline](#chapter-1---the-machine-learning-pipeline)
- [X] [2. Fancy Tricks with Simple Numbers](#chapter-2---fancy-tricks-with-simple-numbers)
- [ ] 3. Text Data: Flattening, Filtering, and Chunking
- [ ] 4. The Effects of Feature Scaling: From Bag-of-Words to Tf-Idf
- [ ] 5. Categorical Variables: Counting Eggs in the Age of Robotic Chickens
- [ ] 6. Dimensionality Reduction: Squashing the Data Pancake with PCA
- [ ] 7. Nonlinear Featurization via K-Means Model Stacking
- [ ] 8. Automating the Featurizer: Image Feature Extraction and Deep Learning
- [ ] 9. Back to the Feature: Building an Academic Paper Recommender

## Chapter 1 - The Machine Learning Pipeline

- Data: observations of real-world phenomena.
  - Each piece of data provides a small window into a limited aspect of reality, and the collection of them gives us a messy picture of the whole.
- *Wrong* data is the result of a mistake in measurement.
- *Redundant* data contains multiple aspects that convey exactly the same information.
- *Missing* data is when some data points are not present.
- A *mathematical model* of data describes the relationships between different aspects of data.
- *Mathematical formulas* relate numeric quatities to each other.
- A *feature* is a numeric representation of raw data.
  
![workflow](https://i.imgur.com/6OeZAyB.png)

## Chapter 2 - Fancy Tricks with Simple Numbers

- Good features should not only represent salient aspects of the data, but also conform to the assumptions of the model.
- Important aspects to notice on your numeric features:
  - Does the magnitude matters:
    - It's particularly important for automatically accrued numbers such as counts.
  - Scale of features: what are the largest and smallest values?
  - Distribution of numeric features: distribution summarizes the probability of taking on a particular value.
  - Sometimes multiple features can be composed together into more complex features.
  
### Scalars, vectors and spaces

- A single numeric feature is a *scalar*.
- An ordered list of scalars is a *vector*.
- Vectors sit within a *vector space*.
- In the world of data, an abstract vector and its feature dimension take on actual meaning. For instance, a vector can represent a person's preference for songs. Each song is a feature. where a value of 1 is equivalent to a thumbs up, and -1 a thumbs down.

### Dealing with counts

- When data can be produced at high volumes and velocity (case of counts), it's very likely to contain a few extreme values.
- It's a good idea to check the scale and determine whether to keep the data as raw numbers or work on them.

#### Binarization
- Clip all counts greater that X (number to be defined by the you) to 1.
  - This works particularly good for user preference, for example: if you're counting how many times a user listened to a song, and they listened to more than 1, you can say that count > 1 = user likes the song.

```python
>>> import pandas as pd
>>> listen_count = pd.read_csv('millionsong/train_triplets.txt.zip', header=None, delimiter='\t')
# The table contains user-song-count triplets. Only nonzero counts are
# included. Hence, to binarize the count, we just need to set the entire
# count column to 1
>>> listen_count[2] = 1
```

#### Quantizatiion or binning

- Raw counts that span several orders of magnitude can be problematic (for example in linear models or unsupervised learning).
- Quantizing: group the counts into bins, and get rid of the actual count values.
- You can quantize through:
  - Fixed width binning: each bin contains a specific numeric range.
    - Your bins ranges should be suited to your data (custom range according to age? powers of 10? depends on what you're dealing with)
  - Quantile binning: are bins that divide the data into equal portions.
    - Suitable for when you have gaps in the counts with no data.

#### Log Transformation

- Taking the logarithm of the count to map the data to exponential-width bins.
- It's a powerful tool for dealing with positive numbers with a heavy tailed distribution.

#### Power Transforms

- The log transform is a specific example of a family of transformations known as *power transformations*.
- In statistical terms, these are *variance-stabilizing transformations*.
- Power transformations change the distribution of the variable so that the variance is no longer dependent on the mean.
- Example: Box-Cox transform.

### Feature scaling or normalization

#### Min-max scaling

- Min-max scaling squeezes (or stretches) all feature values to be within the range of [0, 1].

#### Standardization (variance scaling)

- It subtracts off the mean of the feature (over all data points) and divides by the variance.
- The resulting scaled feature has a mean of 0 and a variance of 1.

#### $ℓ^2$ normalization

- Technique that normalizes (divide) the original feature value by what's known as the $ℓ^2$ norm, also known as the Euclidean norm.
  
No matter the scaling method, feature scaling always divides the feature by a constant (known as *normalization constant*). Therefore, it does **not**s change the shape of the single-feature distribution.

### Interaction features

- A simple pairwise *interaction feature* is the product of two features.
- A simple linear model uses a linear combination of the individual input features to predict the outcome.
- Interaction features are very simple to formulate, but they are very expensive to use.
- The training and scoring time of a linear model with pairwise interaction features would go from $O(n)$ to $O(n^2)$, where $n$ is the number of singleton features.
- Ways to deal with this problem:
  - Perform feature selection on top of all interaction features.
  - Craft a smaller number of complex features more carefully.

### Feature selection

- Feature selection techniques prune away nonuseful features in order to reduce complexity of the resulting model.
- They fall into 3 classes:
- *Filtering*:
  - Remove features that are unlikely to be useful for the model.
  - Much cheaper than Wrapper methods, but they do not take into account the model employed.
- *Wrapper methods*:
  - Allow to try out subset of features, but are expensive.
  - Treats the model as a black box that provides a quality score of a proposed subset of features.
- *Embedded methods*:
  - Perform feature selection as part of the model training process.
  - For example, decision trees.