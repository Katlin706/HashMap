# Name: Katlin Hopkins
# OSU Email: hopkinka@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - HashMap
# Due Date: 03/13/2025
# Description: The code provides a class for a HashMap that is implemented with Open Addressing with
#                Quadratic Probing for collision resolution.

# Citation 
# Date: 03/13/205
# Code from lines 16 through 94 copied from Source URL, which includes imports, HashMap class definition and methods for
# __init__, __str__, _next_prime, _is_prime, get_size, and get_capacity
# Source: Canvas Course Material from Oregon State University, CS261 Data Structures
# URL: https://canvas.oregonstate.edu/courses/1987672/assignments/9952381?module_item_id=25200974

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        this method takes a key and value and adds or updates the hashmap with this new key value pair. if the
        key already exists in the hashmap, it's value is updated. if the table load is greater than or equal to 0.5,
        the hashmap will be resized to have additional buckets.
        :param key: a string that represents the key for the hashentry we are adding/updating
        :param value: an object, the value of the hash entry we are adding or updating
        """
        if key is None:
            return
        if value is None:
            return

        # resize when needed
        if self.table_load() > 0.5:
            self.resize_table(self._capacity*2)

        # if hashmap already has the key
        if self.contains_key(key):
            initial_index = self._hash_function(key) % self._capacity
            #  if it is found at the first hashed location
            if self._buckets[initial_index].key == key:
                self._buckets[initial_index].value = value
            else:
                index = initial_index
                counter = 1
                #  all values will be filled until we reach the key
                while self._buckets[index].key != key:
                    index = (initial_index + counter ** 2) % self._capacity
                    counter += 1
                self._buckets[index].value = value
                if self._buckets[index].is_tombstone:
                    self._buckets[index].is_tombstone = False
                    self._size += 1

        # if hashmap does not have the key
        else:
            initial_index = self._hash_function(key) % self._capacity
            index = initial_index
            counter = 1
            while self._buckets[index] is not None:
                if self._buckets[index].is_tombstone:
                    break
                index = (initial_index + counter ** 2) % self._capacity
                counter += 1
            new_hash_entry = HashEntry(key, value)
            self._buckets.set_at_index(index, new_hash_entry)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        the method will resize the table to the new_capacity integer, however, it may adjust the new_capacity parameter
        to ensure it is a prime number and greater than the size of the current hashmap
        :param new_capacity: an integer that represents the desired number of buckets in the DA within the HashMap
        """
        #  only allowed if greater than the current size
        if new_capacity < self._size:
            return

        # must be prime, find the next prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # create da that will eventually hold the hash entries
        new_da = DynamicArray()
        for index in range(new_capacity):
            new_da.append(None)

        #  tracking old da and capacity, and establishing hashmap with its new properties
        original_da = self._buckets
        original_capacity = self._capacity
        self._buckets = new_da
        self._capacity = new_capacity
        self._size = 0

        for index in range(original_capacity):
            if original_da[index] is not None:
                hash_entry = original_da[index]
                self.put(hash_entry.key, hash_entry.value)
                # calling put creates a new hash entry, and defaults to is_tombstone false. adjust to true when needed
                if original_da[index].is_tombstone:
                    hash_entry.is_tombstone = True

    def table_load(self) -> float:
        """
        the method provides the current table load of the hashmap
        :return float: the load of the hashmap
        """
        load = self._size / self._capacity
        return load

    def empty_buckets(self) -> int:
        """
        the method determines the count of empty buckets within the hashmap
        :return int: an int representing the number of empty buckets in the hashmap
        """
        running_count = 0
        for index in range(self._capacity):
            if self._buckets[index] is None:
                running_count += 1
            #  can have a hash entry in the DA but it's a tombstone, check for that too and iterate empty count forward
            if self._buckets[index] is not None and self._buckets[index].is_tombstone is True:
                running_count += 1
        return running_count

    def get(self, key: str) -> object:
        """
        the method takes a key as a parameter and returns the value of that hash entry
        :param key: a string that represents the key of a particular hash entry
        :return object: the value of the hash entry. if no hash entry is found, or the hash entry is a tombstone,
         None is returned
        """

        location = self._hash_function(key) % self._capacity
        counter = 1
        if self._buckets[location] is not None:
            #  if at first location, not a tombstone
            if self._buckets[location].key == key and self._buckets[location].is_tombstone is False:
                return self._buckets[location].value
            #  if not at first location, do quadratic probing
            elif self._buckets[location].key != key:
                counter = 1
                index = location
                while self._buckets[index].key != key:
                    index = (location + counter ** 2) % self._capacity
                    # if we hit a None, then the key won't exist in the hashmap
                    if self._buckets[index] is None:
                        return None
                    counter += 1
                # if we've found a matching key, check for tombstone
                if not self._buckets[index].is_tombstone:
                    return self._buckets[index].value
                return False
        # no hash entry at the has location (also means no tombstone at location), no hash entry exists with this key
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        the method takes a key as the parameter and determines if that key exists in the hashmap. Note that the
        key must be on a hash entry that is not a tombstone to be considered a part of the hashmap
        :param key: a string representing the key of a hash entry
        :return bool: returns True or False based on whether the key is contained in the Hashmap or not, respectively
        """
        if self._size == 0:
            return False

        location = self._hash_function(key) % self._capacity

        # If first location checked is None, key cannot exist in the hashmap
        if self._buckets[location] is None:
            return False
        # if we find the key at first location, and it's not a tombstone
        if self._buckets[location].key == key and self._buckets[location].is_tombstone is False:
            return True
        # otherwise, need to do quadratic probing to find if it's somewhere else in hashmap
        counter = 1
        index = location
        while self._buckets[index].key != key:
            index = (location + counter ** 2) % self._capacity
            # if we hit a None, key cannot be in the hashmap
            if self._buckets[index] is None:
                return False
            counter += 1
        # if we find a matching location, check for tombstone
        if self._buckets[index].key == key and self._buckets[location].is_tombstone is False:
            return True

        return False

    def remove(self, key: str) -> None:
        """
        the method removes the hash entry from the HashMap with the matching key value. If no match is found, no action
        occurs.
        :param key: a string that represents the key of the hash entry we are attempting to remove
        """
        location = self._hash_function(key) % self._capacity
        # if first location checked is None, key cannot exist in the hashmap.
        if self._buckets[location] is None:
            return
        # if we find key at the first location, if it isn't already tombstone, make it a tombstone and reduce size.
        if self._buckets[location].key == key:
            if not self._buckets[location].is_tombstone:
                self._buckets[location].is_tombstone = True
                self._size -= 1
                return
        # complete quadratic probing to find next possible index/location
        for index in range(self._capacity):
            potential_new_location = (location + index ** 2) % self._capacity
            # if you hit None, the key cannot exist in the hashmap
            if self._buckets[potential_new_location] is None:
                return
            # if you find a matching key, check for tombstone. if not a TS, set it as one and decrement size
            if self._buckets[potential_new_location].key == key:
                if not self._buckets[potential_new_location].is_tombstone:
                    self._buckets[potential_new_location].is_tombstone = True
                    self._size -= 1
                return

    def get_keys_and_values(self) -> DynamicArray:
        """
        the method provides a list of all key, value pairs within the HashMap
        :return DynamicArray: a DynamicArray is returned that contains a tuple of the key, value pairs
        """
        key_value_da = DynamicArray()
        for index in range(self._capacity):
            hash_entry = self._buckets[index]
            if hash_entry is not None:
                if not hash_entry.is_tombstone:
                    key_value_da.append((hash_entry.key, hash_entry.value))
        return key_value_da

    def clear(self) -> None:
        """
        the method removes all content from all buckets within the HashMap while maintaining
        current capacity
        """
        new_da = DynamicArray()
        for index in range(self._capacity):
            new_da.append(None)
        self._buckets = new_da
        self._size = 0

    def __iter__(self):
        """
        allows for iteration across the hashmap object. calls out to HashMapIterator class.
        """
        return HashMapIterator(self._buckets)


class HashMapIterator:
    """
    this calls provides the iter and next functions to facilitate iteration across the hashmap
    """
    def __init__(self, da_of_hashmap):
        self._da_of_hashmap = da_of_hashmap
        self._index = 0

    def __iter__(self):
        """allows for iteration across the hashmap object. creates iterator"""
        return self

    def __next__(self):
        """
        allows for iteration across the hashmap object. obtains the next value and advances
        the iterator. Note, it only returns hash entries that have value and are not tombstones
        """
        try:
            for index in range(self._index, self._da_of_hashmap.length()+1):
                hash_entry = self._da_of_hashmap[index]
                if hash_entry is not None:
                    if not hash_entry.is_tombstone:
                        # still need to iterate index to facilitate overall iteration
                        self._index += 1
                        return hash_entry
                else:
                    self._index += 1

        except DynamicArrayException:
            raise StopIteration

