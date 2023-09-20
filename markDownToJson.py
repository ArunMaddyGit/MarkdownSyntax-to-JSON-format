import re
import json

"""
------------------------------------------------------
Without using Markdown or External Library File 
------------------------------------------------------
List of Functions
__main__ = main function
markdown_to_Html -> to convert .md to html content
clean_html -> to clean html content
html_To_Json -> to convert HTML content to JSON

please change input_file_name to generate output

"""

# to convert markdown content to Counterpart Html Content
def markdown_To_Html(em_str,lines):

    # em_str == empty string
    # tagsList=['#','>','*','_','+','-','!','[',']','(','=','`','|','~']

    digit=re.compile("^[0-9]")

    #function to identify heading
    def get_Headings(line):
        heading=0
        for ch in line:
            if ch != '#':
                break
            heading+=1
        h_line="<h"+str(heading)+">"+line[heading+1:-1]+"</h"+str(heading)+">"
        return h_line

    #function to identify ordered and unordered list
    def get_list(line):
        line=line.strip("+").strip(" ").strip("\n").strip("-").strip("*").strip("1").strip("2").strip("3")
        return "\n<li>"+line+"</li>"

    # to format img tag
    def get_img(line):
        count=0
        alt_text=""
        title=""
        path=""
        line=line.rstrip("\n")

        # to parse alt text of img
        if line[1]=='[':
            line=line.strip("!").strip("[")
            for ch in line:
                if ch ==']':
                    break
                alt_text+=ch

        #to get path of the img
            count=line.index("(")
            for i in range(count+1,len(line)):
                if line[i] == ')':
                    break
                path+=line[i]
            # c = line.index("\"")
            # if c:
            #     title=line[c+1:c+1+1]
        return "<img src=\""+path+"\" alt=\""+alt_text+"\" title=\""+title+"\"/>"


    # to parse anchor tag element
    def get_href(line):
        # line=line.split(" ")
        text = ""
        src = ""
        try:
            start=line.index("[")
            end=line.index("]")
            # to get Text of the Anchor Tag
            for i in range(start+1,len(line)):
                if line[i] == ")" or i >= end:
                    break
                text += line[i]
        except:
            pass
        try:
            hstart=line.index("(")
            hend=line.index(")")

            # to get href path of the tag
            if hstart and hend:
                for i in range(hstart+1,hend):
                    src += line[i]
        except:
            pass

        return "<a href=\""+src+"\">"+text+"</a>"

    # to get <p> paragraph tag
    def getline(line):
        line=line.strip(" ").rstrip(" ")
        em=""

        for ch in line:

            # to check if there is an anchor tag in inline
            if ch == '[':
                em+=get_href(line)
            em+=ch
        em.strip(" ")
        if em.isspace():
            return
        else:
            return "<p>"+em+"</p>\n"


    # main code

    list_exist=False
    line_count=0

    for line in lines:
        line_count+=1

        #
        if line.startswith('* ') or line.startswith("- ") or line.startswith("+ "):
            pass
        else:
            list_exist = False

        # identifying elements
        # header
        if line[0] == '#':
            em_str+= get_Headings(line) +"\n"

        # unoderer list
        elif line.startswith('* ')  or line.startswith("- ") or line.startswith("+ "):
            if not list_exist:
                em_str += "<ul>" + get_list(line) + "\n"
                list_exist = True
            else:
                em_str + get_list(line) + "\n"

            # check if the list closes next line
            nextline=lines[line_count+2]
            if nextline.startswith('* ')  or nextline.startswith("- ") or nextline.startswith("+ "):
                continue
            else:
                em_str+="</ul>\n"
                list_exist=False

        # strong and emphasis
        elif line.startswith("**") or line.startswith("--"):
            line=line.strip("*").strip(" ").strip("\n").strip("-").rstrip("*")
            em_str+="<strong>"+line+"</strong>"

        elif line.startswith("*") or line.startswith("-"):
            line = line.strip("*").strip(" ").strip("\n").strip("-").rstrip("*").rstrip("-")
            em_str += "<em>" + line + "</em>"

        # blockqoute
        elif line.startswith(">"):
            line = line.strip(">").strip(" ").strip("\n").rstrip(">")
            em_str += "<blockqoute>" + line + "</blockqoute>"

        # img tag
        elif line.startswith("!"):
            em_str+= get_img(line)+"\n"

        # anchor tag
        elif line.startswith("["):
            em_str+= get_href(line)+"\n"

        # empty lines
        elif line.isspace():
            continue

        # odered list
        elif digit.search(line[0]):
            if not list_exist:
                em_str += "<ol>" + get_list(line) + "\n"
                list_exist = True
            else:
                em_str + get_list(line) + "\n"
            nextline=lines[line_count+2]
            if nextline.startswith('* ')  or nextline.startswith("- ") or nextline.startswith("+ "):
                continue
            else:
                em_str+="</ol>\n"
                list_exist=False

        # p
        else:
            em_str+= getline(line)

    return em_str



def html_To_Json(htmlcontent):

    json_data = {
        "html_content": htmlcontent
    }
    print(json_data)

    return json_data


""" 'tried classifing futher into individual object'

    # regex to identify the opening and closing tags
    opening_tag = re.compile('^<[a-zA-Z]')
    closing_tag = re.compile(('>$' or '/>$' or '^</'))

    # spliting into a String List
    htmlcontent = " ".join(htmlcontent.split())
    # print(htmlcontent)

    htmlCon = htmlcontent.split(" ")

    for i in range(0, len(htmlCon)):

        ele = htmlCon[i]

        #
        if ele == "<!DOCTYPE":
            htmlCon[i] = htmlCon[i].replace(htmlCon[i], "{ \"" + ele[2:] + "\" : ")
        # to identify br hr tags
        if ele in ['<br>', 'br', 'hr', '<hr>']:
            htmlCon[i] = htmlCon[i].replace(ele, "")
            continue

        # to format opening tags
        # replacing opening Tag with { and tag name
        if opening_tag.search(ele):
            htmlCon[i] = htmlCon[i].replace("<", "{ \"")
            if ele[-1] == '>':
                htmlCon[i] = htmlCon[i].replace(htmlCon[i], "{ \"" + ele[1:-1] + "\" : ")
            else:
                htmlCon[i] = htmlCon[i] + "\" : "

        # to format closing tag
        elif closing_tag.search(ele):
            if ele[-1] == '/>':
                htmlCon[i] = htmlCon[i].replace(htmlCon[i], " }, ")
            if ele[0:2] == '</':
                htmlCon[i] = htmlCon[i].replace(htmlCon[i], " }, ")
            if ele[-1] == '>':
                htmlCon[i] = htmlCon[i].replace('>', " }, ")


    result = " ".join(htmlCon)

    json_data = "{ html :" + result + "}" 

    print(json_data)

    return json_data
"""



def clean_Html(empty_string, lines):

    # cleaning html content for further processing
    for character in lines:
        if character == '<':
            empty_string += " " + character
            continue
        if character == '>':
            empty_string += character + " "
            continue
        empty_string += character


    # Calling Function to Convert HTML to JSON
    return html_To_Json(empty_string)


if __name__ == '__main__':

    # input file and output file
    input_file_name = "assesment.md"
    output_file_name = "json_data.json"

    try:
        with open(input_file_name, "r") as file1:
            file_content = file1.readlines()
            empty_string = ''

            # Function to clean and transform content and assigning to an Empty String
            html_data = markdown_To_Html(empty_string, file_content)


            json_data = clean_Html(empty_string,html_data)

            # writing into an json file
            with open(output_file_name, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)

                print(input_file_name +" has been converted to JSON file as "+ output_file_name)



    except Exception as e:
        print("Error in reading file", e)
    finally:
        file1.close()