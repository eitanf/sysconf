library(readtext)
library(tidytext)
library(textclean)
library(textstem)
library(tidyverse)
library(multidplyr)

toplevel = paste0(Sys.getenv("SYSCONF_HOME"), "/")

all_text <- readtext(paste0(toplevel, "fulltext/*.txt")) %>%
  mutate(doc_id = sub(".txt$", "", doc_id))

#data(stop_words) # Too aggressive, excludes words like "open"

my_stop_words <- c("the", "of", "and", "to", "is", "on", "by", "at", "which", "for", "its", "per", "then",
                   "with", "our", "in", "into", "we", "that", "as", "are", "this", "be", "an", "can", "from",
                   "it", "each", "or", "all", "if", "have", "using", "when", "only", "these", "such", "use",
                   "most", "since", "large", "has", "more", "than", "also", "used", "different", "other",
                   "where", "were", "between", "work", "same", "their", "will", "while", "any", "both", "allow",
                   "over", "example", "there", "here", "they", "may", "case", "since", "most", "because",
                   "et", "cetera", "etc", "some", "do", "thus", "given", "th", "does", "so", "was", "how",
                   "been", "many", "multiple", "without", "after", "due", "under", "through", "out", "once",
                   "must", "every", "note", "therefore", "within", "across", "consider", "about", "means",
                   "possible", "let", "multi", "before", "should", "like", "us", "several", "make", "very",
                   "respecetively", "less", "can", "cannot", "those", "above", "via", "much", "allows", "get",
                   "still", "among", "being", "either", "hence", "able", "whether", "describe", "described",
                   "one", "two", "three", "four", "five", "otherwise", "although", "usage", "always", "never",
                   "would", "up", "down", "not")
conf_stop_words <- c("abstract", "pp", "figure", "fig", "section", "sec", "acm", "ieee", "al", "e.g", "i.e",
                     "proceedings", "conference", "international", "pages", "http", "https", "symposium",
                     "table", "shown", "show", "page", "paper", "article", "usa", "vol", "study", "usenix",
                     "january", "february", "march", "april", "may", "june", "july", "august", "september",
                     "october", "november", "december", "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep",
                     "oct", "nov", "dec", "ii", "iii", "iv", "vi", "vii", "viii", "vix", "gb", "doi.org")

stop_words <- c(my_stop_words, conf_stop_words)

cluster <- new_cluster(parallel::detectCores())
cluster_library(cluster, "textclean")
cluster_library(cluster, "textstem")
cluster_library(cluster, "tidytext")
cluster_library(cluster, "dplyr")

### Clean up words and generate a tidy data structure:

tokens.tidy <- all_text %>%
  partition(cluster) %>%
  mutate(text = gsub("[[:digit:]]+", " ", text)) %>%    # Remove all digits from text
  mutate(text = replace_contraction(text) %>% replace_kern()) %>%
  mutate(text = lemmatize_words(text)) %>%
#  mutate(text = lemmatize_strings(text)) %>%  # Very slow; also, not great ("data" becomes "datum")

  collect() %>%
  as_tibble() %>%
  ungroup()

unigrams <-tokens.tidy %>%
  unnest_tokens(token, text) %>%
  filter(nchar(token) > 1) %>%  # Remove single-character tokens with ambiguous or undefined meaning
  anti_join(data.frame(token = stop_words)) %>%
  count(doc_id, token, sort = TRUE) %>%
  filter(n > 3) # Remove rare words (mostly junk) to make the data size more manageable

bigrams <-tokens.tidy %>%
  unnest_tokens(bigram, text, token = "ngrams", n = 2) %>%
  separate(bigram, c("word1", "word2")) %>%
  filter(nchar(word1) > 1, nchar(word2) > 1) %>%
  filter(!word1 %in% stop_words, !word2 %in% stop_words) %>%
  unite(token, word1, word2, sep = " ") %>%
  count(doc_id, token, sort = TRUE) %>%
  filter(n > 1) # Remove rare words (mostly junk) to make the data size more manageable


rbind(unigrams, bigrams) %>%
  write.csv(paste0(toplevel, "features/tokens.csv"), row.names = FALSE)

