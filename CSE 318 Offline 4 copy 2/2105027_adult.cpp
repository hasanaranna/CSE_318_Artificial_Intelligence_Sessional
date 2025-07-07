#include "2105027_decision_tree.hpp"

int main(int argc, char *argv[])
{
    ofstream logFile("decision_tree_log.txt");
    string criterion;
    int max_depth;

    if (argc != 3)
    {
        cout << "Error: Invalid number of arguments." << endl;
        cout << "Usage: ./decision_tree <criterion> <max_depth>" << endl;
        return 1;
    }
    else
    {
        criterion = argv[1];
        max_depth = stoi(argv[2]);
    }

    if (max_depth == 0)
    {
        max_depth = 1000; // Default max depth if 0 is provided
    }

    // Read data from CSV file
    string filename = "./Datasets/adult.csv";

    vector<vector<string>> initialDataSet = readCSV(filename);

    // remove third column from the dataset
    for (auto &row : initialDataSet)
    {
        if (row.size() > 3)
        {
            row.erase(row.begin() + 2); // Removed the third column (index 2)
        }
    }

    double averageAccuracy = 0.0;
    for (int i = 0; i < 20; i++)
    {
        vector<vector<string>> fullDataSet = initialDataSet; // Copy the initial dataset for each iteration

        int totalRows = fullDataSet.size();
        int trainingSize = static_cast<int>(totalRows * 0.8);
        int testingSize = totalRows - trainingSize;
        vector<vector<string>> trainingDataSet;
        vector<vector<string>> testingDataSet;
        trainingDataSet.clear();
        testingDataSet.clear(); 

        trainingDataSet.assign(fullDataSet.begin(), fullDataSet.begin() + trainingSize);
        testingDataSet.assign(fullDataSet.begin() + trainingSize, fullDataSet.end());

        // Build the decision tree
        Node *root = buildDecisionTree(trainingDataSet, criterion, 0, max_depth);

        // Testing the decision tree with the testing dataset
        int correctGuesses = 0;
        int totalGuesses = testingDataSet.size();
        for (const auto &row : testingDataSet)
        {
            Node *currentNode = root;
            while (!currentNode->children.empty())
            {
                bool found = false;
                for (Node *child : currentNode->children)
                {
                    if (isIntegerOrFloat(row[currentNode->featureIndex])) // Numeric feature
                    {
                        double featureValue = stod(row[currentNode->featureIndex]);
                        if (child->value.find("<=") != string::npos)
                        {
                            double threshold = stod(child->value.substr(2));
                            if (featureValue <= threshold)
                            {
                                currentNode = child;
                                found = true;
                                break;
                            }
                        }
                        else if (child->value.find(">") != string::npos)
                        {
                            double threshold = stod(child->value.substr(1));
                            if (featureValue > threshold)
                            {
                                currentNode = child;
                                found = true;
                                break;
                            }
                        }
                    }
                    else // Categorical feature
                    {
                        if (child->value == row[currentNode->featureIndex])
                        {
                            currentNode = child;
                            found = true;
                            break;
                        }
                    }
                }
                if (!found)
                {
                    break; // No matching child found
                }
            }

            if (currentNode->label == row.back()) // Compared with the actual label
            {
                correctGuesses++;
            }
        }
        double accuracy = static_cast<double>(correctGuesses) / totalGuesses * 100.0;
        averageAccuracy += accuracy;
    }

    averageAccuracy /= 20.0; 
    cout << "Average Accuracy over 20 iterations: " << averageAccuracy << "%" << endl;

    return 0;
}