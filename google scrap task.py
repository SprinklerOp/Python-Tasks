import googlesearch

def scrape_google(query, num_results=4):
    search_results = []
    for result in googlesearch.search(query, num_results=num_results):
        search_results.append(result)
    return search_results

query = input("your search query:")
num_results = 4
search_results = scrape_google(query, num_results)

print("Top 5 search results:")
for idx, result in enumerate(search_results, start=1):
    print(f"{idx}. {result}")
