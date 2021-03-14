import docx
import os
import re


# finding all yellow text and filter it (we want only numbers 1-8 chars in length)
# ACTUALLY IT IS MAGICAL BOX WRITTEN ON PYTHON 2
# https://python-docx.readthedocs.io/en/latest/dev/analysis/features/text/font-highlight-color.html
# ^ maybe i should read this ^
def extract_highlighted(document):
    all_pmid = []  # here we got all yellow text
    pmid_cleared = []  # here we got all yellow 1-to-8-digit numbers
    words = document._element.xpath('//w:r')

    WPML_URI = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    tag_rPr = WPML_URI + 'rPr'
    tag_highlight = WPML_URI + 'highlight'
    tag_val = WPML_URI + 'val'
    tag_t = WPML_URI + 't'
    for word in words:
        for rPr in word.findall(tag_rPr):
            high = rPr.findall(tag_highlight)
            for hi in high:
                if hi.attrib[tag_val] == 'yellow':
                    all_pmid.append(word.find(tag_t).text.lower())  # i dunno why we used "encode" there

    for item in all_pmid:
        # match = re.findall(r'(\d{1,8})', item)  # PMID is a 1 to 8-digit accession number with no leading zeros IN ()
        match = re.findall(r'\d{1,8}', item)  # PMID is a 1 to 8-digit accession number with no leading zeros NOT IN ()
        if match:
            pmid_cleared.append(match[0])

    return pmid_cleared


def main(file_name):
    # print(os.getcwd())  # print current wd

    doc = docx.Document(file_name)  # open file

    pmid_list = extract_highlighted(doc)  # get all yellow 1-to-8-digit numbers
    return pmid_list


if __name__ == '__main__':
    main()