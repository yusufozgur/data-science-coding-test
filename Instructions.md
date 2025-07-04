# Programming a Web Application

Write a simple web app (e.g. via Flask/Django) to display data and questions/results as a single HTML page.

For each question listed below (A1, A2, A3, B1, B2) display the question together with a "calculate" button.

On each calculate-button click, display the corresponding answer to the question. The answer should appear below each question.

The answer should be displayed as text (single numerical value) or the table (depending on the type of result required).

All calculations required to answer the questions should be performed on the server (ideally using Python).

Displaying answers should not require page reloading (you may use AJAX or Fetch to API to get answers from the server and JavaScript to modify the HTML DOM in place).

Please also provide text files containing both questions and answers labeled as below (A1, A2, etc.).

# Bioinformatics/Data science questions

Questions to answer:

In addition to the files above and below, please also provide summaries of the answers below in the body of an email. For instance, single word/number answers with questions and for tables please give the top and bottom of each table. Please also place all relevant files (tables, code, etc.), including the Email summary text as a word file into the shared folder you were given.

## A. The file "9606_abund.txt" gives, for each human protein (Gn column), copy numbers. These roughly measure the average amount of each protein in a typical human cell.

*   **A1.** How many protein/copy-number pairs are in the file? (Single numerical value)
    How many unique copy number values are there in the file? (Single numerical value)
    How many pairs of protein and copy number values are in the file? (Single numerical value)
*   **A2.** Compute the mean and standard deviation of copy numbers for all proteins (considering unique pairs only) first as a single number for all proteins (two numerical values) and then for each protein separately (Table in tsv/csv).
*   **A3.** Calculate the percentile rank (in terms of average copy number ranks) for each protein. (i.e. for protein X, where is it in the ranks from top (0%) to bottom (100%) in terms of abundance) (Table in csv/tsv). Please also give the top ten proteins (highest abundance) as a list with the associated numerical values.

Please also answer the first three questions using a single command line operation in linux.

## B. Proteins can contain one or more “domains” that are regions in the sequence that correspond to a particular function. The same domain can be seen in many different proteins and proteins can have many domains (i.e. it is a many-to-many relationship).

Here you’ll need to use the file "9606_gn_domains.txt" in combination with the file above (that is we want you to combine data from both files). This file gives, for each protein (Gn column) each domain (Domain column) that is present inside it.

*   **B1.** What is the domain with the highest average abundance (i.e. across all copies of the domain in all proteins) and what is the value of the average abundance, and how many times was the domain seen? (single string value and two numerical values)
*   **B2.** Compute the mean and standard deviation of domain average abundance for each protein domain (i.e. by summing abundance values of all versions of these domains) by combining these two files also, compute the percentile rank values as above (One table).

Upload data files and code to the public GitHub repository - check-in data files and code together with instructions on how to run it (README) and notify us sending short email with GitHub repo link to: ____________

It is not mandatory to answer/complete all queries.

Contact __________ in case of questions.

# Email format

In the Email back to us, please use this format (in addition to uploading/providing files):

Copyright Metisox Ltd 2025