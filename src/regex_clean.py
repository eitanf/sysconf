# You can run this script with `python regex_clean.py` in a directory with a `papers` folder which contains everything to be cleaned.

import regex
import os

if input("""I am expecting to be in a directory where 'papers' folder contains 
        all the .txt files. I will create a 'cleaned' folder if necessary. 
        Should I proceed? (y/n)""") != "y":
        quit()

if not os.path.isdir("papers"):
    print("Can't find 'papers'. Bye.")
    quit()

if not os.path.isdir("cleaned"):
    os.mkdir("cleaned")

for filename in sorted(os.listdir("papers")):
    if os.path.isfile(f"cleaned/{filename}"):
        continue

    i = filename.find("_")
    conf_name = filename[:i]

    with open(f"papers/{filename}") as f:
        text = f.read()

    # Remove conference name from headers (improvement: look for paper title as well)
    text = regex.sub(f"(?m)^.*{conf_name}.*$", "", text)

    # Remove text read from figures and tables (assuming the caption is below)
    text = regex.sub("(?r)(?m)(?s)\..*?\n((?:Fig\.|Figure|Table|TABLE) [0-9IVX]+[:.].+?\.\n)", r".\n\1" ,text)

    # Remove text read from algorithms (assuming the caption is above)
    text = regex.sub("(?m)(?s)^Algorithm:? [0-9]*.*\n(.*?\.)", r"\1", text)

    # Remove equations 
    # (adding the letter x to operations might result in words containing x being deleted)
    # (adding - to operations might result in hypenated words being deleted, I have added the unicode minus instead)
    text = regex.sub("[\w\u0370-\u03ff]+ ?[−+*=\/·] ?[\w\u0370-\u03ff]+ ?(?:[−+*= \/·] ?[\w\u0370-\u03ff]+ ?)*[−+*=\/·] ?[\w\u0370-\u03ff]+", "", text)

    # Remove numbers (with weird pattern so we don't remove citations)
    text = regex.sub("([^,])\s[0-9]+(?:[:\.,\s])?[0-9]*([:\.,\s])?", r"\1\2", text)

    # Remove form feed characters
    text = regex.sub("\f", "", text)

    # Remove artifacts from removing numbers (e.g. 5.3.1 -> ..)
    text = regex.sub("(?m)^[:\.]+ ", "", text)
    text = regex.sub("\([\.,:; ]*\)", "", text)

    # Remove single characters (except a, A, I):
    text = regex.sub("(?V1)\m[\w--[AIa]]\M", "", text)

    with open(f"cleaned/{filename}", "w") as f:
        f.write(text)
