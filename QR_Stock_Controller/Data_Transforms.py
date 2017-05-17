
class TransformRowToList():
    def __new__(self, input_list):
        output_list = []

        # convert pyodbc row into normal python list
        for x in range(len(input_list)):
            holder = (input_list[x])
            holder = str(holder).replace('(', "").replace(')', "").replace("'", "").replace(",", "")
            output_list.append(holder)

        return (output_list)

class InsertListFillNull():
    def __new__(self, insert_list):
        build_list = ()
        for x in range(len(insert_list)):
            if insert_list[x] == "":
                insert_list[x] = "Not Applicable"


        for x in range(len(insert_list)):
            build_list = build_list + (insert_list[x],)
        return (build_list)

class SplitAndCleanDBReturn():
    def __new__(self, input_list):
        output_list = []
        input_list = str(input_list).split(',')
        for x in range(len(input_list)):
            holder = (input_list[x].replace(')', "").replace("'", "").replace("(", "").replace(",", "").replace("[", "").replace("]", "").lstrip())
            output_list.append(holder)
        return(output_list)