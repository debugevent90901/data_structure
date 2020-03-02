#include <iostream>
using namespace std;

template <typename T>
void quick_sort_recursive(T arr[], int start, int end)
{
    if (start >= end)
        return;
    T mid = arr[end];
    int left = start, right = end - 1;
    while (left < right)
    {
        while (arr[left] < mid && left < right)
            left++;
        while (arr[right] >= mid && left < right)
            right--;
        swap(arr[left], arr[right]);
    }
    if (arr[left] >= arr[end])
        swap(arr[left], arr[end]);
    else
        left++;
    quick_sort_recursive(arr, start, left - 1);
    quick_sort_recursive(arr, left + 1, end);
}

template <typename T>
void quickSort(T arr[], int len)
{
    quick_sort_recursive(arr, 0, len - 1);
}

int main()
{
    int arr[] = {13, 24, 8, 3, 27, 101, 15, 6, 8, 21};
    int len = (int)sizeof(arr) / sizeof(*arr);
    quickSort(arr, len);
    for (int i = 0; i < len; i++)
        cout << arr[i] << ' ';
    cout << endl;
    /*
    float arrf[] = {17.5, 19.1, 0.6, 1.9, 10.5, 12.4, 3.8, 19.7, 1.5, 25.4, 28.6, 4.4, 23.8, 5.4};
    len = (float)sizeof(arrf) / sizeof(*arrf);
    quickSort(arrf, len);
    for (int i = 0; i < len; i++)
        cout << arrf[i] << ' ' << endl;
    */
    return 0;
}