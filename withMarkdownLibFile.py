import re
import json
import markdown

"""
------------------------------------------------------
with using Markdown Library File
    -to convert Markdown to html

dependency--
-pip install markdown
------------------------------------------------------
Functions List

__main__ = main function
clean_html -> to clean html content
html_To_Json -> to convert HTML content to JSON

please change input_file_name to generate output

"""


# to convert from HTML content to JSON
def html_To_Json(htmlcontent):
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

    json_data = "{\n html : " + result + "\n}"

    print(json_data)

    return json_data


# to clean Html Content to further Processing
def clean_Html(empty_string, lines):
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

    input_file_name = "assesment.md"
    output_file_name = "json_data1.json"

    try:
        with open(input_file_name, "r") as file1:
            file_content = file1.read()
            empty_string = ''

            # markdown to convert MarkDown Syntax to HTML
            file_content = markdown.markdown(file_content)

            # Function to clean and transform content and assigning to an Empty String
            json_data = clean_Html(empty_string, file_content)

            # writing into an json file
            with open(output_file_name, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)

                print(input_file_name + " has been converted to JSON file as " + output_file_name)


    except Exception as e:
        print("Error in reading file", e)
    finally:
        file1.close()