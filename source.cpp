#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};
 
class Solution {
public:
    ListNode* removeZeroSumSublists(ListNode* head) {
    	ListNode *pre = new ListNode(0, head);

    	ListNode *cur = pre->next;
    	unordered_map<int, ListNode *>sumMap;
    	while (cur) {
    		orderma
    	}
    }
};

int main() {
/*	cout << 6/10<< endl;
	Solution s;
	std::vector<int> m{4,3,2,7,8,2,3,1};
	auto  b = s.findDisappearedNumbers(m);
	// cout << "return " << b << endl;
	for (auto x : b) {
		cout << "iiii " <<  x << "  ";
	}
	cout << endl;*/
	return 0;

}

/*
示例 1：

输入：head = [1,2,-3,3,1]
输出：[3,1]
提示：答案 [1,2,1] 也是正确的。
示例 2：

输入：head = [1,2,3,-3,4]
输出：[1,2,4]
示例 3：

输入：head = [1,2,3,-3,-2]
输出：[1]

*/
