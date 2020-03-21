#include <iostream>
using namespace std;

// without binary search
template <typename T>
void insertion_sort(T arr[], int len)
{
    for (int i = 1; i < len; i++)
    {
        T key = arr[i];
        int j = i - 1;
        while ((j >= 0) && (key < arr[j]))
        {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}


/*
// with binary search
template <typename T>
void insertion_sort(T arr[], int len)
{
    for (int i = 1; i < len; i++)
    {
        int left = 0, right = i - 1;
        T tmp = arr[i];
        while (left <= right)
        {
            int mid = left + (right - left) / 2;
            if (arr[mid] > tmp)
                right = mid - 1;
            else
                left = mid + 1;
        }
        for (int j = i - 1; j > right; j--)
            arr[j + 1] = arr[j];
        arr[left] = tmp;
    }
}
*/

int main()
{
    int arr[] = {61, 17, 29, 22, 34, 60, 72, 21, 50, 1, 62};
    int len = (int)sizeof(arr) / sizeof(*arr);
    insertion_sort(arr, len);
    for (int i = 0; i < len; i++)
        cout << arr[i] << ' ';
    cout << endl;
    float arrf[] = {17.5, 19.1, 0.6, 1.9, 10.5, 12.4, 3.8, 19.7, 1.5, 25.4, 28.6, 4.4, 23.8, 5.4};
    len = (float)sizeof(arrf) / sizeof(*arrf);
    insertion_sort(arrf, len);
    for (int i = 0; i < len; i++)
        cout << arrf[i] << ' ' << endl;
    return 0;
}