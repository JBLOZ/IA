class Solucion:

    def subsets(self, nums:list):

        n = len(nums)
        res, sol = [], []


        def backtrack(i):

            if n == i:
                res.append(sol.copy())
                return 
            
            backtrack(i+1)

            sol.append(nums[i])
            backtrack(i + 1)
            sol.pop()
        
        backtrack(0)

        return res


if __name__ == "__main__":
    seter = Solucion()
    print(seter.subsets(nums=[2,3,4,2]))

