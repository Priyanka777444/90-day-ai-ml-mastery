#imports
import numpy as np
import matplotlib.pyplot as plt

#generate data
np.random.seed(42)
cluster1 = np.random.randn(50, 2 )+[2,2]
cluster2 = np.random.randn(50, 2 )+[8,8]
cluster3 = np.random.randn(50, 2 )+[2,8]

X = np.vstack([cluster1, cluster2, cluster3])

#initilize centroid
def ini_centroid(X,k):
    indices = np.random.choice(len(X), k, replace = False)
    return X[indices]

#assign cluster
def assign_cluster(X, centroid):
    dist = np.array([
        np.sqrt(np.sum((X - cent)**2, axis = 1))
        for cent in centroid
    ])
    return np.argmin(dist, axis =0)

#update centroid
def update_centroids(X, labels, k):
    new_cent = []
    for i in range(k):
        cluster_points = X[labels == i]
        new_cent.append(cluster_points.mean(axis=0))
    return np.array(new_cent)

#full k-means loop
def kmeans(X, k=3, max_iterations = 100):
    centroid = ini_centroid(X, k)
    for i in range(max_iterations):
        #assign each point near
        labels = assign_cluster(X, centroid)

        # move centroids to center of their cluster
        new_cent = update_centroids(X, labels, k)

        # check if converged (centroids stopped moving)
        if np.allclose(centroid, new_cent):
            print(f"Converged at iteration {i}")
            break
        centroid = new_cent

    return labels, centroid
    
# Plot Results

labels , centroid = kmeans(X,k=3)

colors = ['red', 'blue','green']
plt.figure(figsize=(8,6))

for i in range(3):
    cluster_points = X[labels == i]
    plt.scatter(cluster_points[:,0], cluster_points[:,1],
                color=colors[i], alpha =0.6, label = f'cluster{i+1}')

plt.scatter(centroid[:,0],centroid[:,0],
            color = 'black', marker = "*", s=300 , label='Centroids')

plt.title("KMEANS")
plt.legend()
plt.savefig("result.png")
plt.show()

print(f"\nFinal Centroids: ")
for i , c in enumerate(centroid):
    print(f"cluster{i+1}: ({c[0]:.2f}, {c[1]:.2f})")