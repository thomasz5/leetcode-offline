Approach
A subarray is a contiguous non-empty sequence of elements within an array.

If we can find one of subarrays from beginning, that is an easy case. For example,

Input: nums = [1,1], k = 2
In this case, we find 1 at index 0.

[1] is not 2
[1,1] is 2
return 1
But how about this?

Input: nums = [1,1,2,5], k = 7
[1] is not 7
[1,1] is not 7
[1,1,2] is not 7
[1,1,2,5] is not 7
return 0
That is wrong answer. We have a subarray with a sum of 7(= [2,5]).

We need to find two types of subarrays: one that starts at index 0 and another that starts somewhere in the middle of the array.

Since we can’t change the positions of the numbers in the subarray, let’s go through all the subarrays we can form by iterating from index 0.

total
↓
1:[1]
2:[1,1]
4:[1,1,2]
9:[1,1,2,5]
Let's foucs on [1,1,2,5].

The reason [2,5] is the answer is because 2 + 5 = 7. So, to create the target k (=7) from the current total (=9), we need to subtract 2. In other words, the number of subarrays with a total equal to total - k corresponds to the number of subarrays that sum up to k (=7).

For example,

 * * * *
[1,1,2,5]
 # # $ $

* array is total 9
# array is total 2
$ array is total 7
Look at all subarray above. We have [1,1] which is total 2. That's why if we subtract [1,1] from [1,1,2,5], we can create [2,5]. That means number of total 2 subarray should be answer in this case.

return 1
To understand the algorithm deeply, let's change the array like this.

[1,1,-1,1,2,5] k = 7
In this case, all subarrays should be

1:[1],[1,1,-1]
2:[1,1],[1,1,-1,1]
4:[1,1,-1,1,2]
9:[1,1,-1,1,2,5]
 * *  * * * * 
[1,1,-1,1,2,5]
 # #  $ $ $ $

 * *  * * * * 
[1,1,-1,1,2,5]
 # #  # # $ $
When we create [1,1,-1,1,2,5], we have two subarrays with total 2(total - k), so if we subtract [1,1] and [1,1,-1,1] from [1,1,-1,1,2,5], we can create subarrays with total 7.

[1,1,-1,1,2,5] - [1,1] = [-1,1,2,5]
[1,1,-1,1,2,5] - [1,1,-1,1] = [2,5]
In this case, the number of subarrays with a total of 7 should match the number of subarrays with a total of 2.

This algorithm needs to have total of subarray and frequency of the total. We will use HashMap. Key is total and value is frequency.

One important is that we initialize the HashMap with {0:1}. Look at the first example.

Input: nums = [1,1], k = 2
In this case, HashMap works like this.

For [1], h = {0:1, 1,1}
For [1,1], h = {0:1, 1:1, 2:1}
Every time we calculate total - k and search for the HashMap. When current subarray is [1,1], that is one of target subarray. In this case,

total - k
= 2 - 2
= 0
If we don't have {0:1} in HashMap, we can't add 1 to return value. Or we need to deal with the situation(extra code).