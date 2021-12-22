#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;

class Solution {
public:
    int findNthDigit(int n) {

    	long k = 9;
    	long start = 0;
    	long end = 9;
    	int bitNum = 1;

    	while(true) {
    		if (start <= n && n <= end)
    		{
    			//找到符合 的区间
    			long startNum = k / 9;
    			long index = n - start - 1;
    			long numIndex = index%bitNum+1; //findNum数字的第几位
    			long findNum =  startNum + index/bitNum; //找到的应该从哪个数字进行提取
    			
    			//取findNum 下标为numIndex的数字
    			while(findNum>0){
    				if(bitNum == numIndex) {
    					return findNum%10;
    				}
    				--bitNum;
    				findNum /= 10;
    			}
    		}

    		start = end;
    		k *= 10;
    		++bitNum;
    		end = start + k * bitNum;
    	}
    	return end;
    }
};

int main() {
	cout << 6/10<< endl;
	Solution s;
	int b = s.findNthDigit(11);
	cout << "return " << b << endl;
	return 0;

}

/*输入
数字序列中某一位的数字
数字以0123456789101112131415…的格式序列化到一个字符序列中。在这个序列中，第5位（从下标0开始计数）是5，第13位是1，第19位是4，等等。

请写一个函数，求任意第n位对应的数字。

 	cout << "findNum:" << findNum << endl;
    			cout << "numIndex:" << numIndex << endl;
    			/*vector<int>v;
    			while(findNum>0){
    				v.push_back(findNum%10);
    				findNum /= 10;
    			}
    			return v[v.size()-1-numIndex];*/
示例 1：

输入：n = 3
输出：3
示例 2：

输入：n = 11
输出：0
 

限制：

0 <= n < 2^31
*/
