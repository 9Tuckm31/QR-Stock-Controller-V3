
class Build_File(object):
    def __new__(self, OutText, build_list, file):

        OutText = open(file,'w')
        # Add open tuck statement
        build_list_out = []
        for x in range(len(build_list)):
            build_list_out.append(build_list[x])
            build_list_out.append("\n")

        write_to_file = Create_Ini_File(OutText, build_list_out, file)
        return build_list_out

class Create_Ini_File(object):

    def __new__(self, OutText, build_list, file):
        with open(file, 'r') as ini_file:
            data = ini_file.read()

        for x in range(len(build_list)):

            OutText.write((build_list[x]))

        OutText.close()

class Read_File(object):
    def __new__(self, Target):
        out_list = []
        with open(Target) as input_file:
            for i, line in enumerate(input_file):
                line = line[:-1]
                out_list.append(line)



        return(out_list)
