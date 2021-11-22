import random
import sys

def bubble_sort(input_num):
	"""
	排序1 冒泡排序
	"""
	sorted_data = input_num
	for i in range(0,len(input_num)):
		for j in range(0,len(input_num) - i -1):
			if sorted_data[j] > sorted_data[j+1]:
				sorted_data[j], sorted_data[j+1] = sorted_data[j+1], sorted_data[j]
		print("         ", sorted_data)
	return sorted_data

def select_sort(input_num):
	"""
	排序5 简单选择排序
	"""
	sorted_data = input_num
	for i in range(0, len(input_num)):
		print(i)
		for j in range(i, len(input_num)):
			if sorted_data[i] > sorted_data[j]:
				sorted_data[i], sorted_data[j] = sorted_data[j], sorted_data[i]
	return sorted_data

def insert_sort(input_num):
	"""
	排序2 插入排序 
	"""
	sorted_data = input_num
	for i in range(1, len(input_num)):
		for j in range(0, i):
			if sorted_data[j] > sorted_data[i]:
				t = sorted_data[i]
				sorted_data.pop(i)
				sorted_data.insert(j, t)
				break;
		print("         ", sorted_data)
	return sorted_data;
	
def shell_sort(input_num):
	"""
	排序3 希尔排序
	"""
	length = len(input_num)
	if length <= 1:
		return input_num
	sorted_data = input_num
	gap = length // 2
	while gap > 0:
		for i in range(0, length):
			j = i - gap
			temp = sorted_data[i]
			
			
			while j >= 0 and temp < sorted_data[j]:
				sorted_data[j+gap] = sorted_data[j]
				j -= gap
				
			sorted_data[j+gap] = temp

			# for j in range(j, -1, -gap):
			# 	temp = sorted_data[j+gap]
			# 	if temp < sorted_data[j]:
			# 		print("-----------------------------i:",i,"gap:",gap, "j:",j, "                ", sorted_data)
			# 		sorted_data[j+gap], sorted_data[j] = sorted_data[j], sorted_data[j+gap]
			# 		print("----------------------------------------------i:",i,"gap:",gap, "j:",j,  sorted_data)
		gap //= 2
	return sorted_data

def qucik_sort(input_num, left, right):
	"""
	排序4 快速排序
	"""
	def division(input_num, left, right):
		base = input_num[left]
		while left < right:
			while left < right and input_num[right] >= base:
				right -= 1
			input_num[left] = input_num[right]
			while left < right and input_num[left] <= base:
				left += 1
			input_num[right] = input_num[left]
		input_num[left] = base
		return left

	if left < right:
		base_index = division(input_num, left, right)
		qucik_sort(input_num, left, base_index-1)
		qucik_sort(input_num, base_index+1, right)

def heap_sort(input_num):
	"""
	排序6 堆排序 升序
	"""
	def heapAdjust(input_num, parent, length):
		"""
		调整大小堆
		"""
		temp = input_num[parent]
		child = 2 * parent + 1
		# print('before: parent:', parent, "child=", child)
		while child < length:
			# print('enter:  parent:', parent, "child=", child)
			if child + 1 < length and input_num[child] < input_num[child + 1]:
				# print("+1")
				child += 1
			if temp >= input_num[child]:
				# print("break")
				break

			input_num[parent] = input_num[child]
			parent = child
			child = 2 * parent + 1
		input_num[parent] = temp

	if len(input_num) == 0:
		return []
	sorted_data = input_num
	length = len(sorted_data)
	# print("len:", length)
	for i in range((length-2) // 2 , -1, -1):
		# print("      i=",i)
		heapAdjust(sorted_data, i, length)
		# print("      i=",i,sorted_data, "\n\n\n")

	for j in range(length-1, 0, -1):
		sorted_data[j], sorted_data[0] = sorted_data[0], sorted_data[j]
		heapAdjust(sorted_data, 0, j)

def merge_sort(input_num):
	"""
	排序7 归并排序 nlog2n
	"""

	def merge(input_list, left, mid, right, temp):
		i = left
		j = mid + 1
		k = 0

		while i <= mid and j <= right:
			if input_list[i] <= input_list[j]:
				temp[k] = input_list[i]
				i += 1
			else:
				temp[k] = input_list[j]
				j += 1
			k += 1
		print(temp)
		while i <= mid:
			temp[k] = input_list[i]
			i += 1
			k += 1
		while j <= right:
			temp[k] = input_list[j]
			j += 1
			k += 1

		k = 0
		while left <= right:
			input_list[left] = temp[k]
			left += 1
			k += 1

	def merge_sort_temp(input_list, left, right, temp):
		if left >= right:
			return
		mid = (right + left) // 2
		print('++++++++++',mid)
		merge_sort_temp(input_list, left, mid, temp)
		merge_sort_temp(input_list, mid+1, right, temp)
		print('------', mid)
		merge(input_list, left, mid, right, temp)


	if len(input_num) == 0:
		return input_num

	sorted_data = input_num
	temp = [0] * len(sorted_data)
	merge_sort_temp(sorted_data, 0, len(sorted_data)-1, temp)
	return sorted_data


def radix_sort(input_list):
	"""
	排序8 基数排序 nlog2n
	"""

	def max_bit(input_list):
		"""
		最大位数
		"""
		max_data = max(input_list)
		bits_nums = 0
		while max_data:
			bits_nums += 1
			max_data //= 10
		return bits_nums

	def digit(num, d):
		"""
		当前位数的数字
		"""
		p = 1
		while d > 1:
			d -= 1
			p *= 10
		return num // p % 10


	if len(input_list) == 0:
		return input_list

	sorted_data = input_list
	length = len(sorted_data)
	bucket = [0] * length
	for d in range(1, max_bit(sorted_data) + 1):
		count = [0] * 10

		for i in range(0, length):
			count[digit(sorted_data[i], d)] += 1
			# print("--data", sorted_data[i], "bit:", d, "data:", digit(sorted_data[i], d))
		print("\n    ",count)
		for i in range(1, 10):
			count[i] += count[i-1]

		print("new ",count)
		for i in range(length - 1, -1, -1):
			k = digit(sorted_data[i], d)
			print("     ",k, end=', ')
			bucket[count[k] -1] = sorted_data[i]
			count[k] -= 1
			print("----",bucket)

		for i in range(0,length):
			sorted_data[i] = bucket[i]

		print("\n first ------", sorted_data, "\n\n\n\n\n")






if __name__ == '__main__':
	sys.setrecursionlimit(1111111111)
	input_num = []
	for x in range(1,8):
		input_num.append(random.randint(0, 511))
	input_num = [50, 123, 543, 187, 49, 30, 0, 2, 11, 100]
	print("原始数据： " , input_num)

# 	# sorted_num = bubble_sort(input_num)
# 	# print("排序数据: ", sorted_num,"\n\n\n")

# 	# sorted_num = select_sort(input_num)
# 	# print("排序数据: ", sorted_num)

# 	# sorted_num = insert_sort(input_num)
# 	# print("排序数据: ", sorted_num)

	# sorted_num = shell_sort(input_num)
# 	# print("排序数据: ", sorted_num)

# 	qucik_sort(input_num, 0, len(input_num)-1)
	# print("排序数据: ", input_num)

	# heap_sort(input_num)
	# print("排序数据: ", input_num)

	# merge_sort(input_num)
	# print("排序数据: ", input_num)

	radix_sort(input_num)
	print("\n排序数据: ", input_num)