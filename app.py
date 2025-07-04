import streamlit as st
import polars as pl

st.title("Question Solver App")

# Define options for the dropdown
question_options = [
    "Select a question",
    "A1",
    "A2",
    "A3",
    "B1",
    "B2"
]

# Create the dropdown menu
selected_question = st.selectbox("questions", question_options)

def st_write_list(x: list):
    for it in x:
        st.write(it)

# Create the button
if st.button("solve question"):
    abund = pl.read_csv("data/9606_abund.txt", separator="\t")
    dom = pl.read_csv("data/9606_gn_dom.txt", separator="\t")
    combined = abund.join(dom, on="Gn")
    
    match selected_question:
        case "Select a question":
            st.warning("Please select a question first.")
        case "A1":
            st_write_list(["**A1.1.** How many protein/copy-number pairs are in the file? (Single numerical value)",
            abund.shape[0],
            "**A1.2.** How many unique copy number values are there in the file? (Single numerical value)",
           abund["Mean-copy-number"].n_unique(),
           "**A1.3.** How many pairs of protein and copy number values are in the file? (Single numerical value)",
           abund.group_by(["Gn","Mean-copy-number"]).len().shape[0],
           "**A1.4.** Please also answer the first three questions using a single command line operation in linux.",
            """
                Answer:
You can run the following cli commands in nushell (https://www.nushell.sh/)
```
#A1.1
open data/9606_abund.txt | from tsv | length
53641
#A1.2
open data/9606_abund.txt | from tsv | get `Mean-copy-number` | uniq | length
#A1.3
open data/9606_abund.txt | from tsv | each {|x| $"($x.Gn)_($x.Mean-copy-number)"} | uniq | length
```
            """
            ])
        case "A2":
            a2mean = abund["Mean-copy-number"].mean()
            a2std = abund["Mean-copy-number"].std()
            st_write_list([
                "**A2.** Compute the mean and standard deviation of copy numbers for all proteins (considering unique pairs only) first as a single number for all proteins (two numerical values) and then for each protein separately (Table in tsv/csv).",
                    f"For all proteins, mean is {a2mean} and std is {a2std}.",
                "for each protein:",
                abund.group_by(["Gn","Mean-copy-number"]).agg(
                pl.col("Mean-copy-number").mean().alias("mean"),
                pl.col("Mean-copy-number").std().alias("std"),
            )
            ])
        case "A3":
            pranks = abund.group_by(["Gn","Mean-copy-number"]).agg(
                pl.col("Mean-copy-number").mean().alias("mean"),
            ).with_columns(
                pl.col("mean").rank().alias("rank")
            ).with_columns(
                (pl.col("rank") / pl.len() * 100 ).alias("percentile_rank")
            )

            st_write_list(["**A3.** Calculate the percentile rank (in terms of average copy number ranks) for each protein. (i.e. for protein X, where is it in the ranks from top (0%) to bottom (100%) in terms of abundance) (Table in csv/tsv).",
                    pranks,
                    "Please also give the top ten proteins (highest abundance) as a list with the associated numerical values.",
                    str(pranks.top_k(10, by="mean").select("Gn","percentile_rank").rows())
                    ])
        case "B1":
            st_write_list([
                """
## B. 
Proteins can contain one or more “domains” that are regions in the sequence that correspond to a particular function. The same domain can be seen in many different proteins and proteins can have many domains (i.e. it is a many-to-many relationship).

Here you’ll need to use the file "9606_gn_domains.txt" in combination with the file above (that is we want you to combine data from both files). This file gives, for each protein (Gn column) each domain (Domain column) that is present inside it.
"""
            ])
            st_write_list([
                "Domains:",
                dom,
                "Combined:",
                combined
            ])
            
            dom_most = combined.group_by("Domain").agg(pl.col("Mean-copy-number").mean().alias("avg_abundance")).top_k(k=1,by="avg_abundance").to_struct()[0]

            st_write_list(["**B1.** What is the domain with the highest average abundance (i.e. across all copies of the domain in all proteins)? (single string value and two numerical values)",
          f"Domain with most abundance is {dom_most['Domain']} domain with an average abundance of {dom_most['avg_abundance']}"
          ])
        case "B2":
            dom_mean_std = combined.group_by("Domain").agg(pl.col("Mean-copy-number").mean().alias("mean"),pl.col("Mean-copy-number").std().alias("std")).with_columns(
                pl.col("mean").rank().alias("rank")
            ).with_columns(
                (pl.col("rank") / pl.len() * 100 ).alias("percentile_rank")
            ).sort("rank", descending=True)


            st_write_list(["**B2.** Compute the mean and standard deviation of domain average abundance for each protein domain (i.e. by summing abundance values of all versions of these domains) by combining these two files also, compute the percentile rank values as above (One table).", dom_mean_std])
        case _:
            pass