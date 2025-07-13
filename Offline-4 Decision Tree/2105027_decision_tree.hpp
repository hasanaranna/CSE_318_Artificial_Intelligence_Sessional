#ifndef DECISION_TREE_HPP
#define DECISION_TREE_HPP

#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <sstream>
#include <map>
#include <set>
#include <regex>
#include <algorithm>
#include <random>
#include <fstream>

using namespace std;

double globalThreshold = 0.0; // Global threshold variable

// Structure to represent a node in the decision tree
struct Node
{
    int featureIndex;        // Index of the feature used for splitting
    string value;            // Value of the feature
    vector<Node *> children; // Children nodes
    string label;            // Class label if it's a leaf node
    int depth;               // Depth of the node in the tree
    Node(int fIndex, string v) : featureIndex(fIndex), value(v), label("") {}
};

bool isIntegerOrFloat(const string& str) {
    regex pattern(R"(^[-+]?\d*\.?\d+$)");
    return regex_match(str, pattern);
}

// Function to calculate entropy of a dataset
double calculateEntropy(const vector<vector<string>> &data)
{
    map<string, int> classCounts;
    int totalRows = data.size();
    int targetIndex = data[0].size() - 1;

    for (const auto &row : data)
    {
        if (targetIndex < row.size())
        {
            classCounts[row[targetIndex]]++;
        }
    }
    double entropy = 0.0;
    // Calculated entropy using the formula: -sum(p * log2(p))
    for (const auto &pair : classCounts)
    {
        double p = static_cast<double>(pair.second) / totalRows;
        if (p > 0)
        {
            entropy -= p * log2(p);
        }
    }
    return entropy;
}

// Function to calculate information gain
double calculateInformationGain(const vector<vector<string>> &data, int featureIndex)
{
    map<string, vector<vector<string>>> subsets;
    int targetIndex = data[0].size() - 1;
    double totalEntropy = calculateEntropy(data);

    int totalRows = data.size();
    // Split data into subsets based on the feature value
    for (const auto &row : data)
    {
        if (featureIndex < row.size())
        {
            subsets[row[featureIndex]].push_back(row);
        }
    }
    double weightedEntropy = 0.0;
    // Calculated weighted entropy for each subset
    for (const auto &pair : subsets)
    {
        double subsetEntropy = calculateEntropy(pair.second);
        double subsetProbability = static_cast<double>(pair.second.size()) / totalRows;
        weightedEntropy += subsetProbability * subsetEntropy;
    }

    return totalEntropy - weightedEntropy;
}

// Function to calculate Intrinsic Value
double calculateIntrinsicValue(const vector<vector<string>> &data, int featureIndex)
{
    map<string, int> valueCounts;
    int totalRows = data.size();
    // Count occurrences of each feature value
    for (const auto &row : data)
    {
        if (featureIndex < row.size())
        {
            valueCounts[row[featureIndex]]++;
        }
    }
    double intrinsicValue = 0.0;
    // Calculated intrinsic value using the formula: -sum(p * log2(p))
    for (const auto &pair : valueCounts)
    {
        double p = static_cast<double>(pair.second) / totalRows;
        if (p > 0)
        {
            intrinsicValue -= p * log2(p);
        }
    }
    return intrinsicValue;
}

// Function to calculate Gain Ratio
double calculateGainRatio(const vector<vector<string>> &data, int featureIndex)
{
    double informationGain = calculateInformationGain(data, featureIndex);
    double intrinsicValue = calculateIntrinsicValue(data, featureIndex);

    // Avoid division by zero
    if (intrinsicValue == 0)
    {
        return 0.0;
    }

    // Gain Ratio = Information Gain / Intrinsic Value
    return informationGain / intrinsicValue;
}

// Function to calculate Normalized Weighted Information Gain
double calculateNWIG(const vector<vector<string>> &data, int featureIndex)
{
    int k;                       // Number of unique values for the feature
    int totalRows = data.size(); // |S|
    vector<string> uniqueValues;

    // unique values for the feature
    for (const auto &row : data)
    {
        if (featureIndex < row.size())
        {
            string value = row[featureIndex];
            if (find(uniqueValues.begin(), uniqueValues.end(), value) == uniqueValues.end())
            {
                uniqueValues.push_back(value);
            }
        }
    }
    k = uniqueValues.size();
    double informationGain = calculateInformationGain(data, featureIndex);
    double NWIG = 0.0;
    // Calculated Normalized Weighted Information Gain
    NWIG = (informationGain / log2(k + 1)) * (1 - ((log2(k - 1)) / totalRows));

    return NWIG;
}

// Function to Find the best Attribute to split on
int findBestAttribute(const vector<vector<string>> &data, const string &criterion)
{
    int bestAttributeIndex = -1;
    double bestValue = -1.0;
    int numAttributes = data[0].size() - 1; // Excluded target variable

    double totalEntropy = calculateEntropy(data);

    for (int i = 0; i < numAttributes; i++)
    {
        bool isNumeric = true;
        if (isIntegerOrFloat(data[0][i]) == false)
        {
            isNumeric = false; 
        }

        if (isNumeric)
        {
            set<string> uniqueValues;
            for (const auto &row : data)
            {
                if (i < row.size())
                {
                    uniqueValues.insert(row[i]);
                }
            }

            // If the feature has only one unique value, skipped it
            if (uniqueValues.size() <= 1)
            {
                continue;
            }

            vector<string> sortedValues(uniqueValues.begin(), uniqueValues.end());
            vector<vector<string>> leftSubset, rightSubset;
            double bestSplitValue = 0.0;
            double bestThreshold = 0.0; 
            double bestGain = -1.0;
            // Iterated through the sorted unique values to find the best split
            for (size_t j = 0; j < sortedValues.size() - 1; j++)
            {
                bestSplitValue = (stod(sortedValues[j]) + stod(sortedValues[j + 1])) / 2.0; // Midpoint for split
                leftSubset.clear();
                rightSubset.clear();
                // Split the data into left and right subsets based on the split value
                for (const auto &row : data)
                {
                    if (i < row.size())
                    {
                        if (stod(row[i]) <= bestSplitValue)
                        {
                            leftSubset.push_back(row);
                        }
                        else
                        {
                            rightSubset.push_back(row);
                        }
                    }
                }
                if (leftSubset.empty() || rightSubset.empty())
                {
                    continue; // Skip if any subset is empty
                }

                // Calculate Information Gain for the split
                double leftEntropy = calculateEntropy(leftSubset);
                double rightEntropy = calculateEntropy(rightSubset);
                double weightedEntropy = (static_cast<double>(leftSubset.size()) / data.size()) * leftEntropy +
                                         (static_cast<double>(rightSubset.size()) / data.size()) * rightEntropy;
                double informationGain = totalEntropy - weightedEntropy;

                if (criterion == "GR")
                {
                    // calculation of Intrinsic value
                    double intrinsicValue = - (static_cast<double>(leftSubset.size()) / data.size()) * log2(static_cast<double>(leftSubset.size()) / data.size()) -
                                            (static_cast<double>(rightSubset.size()) / data.size()) * log2(static_cast<double>(rightSubset.size()) / data.size());
                    // Avoid division by zero
                    if (intrinsicValue == 0)
                    {
                        continue; // Skip if intrinsic value is zero
                    }

                    double gainRatio = informationGain / intrinsicValue;
                    informationGain = gainRatio; // used gain ratio instead of information gain
                }
                else if (criterion == "NWIG")
                {
                    int k = uniqueValues.size();
                    // calculation of Normalized Weighted Information Gain
                    double nwig = (informationGain / log2(k + 1)) * (1 - (log2(k - 1) / data.size()));
                    informationGain = nwig; // used Normalized Weighted Information Gain instead of information gain
                }

                // Updated best gain and split value if current gain is better
                if (informationGain > bestGain)
                {
                    bestGain = informationGain;
                    bestThreshold = bestSplitValue;
                }
            }
            // If no valid split was found, continue to the next attribute
            if (bestGain <= 0)
            {
                continue;
            }
            if (bestGain > bestValue)
            {
                bestValue = bestGain;
                bestAttributeIndex = i;
                globalThreshold = bestThreshold; // Update global threshold
            }
        }
        else
        {
            double ratio = 0.0;
            if (criterion == "IG")
            {
                ratio = calculateInformationGain(data, i);
            }
            else if (criterion == "GR")
            {
                ratio = calculateGainRatio(data, i);
            }
            else if (criterion == "NWIG")
            {
                ratio = calculateNWIG(data, i);
            }

            if (ratio > bestValue)
            {
                bestValue = ratio;
                bestAttributeIndex = i;
            }
        }
    }

    if (bestValue <= 0)
    {
        // If no attribute provides a positive gain, return -1
        return -1;
    }
    return bestAttributeIndex;
}

// building the decision tree recursively
Node *buildDecisionTree(const vector<vector<string>> &data, const string &criterion, int currentDepth, int maxDepth)
{
    // Base case: if all rows have the same class label, returning a leaf node
    map<string, int> classCounts;
    for (const auto &row : data)
    {
        classCounts[row.back()]++;
    }

    if (classCounts.size() == 1 || currentDepth >= maxDepth)
    {
        Node *leafNode = new Node(-1, "");

        // Find the most frequent class
        string mostFrequentClass = classCounts.begin()->first;
        int maxCount = classCounts.begin()->second;
        for (const auto &pair : classCounts)
        {
            if (pair.second > maxCount)
            {
                maxCount = pair.second;
                mostFrequentClass = pair.first;
            }
        }
        leafNode->label = mostFrequentClass; // Assign the most frequent class label
        leafNode->depth = currentDepth;
        return leafNode;
    }

    // Find the best attribute to split on
    int bestAttributeIndex = findBestAttribute(data, criterion);
    if (bestAttributeIndex == -1)
    {
        Node *leafNode = new Node(-1, "");

        // Find the most frequent class
        string mostFrequentClass = classCounts.begin()->first;
        int maxCount = classCounts.begin()->second;
        for (const auto &pair : classCounts)
        {
            if (pair.second > maxCount)
            {
                maxCount = pair.second;
                mostFrequentClass = pair.first;
            }
        }
        leafNode->label = mostFrequentClass; // Assign the most frequent class label
        leafNode->depth = currentDepth;

        return leafNode;
    }

    Node *node = new Node(bestAttributeIndex, "");
    node->depth = currentDepth;

    map<string, vector<vector<string>>> subsets;
    if (isIntegerOrFloat(data[0][bestAttributeIndex]))
    {
        double localThreshold = globalThreshold; // Use the global threshold for numeric attributes
        globalThreshold = 0;                     // Reset global threshold for next use

        for (const auto &row : data)
        {
            if (bestAttributeIndex < row.size())
            {
                if (stod(row[bestAttributeIndex]) <= localThreshold)
                {
                    subsets["<=" + to_string(localThreshold)].push_back(row);
                }
                else
                {
                    subsets[">" + to_string(localThreshold)].push_back(row);
                }
            }
        }
    }
    else
    {
        // For categorical attributes, split based on unique values
        for (const auto &row : data)
        {
            if (bestAttributeIndex < row.size())
            {
                subsets[row[bestAttributeIndex]].push_back(row);
            }
        }
    }

    // Recursively build child nodes
    for (const auto &pair : subsets)
    {
        Node *childNode = buildDecisionTree(pair.second, criterion, currentDepth + 1, maxDepth);
        childNode->value = pair.first;
        node->children.push_back(childNode);
    }

    return node;
}

// Function to split a string by delimiter
vector<string> split(const string &str, char delimiter)
{
    vector<string> tokens;
    stringstream ss(str);
    string token;
    while (getline(ss, token, delimiter))
    {
        tokens.push_back(token);
    }
    return tokens;
}

// Function to read CSV file
vector<vector<string>> readCSV(const string &filename)
{
    vector<vector<string>> data;
    ifstream file(filename);

    if (!file.is_open())
    {
        cerr << "Error: Could not open file " << filename << endl;
        return data;
    }

    string line;
    while (getline(file, line))
    {
        if (!line.empty())
        {
            vector<string> row = split(line, ',');
            // Remove any trailing whitespace or carriage returns
            for (auto &cell : row)
            {
                while (!cell.empty() && (cell.back() == '\r' || cell.back() == ' '))
                {
                    cell.pop_back();
                }
            }
            data.push_back(row);
        }
    }

    file.close();
    return data;
}

// Function to count total number of nodes in decision tree
int countNodes(Node *node)
{
    if (node == nullptr)
    {
        return 0;
    }
    int count = 1; 
    for (Node *child : node->children)
    {
        count += countNodes(child); 
    }
    return count;
}

// Function to measure the depth of the decision tree
int measureDepth(Node *node)
{
    if (node == nullptr)
    {
        return 0;
    }
    int maxDepth = node->depth; 
    for (Node *child : node->children)
    {
        maxDepth = max(maxDepth, measureDepth(child)); 
    }
    return maxDepth;
}

#endif // DECISION_TREE_HPP