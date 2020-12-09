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
    N = len(corpus)
    final_dict = {}

    for actual_page in corpus:
        final_dict[actual_page] = (1 - damping_factor)/N

    for link in corpus[page]:
        if link == page:
            del corpus[page][page]

    number_of_links_of_page = len(corpus[page])

    if number_of_links_of_page == 0:
        return final_dict

    for link in corpus[page]:
        final_dict[link] += damping_factor / number_of_links_of_page

    return final_dict

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    first_page = random.choice(list(corpus))
    model = transition_model(corpus, first_page, DAMPING)

    for i in range(n):

        choosen = random.random()
        total = 0

        for k, v in model.items():
            total += v

            if choosen <= total:
                page = k
                break
        
        model = transition_model(corpus, page, DAMPING)
    
    return model

def iterate_pagerank(corpus, damping_factor, final_dict = None):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)

    if final_dict is not None:
        
        convergence = {}

        for actual_page in corpus:

            number_of_links_of_page = len(corpus[actual_page])

            if number_of_links_of_page == 0:
                number_of_links_of_page = 1 / N

            old_value = final_dict[actual_page]

            final_dict[actual_page] = (1 - damping_factor) / N
            final_dict[actual_page] += damping_factor * final_dict[actual_page] / number_of_links_of_page

            if old_value - final_dict[actual_page] > -0.001 and old_value - final_dict[actual_page] < 0.001:
                convergence[actual_page] = True
            else :
                convergence[actual_page] = False
        
        if all(value == True for value in convergence.values()):
            return final_dict
        else:
            final_dict = iterate_pagerank(corpus, damping_factor, final_dict)

    else:
        final_dict = {}

        for actual_page in corpus:
            final_dict[actual_page] = 1/N
    
        final_dict = iterate_pagerank(corpus, damping_factor, final_dict)
    
    return final_dict

if __name__ == "__main__":
    main()
