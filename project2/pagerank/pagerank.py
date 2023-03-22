import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    linked_pages = len(corpus[page])
    prob_linked_page = damping_factor/(linked_pages)
    prob_random_page = (1-damping_factor)/(len(corpus))

    model = dict()
    model[page] = prob_random_page
 
    for pages in corpus:
        if pages not in model:
            model[pages] = prob_random_page
        if pages in corpus[page]:
             model[pages] += prob_linked_page

    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    list_pages = list(corpus.keys())
    start_page = random.choices(list_pages)[0]

    count = dict()
    for page in corpus:
        count[page] = 0
    
    for i in range(n):
        count[start_page]+=1

        model = transition_model(corpus,start_page,damping_factor)
        start_page = random.choices(list(model.keys()),weights=list(model.values()))[0]
    
    rank = dict()
    for page in corpus:
        rank[page] = count[page] / n

    return rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    """

    rank = dict()
    N = len(corpus)

    for page in corpus:
        rank[page] = 1/N
    
    while(True):
        change = False
        for page in corpus:
            summation  = 0;
            for pages in corpus:
                if page in corpus[pages]:
                    numLinks = len(corpus[pages])
                    summation += rank[pages]/numLinks

            pageRank = (1-damping_factor)/N + damping_factor*summation

            if abs(rank[page]-pageRank) > 0.001:
                change = True
            
            rank[page] = pageRank

        sum = 0
        for i in rank:
            sum+=rank[i]
        
        if change == False:
            print(sum)
            return rank

if __name__ == "__main__":
    main()
