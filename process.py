def process(file_name:str):    
    with open(file_name, "r") as f:
        data = f.read()
        data = data.splitlines()

        data_1 = []
        for i in data:
            if len(i) != 0:
                data_1.append(i)

        indent = 0
        for i in range(len(data_1)):
            current_indent = 0
            for j in data_1[i]:
                if j != " ":
                    break
                current_indent += 1
            if current_indent > indent:
                data_1[i - 1] = data_1[i - 1] + " INDENT"
            if current_indent < indent:
                for j in range(int((indent - current_indent) / 4)):
                    data_1[i - 1] = data_1[i - 1] + " DEDENT"
            indent = current_indent

        count = 0
        for i in data_1[-1]:
            if i == " ":
                count += 1
            else:
                break
            if count % 4 == 0:
                data_1[-1] += " DEDENT"

        result = "\n".join(data_1)
        print(result)
        return result
