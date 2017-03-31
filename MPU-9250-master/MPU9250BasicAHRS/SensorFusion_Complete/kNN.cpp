/*
  kNN.cpp - Library for running a K-nearest Neighbors.
  Created by Brian Krentz, March 18, 2017.
*/

#include "Arduino.h"
#include "kNN.h"

kNN::kNN()
{ 
  k = 1;
}

int kNN::run(int* test_p, float* test_o)
{
  return 10*pose_kNN(test_p) + orient_kNN(test_o);
}

int kNN::pose_kNN(int* test)
{
  // Measure distances to all training data points
  int distances[20] = {0}; // 20 = 5 datapoints for each 4 poses
  int idx[20] = {15}; // label distances as gestures
  for (int j=0; j<5; j++){  // iterate through each data point
    for (int l=0; l<5; l++){  // iterate through each vector
      distances[l] += sq(test[j] - pose0[l][j]);
      distances[l+5] += sq(test[j] - pose1[l][j]);
      distances[l+10] += sq(test[j] - pose2[l][j]);
      distances[l+15] += sq(test[j] - pose3[l][j]);
    }
    idx[j] = 0;
    idx[j+5] = 1;
    idx[j+10] = 2;
    idx[j+15] = 3;
  }
  
  // Choose closest k distances
  int closest[1] = {10000000};
  int idx2[1] = {15};
  for (int i=0; i<20; i++){
    for (int j=0; j<1; j++){
      if (distances[i] < closest[j]){
        closest[j] = distances[i];
        idx2[j] = idx[i];
        break;
      }
    }
  }

  // Choose Gesture
  int maxPose=0;
  int modes[4] = {0};
  for (int i=0;i<1;i++){
    modes[idx2[i]] += 1;
  }
  for (int i=0;i<4;i++){
    if (modes[i] > maxPose){
      maxPose = i;
    }
  }
  return maxPose;
}

int kNN::orient_kNN(float* test)
{
  // Measure distances to all training data points
  int distances[10] = {0}; // store distances
  int idx[10] = {15}; // label distances as gestures
  
  // Iterate through each training datapoint
  for (int j=0; j<5; j++){
     // iterate through each vector
    for (int l=0; l<3; l++){
      distances[j] += sq(test[l] - orient0[j][l]);
      distances[j+5] += sq(test[l] - orient1[j][l]);
    }
    idx[j] = 0;
    idx[j+5] = 1;
  }

  // Choose closest k distances
  int closest[1] = {10000000};
  int idx2[1] = {15};
  for (int i=0; i<10; i++){
    for (int j=0; j<1; j++){
      if (distances[i] < closest[j]){
        closest[j] = distances[i];
        idx2[j] = idx[i];
        break;
      }
    }
  }

  // Choose Gesture
  int maxOrient=0;
  int modes[2] = {0};
  for (int i=0;i<k;i++){
    modes[idx2[i]] += 1;
  }
  for (int i=0;i<2;i++){
    if (modes[i] > maxOrient){
      maxOrient = i;
    }
  }

  return maxOrient;
}