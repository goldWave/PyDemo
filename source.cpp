#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;


class Solution {
public:
    void nextPermutation(vector<int>& nums) {
    	int n = nums.size();
    	if (n == 0) {
    		return;
    	}

    	int i = n - 2;
    	int j = n - 1;
    	int k = n - 1;

    	while (i >= 0 && nums[i] > nums[j]) {
    		i--;
    		j--;
    	}
    	if (j >= 0) {
    		// 找k值
    		while(j <= k && nums[i] > nums[k]){
    			k--;
    		}
    		swap(nums[i], nums[k]);

    		i++;
    		while (i < k) {
    			swap(nums[i], nums[k]);
    			i--;
    			k--;
    		}
    	}
    }
};

class SolutionA {
public:
    int countPrimes(int n) {
    	std::vector<bool>vec(n, true);
    	int total = 0;
    	if (n < 2)
    	{
    		return total;
    	}

    	vec[0] = false;
    	vec[1] = false;

    	int i = 2;

    	while (i < n) {

    		if (vec[i] == true)
    		{
    			total++;
    			for (int j = i*2; j < n; j+=i)
    			{
    				vec[j] = false;
    			}
    		}
    		i++;
    	}
    	return total;
    }
};

int main() {

	SolutionA s;
	auto c = s.countPrimes(4);	
	std::cout << c << std::endl;

/*	std::vector<int> m{3,2,1};
	for (auto x : m) {
		cout << "iiii " <<  x << "  ";
	}
	
	cout << endl;

	Solution s;
	s.nextPermutation(m);
	// cout << "return " << b << endl;
	for (auto x : m) {
		cout << "iiii " <<  x << "  ";
	}
	cout << endl;*/
	return 0;

}
