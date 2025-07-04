import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    return mo, pl


@app.cell
def _(mo):
    mo.md(
        r"""
    ## A. 

    The file "9606_abund.txt" gives, for each human protein (Gn column), copy numbers. These roughly measure the average amount of each protein in a typical human cell.
    """
    )
    return


@app.cell
def _(mo, pl):
    abund = pl.read_csv("data/9606_abund.txt", separator="\t")
    mo.vstack(["Inspect data",abund])
    return (abund,)


@app.cell
def _(abund, mo):
    mo.vstack(["**A1.** How many protein/copy-number pairs are in the file? (Single numerical value)",
              abund.shape[0]
              ])
    return


@app.cell
def _(abund, mo):
    mo.vstack(["How many unique copy number values are there in the file? (Single numerical value)",
               abund["Mean-copy-number"].n_unique()
              ])
    return


@app.cell
def _(abund, mo):
    mo.vstack(["How many pairs of protein and copy number values are in the file? (Single numerical value)",
              abund.group_by(["Gn","Mean-copy-number"]).len().shape[0]
              ])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Please also answer the first three questions using a single command line operation in linux.

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
    )
    return


@app.cell
def _(abund, mo, pl):
    a2mean = abund["Mean-copy-number"].mean()
    a2std = abund["Mean-copy-number"].std()
    mo.vstack([
        "**A2.** Compute the mean and standard deviation of copy numbers for all proteins (considering unique pairs only) first as a single number for all proteins (two numerical values) and then for each protein separately (Table in tsv/csv).",
              f"For all proteins, mean is {a2mean} and std is {a2std}.",
        "for each protein:",
        abund.group_by(["Gn","Mean-copy-number"]).agg(
        pl.col("Mean-copy-number").mean().alias("mean"),
        pl.col("Mean-copy-number").std().alias("std"),
    )
    ])
    return


@app.cell
def _(abund, mo, pl):
    pranks = abund.group_by(["Gn","Mean-copy-number"]).agg(
        pl.col("Mean-copy-number").mean().alias("mean"),
    ).with_columns(
        pl.col("mean").rank().alias("rank")
    ).with_columns(
        (pl.col("rank") / pl.len() * 100 ).alias("percentile_rank")
    )

    mo.vstack(["**A3.** Calculate the percentile rank (in terms of average copy number ranks) for each protein. (i.e. for protein X, where is it in the ranks from top (0%) to bottom (100%) in terms of abundance) (Table in csv/tsv).",
              pranks,
               "Please also give the top ten proteins (highest abundance) as a list with the associated numerical values.",
               str(pranks.top_k(10, by="mean").select("Gn","percentile_rank").rows())
              ])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## B. 
    Proteins can contain one or more “domains” that are regions in the sequence that correspond to a particular function. The same domain can be seen in many different proteins and proteins can have many domains (i.e. it is a many-to-many relationship).

    Here you’ll need to use the file "9606_gn_domains.txt" in combination with the file above (that is we want you to combine data from both files). This file gives, for each protein (Gn column) each domain (Domain column) that is present inside it.
    """
    )
    return


@app.cell
def _(mo, pl):
    dom = pl.read_csv("data/9606_gn_dom.txt", separator="\t")
    mo.vstack([
        "Domains:",
        dom
    ])
    return (dom,)


@app.cell
def _(abund, dom, mo):
    combined = abund.join(dom, on="Gn")
    mo.vstack([
        "Combined:",
        combined
    ])
    return (combined,)


@app.cell
def _(combined, mo, pl):
    dom_most = combined.group_by("Domain").agg(pl.col("Mean-copy-number").mean().alias("avg_abundance")).top_k(k=1,by="avg_abundance").to_struct()[0]

    mo.vstack(["**B1.** What is the domain with the highest average abundance (i.e. across all copies of the domain in all proteins)? (single string value and two numerical values)",
              f"Domain with most abundance is {dom_most['Domain']} domain with an average abundance of {dom_most['avg_abundance']}"
              ])
    return


@app.cell
def _(combined, mo, pl):
    dom_mean_std = combined.group_by("Domain").agg(pl.col("Mean-copy-number").mean().alias("mean"),pl.col("Mean-copy-number").std().alias("std")).with_columns(
        pl.col("mean").rank().alias("rank")
    ).with_columns(
        (pl.col("rank") / pl.len() * 100 ).alias("percentile_rank")
    ).sort("rank", descending=True)


    mo.vstack(["**B2.** Compute the mean and standard deviation of domain average abundance for each protein domain (i.e. by summing abundance values of all versions of these domains) by combining these two files also, compute the percentile rank values as above (One table).", dom_mean_std])
    return


if __name__ == "__main__":
    app.run()
