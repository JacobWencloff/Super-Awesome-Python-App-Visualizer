

# def search(nums, target):
#         start = 0
#         end = len(nums) -1
        
#         while start <= end:
#             mid = start + (end - start) // 2
#             mid_val = nums[mid]
            
#             if mid_val == target:
#                 print(mid)
#                 return mid
#             elif target < mid_val:
#                 end = mid - 1
#             else:
#                 start = mid + 1 
#         return None




# nums = [-1,0,3,5,9,12,13]
# target = 3

# search(nums, target)

def searchInsert( nums, target):
    low_index = 0
    high_index = len(nums) -1

    while low_index <= high_index:
        mid_index = low_index + (high_index - low_index) // 2
        mid_val = nums[mid_index]
        
        if target > nums[high_index]:
            return high_index + 1

        elif target < nums[low_index]:
            if low_index == 0:
                return low_index
            else:
                return low_index - 1

        if (high_index - low_index) == 1:
            return mid_index
        
        if mid_val == target:
            return(mid_index)
        
        elif target < mid_val:
            high_index = mid_index -1
            
        elif target > mid_val:
            low_index = mid_index +1

            

nums = [2,3,5,6]

print(searchInsert(nums, 4))