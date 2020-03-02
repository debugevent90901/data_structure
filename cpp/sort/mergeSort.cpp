#include <iostream>
#include <vector>
#include <limits>
using namespace std;

template <typename T>
void merge(vector<T> &Array, int front, int mid, int end)
{
    vector<T> LeftSubArray(Array.begin() + front, Array.begin() + mid + 1);
    vector<T> RightSubArray(Array.begin() + mid + 1, Array.begin() + end + 1);
    int idxLeft = 0, idxRight = 0;
    LeftSubArray.insert(LeftSubArray.end(), numeric_limits<int>::max());
    RightSubArray.insert(RightSubArray.end(), numeric_limits<int>::max());
    for (int i = front; i <= end; i++)
    {
        if (LeftSubArray[idxLeft] < RightSubArray[idxRight])
        {
            Array[i] = LeftSubArray[idxLeft];
            idxLeft++;
        }
        else
        {
            Array[i] = RightSubArray[idxRight];
            idxRight++;
        }
    }
}

template <typename T>
void mergeSort(vector<T> &Array, int front, int end)
{
    if (front >= end)
        return;
    int mid = front + (end - front) / 2;
    mergeSort(Array, front, mid);
    mergeSort(Array, mid + 1, end);
    merge(Array, front, mid, end);
}

int main()
{
    vector<int> iarr = {61, 17, 29, 22, 34, 60, 72, 21, 50, 1, 62};
    mergeSort(iarr, 0, iarr.size() - 1);
    for (int i = 0; i < iarr.size(); i++)
        cout << iarr[i] << ' ';
    cout << endl;

    vector<double> darr = {17.5, 19.1, 0.6, 1.9, 10.5, 12.4, 3.8, 19.7, 1.5, 25.4, 28.6, 4.4, 23.8, 5.4};
    mergeSort(darr, 0, darr.size() - 1);
    for (int i = 0; i < darr.size(); i++)
        cout << darr[i] << ' ' << endl;
    return 0;
}