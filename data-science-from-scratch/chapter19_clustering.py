from chapter04_linearalgebra import squared_distances, vector_mean, distance
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
np.seterr(over='ignore')

class KMeans:
    """ Performs k-means clustering """

    def __init__(self, k):
        self.k = k                  # number of clusters
        self.means = None           # means of clusters

    def classify(self, input):
        """ Return the index of the cluster closest to the input """
        return min(range(self.k),
                   key = lambda i: squared_distances(input, self.means[i]))

    def train(self, inputs):

        # choose k random points as the initial means

        self.means = random.sample(inputs, self.k)
        assignments = None

        while True:
            # Find new assignments
            new_assignments = list(map(self.classify, inputs))

            # If no assignments have changed, we''e done
            if assignments == new_assignments:
                return

            # Otherwise keep the new assignments,
            assignments = new_assignments

            # And compute new means based on the new assignments
            for i in range(self.k):
                # find all the points assigned to a cluster i
                i_points = [p for p, a in zip(inputs, assignments) if a == i]
                # make sure i_points is not empty so don't divide by 0
                if i_points:
                    self.means[i] = vector_mean(i_points)

def squared_clustering_errors(inputs, k):
    """ Find the total squared error from k-means clustering the inputs """
    clusterer = KMeans(k)
    clusterer.train(inputs)
    means = clusterer.means
    assignments = map(clusterer.classify, inputs)

    return sum(squared_distances(input, means[cluster])
                                 for input, cluster in zip(inputs, assignments))

def recolor_image(input_file, k=5):
    img = mpimg.imread(input_file)
    pixels = [pixel for row in img for pixel in row]
    clusterer = KMeans(k)
    clusterer.train(pixels) # this might take a while

    def recolor(pixel):
        cluster = clusterer.classify(pixel) # index of the closest cluster
        return clusterer.means[cluster]     # mean of the closest cluster

    new_img = [[recolor(pixel) for pixel in row]
               for row in img]

    plt.imshow(new_img)
    plt.axis('off')
    plt.show()


###############################
#                             #
#   HIERARCHICAL CLUSTERING   #
#                             #
###############################


def is_leaf(cluster):
    """ A cluster is a leaf if it has length 1 """
    return len(cluster) == 1

def get_children(cluster):
    """ Returns the two children of this cluster if it's a merged cluster;
    raises an Exception if this is a leaf cluster"""
    if is_leaf(cluster):
        raise TypeError("a lea cluster has no children")
    else:
        return cluster[1]

def get_values(cluster):
    """ Returns the value in this cluster (if it's a leaf cluster)
    or all the values in the leaf clusters below it (if it's not) """
    if is_leaf(cluster):
        return cluster
    else:
        return [value
                for child in get_children(cluster)
                for value in get_values(child)]

def cluster_distance(cluster1, cluster2, distance_agg=min):
    """ Compute all te pairwise distances between cluster1 and cluster2
    and apply distance_agg to the resulting list"""
    return distance_agg([distance(input1, input2)
                         for input1 in get_values(cluster1)
                         for input2 in get_values(cluster2)])

def get_merge_order(cluster):
    if is_leaf(cluster):
        return float('inf')
    else:
        return cluster[0]           # merge_order is first element of 2 tuple

def bottom_up_cluster(inputs, distance_agg=min):
    distance_agg=max
    # start with every inut a leaf cluster / 1-tuple
    clusters = [(input,) for input in inputs]

    # as long as we have more than 1 cluster left...
    while len(clusters) > 1:
        # find the two closest clusters
        c1, c2 = min([(cluster1, cluster2)
                      for i, cluster1 in enumerate(clusters)
                      for cluster2 in clusters[:i]],
                     key=lambda p: cluster_distance(p[0], p[1], distance_agg))

        # remove them from the list of clusters
        clusters = [c for c in clusters if c != c1 and c != c2]

        # merge the, using merge_order = # of clusters left
        merged_cluster = (len(clusters), [c1, c2])

        # and add their merge
        clusters.append(merged_cluster)

    # when there's only one cluster left, return it
    return clusters[0]

def generate_clusters(base_cluster, num_clusters):
    #start with a list with just the base cluster
    clusters = [base_cluster]

    # as long as we don't have enough clusters yet...
    while len(clusters) < num_clusters:
        # choose the last-merged of our clusters
        next_cluster = min(clusters, key=get_merge_order)
        # remove it from the list
        clusters = [c for c in clusters if c != next_cluster]
        # and add its children to the list (i.e. unmerge it)
        clusters.extend(get_children(next_cluster))

    # once we have enough clusters
    return clusters

if __name__ == '__main__':

    inputs = [[-14,-5],[13,13],[20,23],[-19,-11],[-9,-16],[21,27],
              [-49,15],[26,13],[-46,5],[-34,-1],[11,15],[-49,0],[-22,-16],
              [19,28], [-12,-8],[-13,-19],[-41,8],[-11,-6],[-25,-9],[-18,-3]]
    x = [i[0] for i in inputs]
    y = [i[1] for i in inputs]

    meetups = 0
    recolor = 1
    bottom_up = 0

    if meetups == 1:

        random.seed()
        clusterer = KMeans(3)
        clusterer.train(inputs)
        clusterer_means = clusterer.means

        x_means = [round(i[0],0) for i in clusterer_means]
        y_means = [round(i[1],0) for i in clusterer_means]

        plt.figure(figsize=(8, 10))
        plt.subplot(2, 1, 1)
        inputs_plot = plt.scatter(x, y, marker='o', c='green')
        k_centroids = plt.scatter(x_means, y_means, marker='D', c='red')
        plt.xlabel("blocks east of city center")
        plt.ylabel("blocks north of city center")
        plt.title("User Locations -- 3 clusters")

        # Now plot fom 1 to len(inputs) clusters

        ks = range(1, len(inputs) + 1)
        errors = [squared_clustering_errors(inputs, k) for k in ks]

        plt.subplot(2, 1, 2)
        plt.plot(ks, errors)
        plt.xticks(ks)
        plt.xlabel("k")
        plt.ylabel("total squared error")
        plt.title("Total Error vs. # of Clusters")
        plt.tight_layout()
        plt.show()

    if recolor == 1:
        path_to_png_file = "to_recolor.jpg"
        recolor_image(path_to_png_file)

    if bottom_up == 1:
        leaf1 = ([10, 20], )      # to make a 1-tuple you need the trailing comma
        leaf2 = ([30, -15], )     # otherwise Python treats the parentheses as parentheses, not tuple

        merged = (1, [leaf1, leaf2])

        base_cluster = bottom_up_cluster(inputs)

        three_clusters = [get_values(cluster) for cluster in generate_clusters(base_cluster, 3)]

        for i, cluster, marker, color in zip([1, 2, 3],
                                             three_clusters,
                                             ['D', 'o', '*'],
                                             ['r', 'g', 'b']):
            xs, ys = zip(*cluster)      # magic unzipping trick
            plt.scatter(xs, ys, color=color, marker=marker)

            # put a number at the mean of the cluster
            x, y = vector_mean(cluster)
            plt.plot(x, y, marker='$' + str(i) + '$', color='black')

        plt.title("User Locations -- 3 Bottom-up Clusters, Min")
        plt.xlabel("blocks east of city center")
        plt.ylabel("blocks north of city center")
        plt.show()
