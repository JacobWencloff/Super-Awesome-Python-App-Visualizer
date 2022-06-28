

def search(nums, target):
        start = 0
        end = len(nums) -1
        
        while start <= end:
            mid = start + (end - start) // 2
            mid_val = nums[mid]
            
            if mid_val == target:
                print(mid)
                return mid
            elif target < mid_val:
                end = mid - 1
            else:
                start = mid + 1 
        return None




nums = [-1,0,3,5,9,12,13]
target = 3

search(nums, target)