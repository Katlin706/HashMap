# Name: Katlin Hopkins
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - HashMap
# Date: 03/13/2025
# Description: The code provides an implementation of a HashMap using chaining for collisions.

# Citation 
# Date: 03/13/205
# Code from lines 15 through 95 copied from Source URL, which includes imports, HashMap class definition and methods for
# __init__, __str__, _next_prime, _is_prime, get_size, and get_capacity
# Source: Canvas Course Material from Oregon State University, CS261 Data Structures
# URL: https://canvas.oregonstate.edu/courses/1987672/assignments/9952381?module_item_id=25200974


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        the method either adds the key, value pair to the HashMap or updates the value of the node if the key already
        exists in the HashMap
        :param key: a string that represents the key for the node we are adding/updating
        :param value: an object, the value of the node we are adding or updating
        """
        # resize as needed
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # if the hashmap already has this key, work to update its value
        if self.contains_key(key):
            location = self._hash_function(key) % self.get_capacity()
            current_sl_node = self._buckets[location].contains(key)
            current_sl_node.value = value
            return

        # if key isn't in hashmap, add it and iterate forward in size
        else:
            new_location = self._hash_function(key) % self.get_capacity()
            self._buckets[new_location].insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        the method will resize the table to the new_capacity integer, however, it may adjust the new_capacity parameter
        to ensure it is a prime number and greater than 0.
        :param new_capacity: an integer that represents the desired number of buckets in the DA within the HashMap
        """
        #  capacity cannot be 0 or less
        if new_capacity < 1:
            return

        #  requires size to be a prime
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # new da where we will place our re-hashed data
        new_da = DynamicArray()
        for new_index in range(new_capacity):
            new_da.append(LinkedList())

        #  tracking old da and capacity, and establishing hashmap with its new properties
        original_da = self._buckets
        original_capacity = self._capacity
        self._buckets = new_da
        self._capacity = new_capacity
        self._size = 0

        # copying over the values from old da to new da
        for index in range(original_capacity):
            current_linked_list = original_da[index]
            for node in current_linked_list:
                self.put(node.key, node.value)

    def table_load(self) -> float:
        """
        the method calculates the load of the current HashMap
        :return float: a float representing the table load is returned
        """
        load = self._size/self._capacity
        return load

    def empty_buckets(self) -> int:
        """
        the method counts how many buckets are in the HashMap that have no nodes
        :return int: returns the number of buckets that are empty
        """
        running_count = 0
        for index in range(self._capacity):
            if self._buckets[index].length() == 0:
                running_count += 1
        return running_count

    def get(self, key: str) -> object:
        """
        the method takes a key as a parameter and returns the value of that node
        :param key: a string that represents the key of a particular node
        :return object: the value of the node. if no node is found, None is returned
        """
        location = self._hash_function(key) % self._capacity
        sl_node = self._buckets[location].contains(key)
        if sl_node is not None:
            return sl_node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        the method determines if a key is contained within the HashMap
        :param key: a string representing the key of a node
        :return bool: returns True or False based on whether the key is contained in the Hashmap or not, respectively
        """
        if self.get_size() == 0:
            return False

        index_of_key = self._hash_function(key) % self._capacity
        if self._buckets[index_of_key].contains(key) is not None:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        the method removes the node from the HashMap with the matching key value. If no match is found, no action
        occurs.
        :param key: a string that represents the key of the node we are attempting to remove
        """
        location = self._hash_function(key) % self._capacity
        if self._buckets[location].contains(key) is not None:
            self._buckets[location].remove(key)
            self._size -= 1
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        the method provides a list of all key, value pairs within the HashMap
        :return DynamicArray: a DynamicArray is returned that contains a tuple of the key, value pairs
        """
        output_da = DynamicArray()
        for index in range(self._capacity):
            linked_list = self._buckets[index]
            for node in linked_list:
                output_da.append((node.key, node.value))
        return output_da

    def clear(self) -> None:
        """
        the method removes all content from all buckets within the HashMap while maintaining
        current capacity
        """
        self._size = 0
        new_da = DynamicArray()
        for new_index in range(self._capacity):
            new_da.append(LinkedList())
        self._buckets = new_da


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    the function finds the mode of the dynamic array that is passed in as a parameter. it returns a tuple of a dynamic
    array and an int. The DynamicArray returned in the tuple represents the value of the mode. If there are multiple
    values that have the same frequency, all will be listed. The int passed back in the tuple represents the frequncy
    of the mode value(s)
    :param da: a Dynamic Array object that we want to find the mode of
    :return tuple: a tuple of a DynamicArray and an int are passed back, representing the value of the mode and its
    frequency.
    """
    # create a hashmap in the param. key will be the string in the da,
    # the value will be the frequency of that value
    map = HashMap()
    for index in range(da.length()):
        #  if key already exists in hashmap, iterate its frequency by 1
        if map.contains_key(da[index]):
            value = int(map.get(da[index])) + 1
            map.put(da[index], value)
        else:
            map.put(da[index], 1)

    running_mode_array = DynamicArray()
    running_freq = 1

    full_da = map.get_keys_and_values()
    for index in range(full_da.length()):
        # looking at the current index of the da, then looking at the value in the second
        # spot in the tuple returned, which is the value of that node
        if full_da[index][1] > running_freq:
            running_freq = full_da[index][1]
            # create a new DA that is empty, so we can start over and add new mode value
            running_mode_array = DynamicArray()
            running_mode_array.append(full_da[index][0])
        elif full_da[index][1] == running_freq:
            running_mode_array.append(full_da[index][0])

    return running_mode_array, running_freq
