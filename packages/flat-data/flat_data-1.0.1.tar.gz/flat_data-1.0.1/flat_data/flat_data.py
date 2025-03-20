
# Class which can convert unstructed dictionary to structured dictionary. Mostly used in Data engineering domain.

class FlatData:
    
    def __init__(self, data, records):
        # data is the input dictionary or list given by client

        self.data = data
        self.records = records

        # flat_data which stores the structured dictionary
        self.flat_data = {}
        for key in records:
            self.flat_data[key] = []
 

    def __dfs(self, curr_data, key_name):
        # __dfs is a private function to traverse all the input data. It follows the Depth first search algorithm

        if(type(curr_data) == list):
            # if the curr_data is of type list, traverse through all the elements of that list
            for element in curr_data:
                self.__dfs(element, key_name)

        elif(type(curr_data) == dict):
            # if the curr_data is of type dict, apply dfs to all the keys of that dictionary
            for key in curr_data.keys():
                self.__dfs(curr_data[key], key)

        else:
            # its primitive data type
            # check if the key_name is present in the records list
            key_index = -1
            for i in range(0, len(self.records)):
                if(self.records[i] == key_name):
                    key_index = i
                    break

            if(key_index != -1):
                key = self.records[key_index]
                self.flat_data[key].append(curr_data)
                list_len = len(self.flat_data[key])
                for i in range(0, key_index):
                    if(len(self.flat_data[self.records[i]]) < list_len):
                        last_value = self.flat_data[self.records[i]][len(self.flat_data[self.records[i]]) - 1]
                        self.flat_data[self.records[i]].append(last_value)



    # public method
    def get_flat_data(self):
        # Client can use get_flat_data to process it convert it into structured format

        self.__dfs(self.data, 'input_data_user')

        return self.flat_data

