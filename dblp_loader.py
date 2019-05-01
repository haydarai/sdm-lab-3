import pandas as pd
import re
import lorem
from gensim.utils import deaccent
from nameparser import HumanName
import nltk
import geograpy
import spacy
import random
from collections import Counter


def generate_abstract(row):
    return lorem.paragraph()


def generate_textual_description(row):
    return lorem.sentence()


def is_corresponding(author):
    last_name = author.last_name.split()
    if last_name:
        return deaccent(last_name[-1]) in deaccent(author.key)
    return False


def get_author_uri(full_name):
    full_name = re.sub(r'\d+', '', full_name)
    last_name = re.sub(' ', '_', HumanName(full_name).last)
    first_name = HumanName(full_name).first
    if (first_name):
        return 'https://dblp.org/db/' + 'pers/' + HumanName(full_name).last + '_' + HumanName(full_name).first[0]
    return 'https://dblp.org/db/' + 'pers/' + HumanName(full_name).last


def extract_last_name(full_name):
    full_name = re.sub(r'\d+', '', full_name)
    return HumanName(full_name).last


def remove_numbers_from_name(name):
    return re.sub(r'\d+', '', name)


def extract_venue(title):
    places = geograpy.get_place_context(text=title).cities
    if places:
        return ','.join(places)
    else:
        return None


def generate_conference_dates(conference):
    conference['start_date'] = str(conference['year']) + '-01-01'
    conference['end_date'] = str(conference['year']) + '-01-02'
    return conference


def get_conference_uri(conference):
    return 'https://dblp.org/db/' + conference['crossref'].split('-')[0]


def get_journal_uri(journal):
    keys = journal['key'].split('/')
    return 'https://dblp.org/db/' + keys[0] + '/' + keys[1] + '/' + str(journal['year']) + '/' + str(journal['volume'])


def get_paper_uri(paper):
    return 'https://dblp.org/db/' + paper['key']


def get_conference_uri_from_paper(paper):
    paper_keys = paper['key'].split('/')
    paper_keys = paper_keys[:-1]
    return '/'.join(paper_keys) + '/' + str(paper['year'])


def get_journal_uri_from_paper(paper):
    paper_keys = paper['key'].split('/')
    paper_keys = paper_keys[:-1]
    return '/'.join(paper_keys) + '/' + str(paper['year']) + '/' + str(paper['volume'])


def get_school_uri(name):
    name = name.split(',')[0]
    name = re.sub(r' ', '_', name)
    return 'https://dblp.org/db/' + 'schools/' + name


def generate_journal_date(journal):
    return str(journal['year']) + '-01-01'


class DBLP_Loader():

    def __init__(self, *args, **kwargs):
        nltk.downloader.download('averaged_perceptron_tagger', quiet=True)
        nltk.downloader.download('maxent_ne_chunker', quiet=True)
        nltk.downloader.download('words', quiet=True)
        nltk.downloader.download('treebank', quiet=True)
        nltk.downloader.download('maxent_treebank_pos_tagger', quiet=True)
        nltk.downloader.download('punkt', quiet=True)

        self.nlp = spacy.load('en')
        self.all_keywords = []
        self.papers = []
        self.schools = []
        return super().__init__(*args, **kwargs)

    def extract_keyword_from_title(self, title):
        keywords = []
        for token in self.nlp(title):
            if token.pos_ == "NOUN":
                keywords.append(token.lower_)
        self.all_keywords.extend(keywords)
        return keywords

    def randomize_keyword(self, keywords):
        if not keywords:
            return random.choices(self.all_keywords, k=5)
        elif len(keywords) < 5:
            remaining = 5 - len(keywords)
            return keywords + list(set(random.choices(self.all_keywords, k=remaining)) - set(keywords))
        else:
            return keywords

    def get_random_reviewers(self, authors, reviewers):
        current_authors = set(authors)
        filtered_reviewers = list(
            filter(lambda x: x not in current_authors, reviewers))
        return random.choices(filtered_reviewers, k=3)

    def get_random_cited_by(self, paper):
        current_paper = set(paper)
        filtered_papers = list(
            filter(lambda x: x not in paper, self.papers))
        k = random.randint(1, 10)
        return random.choices(filtered_papers, k=k)

    def extract_conferences(self):
        print('Extracting conferences...')
        df = pd.read_csv('input/output_inproceedings.csv',
                         delimiter=';', nrows=10000, error_bad_lines=False)

        df_proceedings = pd.read_csv('input/output_proceedings.csv',
                                     delimiter=';', nrows=10000)

        df_proceedings = df_proceedings.dropna(axis=1, how='all')

        # Extract useful columns
        df_proceedings = df_proceedings[['booktitle', 'title']]

        # Drop duplicates of conference title
        df_proceedings = df_proceedings.drop_duplicates(
            ['booktitle'], keep='first')

        # Drop rows with any null value in defined columns
        df_proceedings = df_proceedings.dropna(subset=['booktitle', 'title'])

        df_proceedings['venue'] = df_proceedings['title'].apply(extract_venue)

        # Drop rows with no venue information
        df_proceedings = df_proceedings.dropna(subset=['venue'])
        df_proceedings = df_proceedings[['booktitle', 'venue']]
        df_proceedings = df_proceedings.rename(columns={'booktitle': 'title'})

        # Drop columns with no value
        df = df.dropna(axis=1, how='all')
        df = df[df['crossref'].str.contains('conf/')]

        # Extract useful columns
        df = df[['crossref', 'booktitle', 'year']]
        df['crossref'] = df.apply(get_conference_uri, axis=1)

        # Drop rows with incomplete information
        df = df.drop_duplicates()

        # Ignoring rows with non-numerical value in year column
        df['year'] = pd.to_numeric(df['year'], errors='coerce')

        # Drop rows with any null value in defined columns
        df = df.dropna(subset=['booktitle', 'year'])
        df = df.apply(generate_conference_dates, axis=1)
        df = df.rename(columns={'crossref': 'uri', 'booktitle': 'title', })

        df = pd.merge(df, df_proceedings, on='title', how='left')
        df['num_of_reviewers'] = 3

        df.to_csv('output/conferences.csv',
                  sep=',', index=False)
        print('Conferences extracted.')

    def extract_journals(self):
        print('Extracting journals...')
        df = pd.read_csv('input/output_article.csv',
                         delimiter=';', nrows=10000, error_bad_lines=False)
        df = df.dropna(axis=1, how='all')
        df = df[df['key'].str.contains('journals/')]
        df = df[['key', 'journal', 'year', 'volume', 'mdate']]

        # Ignoring rows with non-numerical value in year column
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df = df.sort_values(by=['mdate'], ascending=False, na_position='last')
        df = df.drop_duplicates(['journal', 'year', 'volume'], keep='first')
        df = df.drop('mdate', axis=1)

        # Drop rows with any null value in defined columns
        df = df.dropna(subset=['key', 'journal', 'year', 'volume'])
        df['key'] = df.apply(get_journal_uri, axis=1)
        df['date'] = df.apply(generate_journal_date, axis=1)
        df = df.rename(columns={'key': 'uri'})
        df['num_of_reviewers'] = 3

        df.to_csv('output/journals.csv',
                  sep=',', index=False)
        print('Journals extracted.')

    def extract_conference_papers(self):
        print('Extracting conference papers...')
        df = pd.read_csv('input/output_inproceedings.csv',
                         delimiter=';', nrows=10000, error_bad_lines=False)

        # Drop columns with no value
        df = df.dropna(axis=1, how='all')
        df = df[df['key'].str.contains('conf/')]
        df['key'] = df.apply(get_paper_uri, axis=1)

        # Extract useful columns
        df = df[['key', 'title', 'booktitle', 'year', 'mdate']]

        df = df.sort_values(by=['mdate'], ascending=False, na_position='last')
        df = df.drop_duplicates(['key', 'title'], keep='first')
        df = df.drop('mdate', axis=1)

        # Drop rows with any null value in defined columns
        df = df.dropna(subset=['key', 'title', 'booktitle', 'year'])

        # Generate random abstract
        df['abstract'] = df.apply(generate_abstract, axis=1)

        # Extract keywords
        df['keywords'] = df['title'].apply(self.extract_keyword_from_title)

        # Get top 20 keywords to fill in papers without any keyword
        self.all_keywords = Counter(self.all_keywords)
        self.all_keywords = self.all_keywords.most_common(20)
        self.all_keywords = pd.DataFrame(self.all_keywords, columns=[
            'keyword', 'occurence'])
        self.all_keywords = self.all_keywords['keyword'].tolist()

        # Randomize kwyword insertion to papers without any keyword
        df['keywords'] = df['keywords'].apply(self.randomize_keyword)
        df_keywords = df.set_index(['key']).keywords.apply(pd.Series).stack(
        ).reset_index(name='keyword').drop('level_1', axis=1)
        df = df.drop('keywords', axis=1)

        df['conference_uri'] = df.apply(get_conference_uri_from_paper, axis=1)
        df = df.drop(['booktitle', 'year'], axis=1)
        df = df.rename(columns={'key': 'uri'})
        df_keywords = df_keywords.rename(columns={'key': 'uri'})

        df.to_csv('output/conference_papers.csv',
                  sep=',', index=False)
        df_keywords.to_csv('output/conference_paper_keywords.csv',
                           sep=',', index=False)
        print('Conference papers extracted.')

    def extract_journal_papers(self):
        print('Extracting journal papers...')
        df = pd.read_csv('input/output_article.csv',
                         delimiter=';', nrows=10000, error_bad_lines=False)

        # Drop columns with no value
        df = df.dropna(axis=1, how='all')
        df = df[df['key'].str.contains('journals/')]
        df['key'] = df.apply(get_paper_uri, axis=1)

        # Extract useful columns
        df = df[['key', 'title', 'journal', 'year', 'volume', 'mdate']]

        df = df.sort_values(by=['mdate'], ascending=False, na_position='last')
        df = df.drop_duplicates(['key', 'title'], keep='first')
        df = df.drop('mdate', axis=1)

        # Drop rows with any null value in defined columns
        df = df.dropna(subset=['key', 'title', 'journal', 'year', 'volume'])

        # Generate random abstract
        df['abstract'] = df.apply(generate_abstract, axis=1)

        # Extract keywords
        df['keywords'] = df['title'].apply(self.extract_keyword_from_title)

        # Get top 20 keywords to fill in papers without any keyword
        self.all_keywords = Counter(self.all_keywords)
        self.all_keywords = self.all_keywords.most_common(20)
        self.all_keywords = pd.DataFrame(self.all_keywords, columns=[
            'keyword', 'occurence'])
        self.all_keywords = self.all_keywords['keyword'].tolist()

        # Randomize kwyword insertion to papers without any keyword
        df['keywords'] = df['keywords'].apply(self.randomize_keyword)
        df_keywords = df.set_index(['key']).keywords.apply(pd.Series).stack(
        ).reset_index(name='keyword').drop('level_1', axis=1)

        df = df.drop('keywords', axis=1)
        df['journal_uri'] = df.apply(get_journal_uri_from_paper, axis=1)
        df = df.drop(['journal', 'year', 'volume'], axis=1)
        df = df.rename(columns={'key': 'uri'})
        df_keywords = df_keywords.rename(columns={'key': 'uri'})

        df.to_csv('output/journal_papers.csv',
                  sep=',', index=False)
        df_keywords.to_csv('output/journal_paper_keywords.csv',
                           sep=',', index=False)
        print('Journal papers extracted.')

    def extract_conference_authors(self):
        print('Extracting authors from conference papers...')
        df = pd.read_csv('input/output_inproceedings.csv',
                         delimiter=';', nrows=10000,
                         error_bad_lines=False)

        # Drop columns with no value
        df = df.dropna(axis=1, how='all')

        # Extract useful columns
        df = df[['author', 'key']]
        df = df.drop_duplicates()

        df = df[df['key'].str.contains('conf/')]

        df['author'] = df['author'].str.split('|')

        df = df.set_index(['key']).author.apply(pd.Series).stack(
        ).reset_index(name='author').drop('level_1', axis=1)

        df['author'] = df['author'].apply(remove_numbers_from_name)
        df['last_name'] = df['author'].apply(extract_last_name)
        df['is_corresponding'] = df.apply(is_corresponding, axis=1)

        df['paper_uri'] = df.apply(get_paper_uri, axis=1)
        df['author_uri'] = df['author'].apply(get_author_uri)

        df_corresponding = df[df['is_corresponding'] == True]
        df_non_corresponding = df[df['is_corresponding'] == False]

        # Extract useful columns
        df_corresponding = df_corresponding[[
            'paper_uri', 'author_uri', 'author']]
        df_non_corresponding = df_non_corresponding[[
            'paper_uri', 'author_uri', 'author']]

        # Drop duplicates
        df_corresponding = df_corresponding.drop_duplicates(
            ['paper_uri'], keep='first')
        df_non_corresponding = df_non_corresponding.drop_duplicates(
            ['paper_uri', 'author'], keep='first')

        df_corresponding.to_csv('output/corresponding_conference_authors.csv',
                                sep=',', index=False)
        df_non_corresponding.to_csv('output/non_corresponding_conference_authors.csv',
                                    sep=',', index=False)
        print('Authors from conference papers extracted.')

    def extract_journal_authors(self):
        print('Extracting authors from journal papers...')
        df = pd.read_csv('input/output_article.csv',
                         delimiter=';', nrows=10000,
                         error_bad_lines=False)

        # Drop columns with no value
        df = df.dropna(axis=1, how='all')

        # Extract useful columns
        df = df[['author', 'key']]
        df = df.drop_duplicates()

        df = df[df['key'].str.contains('journals/')]

        df['author'] = df['author'].str.split('|')

        df = df.set_index(['key']).author.apply(pd.Series).stack(
        ).reset_index(name='author').drop('level_1', axis=1)

        df['author'] = df['author'].apply(remove_numbers_from_name)
        df['last_name'] = df['author'].apply(extract_last_name)
        df['is_corresponding'] = df.apply(is_corresponding, axis=1)

        df['paper_uri'] = df.apply(get_paper_uri, axis=1)
        df['author_uri'] = df['author'].apply(get_author_uri)

        df_corresponding = df[df['is_corresponding'] == True]
        df_non_corresponding = df[df['is_corresponding'] == False]

        # Extract useful columns
        df_corresponding = df_corresponding[[
            'paper_uri', 'author_uri', 'author']]
        df_non_corresponding = df_non_corresponding[[
            'paper_uri', 'author_uri', 'author']]

        # Drop duplicates
        df_corresponding = df_corresponding.drop_duplicates(
            ['paper_uri'], keep='first')
        df_non_corresponding = df_non_corresponding.drop_duplicates(
            ['paper_uri', 'author'], keep='first')

        df_corresponding.to_csv('output/corresponding_journal_authors.csv',
                                sep=',', index=False)
        df_non_corresponding.to_csv('output/non_corresponding_journal_authors.csv',
                                    sep=',', index=False)

        # df.to_csv('output/journal_authors.csv',
        #           sep=',', index=False)
        print('Authors from journal papers extracted.')

    def extract_schools(self):
        print('Extracting schools...')
        df = pd.read_csv('input/output_school.csv', delimiter=';', nrows=10000,
                         usecols={'school:string'},
                         dtype={'school:string': str})
        df = df.drop_duplicates(['school:string'])
        df['uri'] = df['school:string'].apply(get_school_uri)
        df = df.rename(columns={'school:string': 'name'})

        df.to_csv('output/schools.csv',
                  sep=',', index=False)
        print('Schools extracted.')

    def generate_random_author_schools(self):
        print("Generating random author's schools")

        df_corresponding_conference_authors = pd.read_csv(
            'output/corresponding_conference_authors.csv', delimiter=',', nrows=10000)
        df_corresponding_conference_authors = df_corresponding_conference_authors[[
            'author_uri']]
        df_corresponding_conference_authors['author_uri'] = df_corresponding_conference_authors[
            'author_uri']

        df_corresponding_journal_authors = pd.read_csv(
            'output/corresponding_journal_authors.csv', delimiter=',', nrows=10000)
        df_corresponding_journal_authors = df_corresponding_journal_authors[[
            'author_uri']]
        df_corresponding_journal_authors['author_uri'] = df_corresponding_journal_authors['author_uri']

        df_non_corresponding_conference_authors = pd.read_csv(
            'output/non_corresponding_conference_authors.csv', delimiter=',', nrows=10000)
        df_non_corresponding_conference_authors = df_non_corresponding_conference_authors[[
            'author_uri']]
        df_non_corresponding_conference_authors['author_uri'] = df_non_corresponding_conference_authors[
            'author_uri']

        df_non_corresponding_journal_authors = pd.read_csv(
            'output/non_corresponding_journal_authors.csv', delimiter=',', nrows=10000)
        df_non_corresponding_journal_authors = df_non_corresponding_journal_authors[[
            'author_uri']]
        df_non_corresponding_journal_authors['author_uri'] = df_non_corresponding_journal_authors[
            'author_uri']

        df = pd.concat([df_corresponding_conference_authors, df_corresponding_journal_authors,
                        df_non_corresponding_conference_authors, df_non_corresponding_journal_authors])
        df = df.drop_duplicates()
        df = pd.DataFrame(df)

        df_schools = pd.read_csv('output/schools.csv',
                                 delimiter=',', nrows=10000)
        df_schools = df_schools[['uri']]

        df_schools = df_schools.drop_duplicates(['uri'])
        self.schools = df_schools['uri'].tolist()
        df['school_uri'] = df['author_uri'].apply(
            lambda author: random.choice(self.schools))

        df.to_csv('output/author_schools.csv',
                  sep=',', index=False)
        print("Author's affiliations generated.")

    def generate_random_conference_reviewers(self):
        print("Generating random conference's reviewers")
        df = pd.read_csv('input/output_inproceedings.csv',
                         delimiter=';', nrows=10000, error_bad_lines=False)

        # Drop columns with no value
        df = df.dropna(axis=1, how='all')

        df = df.dropna(subset=['author'])
        df = df[df['key'].str.contains('conf/')]

        df_authors = df[['author', 'key']]
        df_authors = df_authors.drop_duplicates()

        df_authors['author'] = df_authors['author'].str.split('|')

        df_authors_all = df_authors.set_index(['key']).author.apply(
            pd.Series).stack().reset_index(name='author').drop('level_1', axis=1)
        df_authors_all['author'] = df_authors_all['author'].apply(
            remove_numbers_from_name)

        authors = df_authors_all['author'].tolist()

        df_authors['reviewer'] = df_authors['author'].apply(
            lambda author: self.get_random_reviewers(author, authors))
        df_authors = df_authors.set_index(['key']).reviewer.apply(
            pd.Series).stack().reset_index(name='reviewer').drop('level_1', axis=1)
        df_authors['reviewer'] = df_authors['reviewer'].apply(
            remove_numbers_from_name)

        df_authors['reviewer_uri'] = df_authors['reviewer'].apply(
            get_author_uri)
        df_authors['paper_uri'] = df_authors.apply(get_paper_uri, axis=1)

        df_authors = df_authors.drop(['reviewer', 'key'], axis=1)

        df_authors['textual_description'] = df_authors.apply(
            generate_textual_description, axis=1)
        df_authors['accept'] = True

        df_authors.to_csv('output/conference_paper_reviewers.csv',
                          sep=',', index=False)

        print("Conference's reviewers generated.")

    def generate_random_journal_reviewers(self):
        print("Generating random journal's reviewers")
        df = pd.read_csv('input/output_article.csv',
                         delimiter=';', nrows=10000, error_bad_lines=False)

        # Drop columns with no value
        df = df.dropna(axis=1, how='all')

        df = df.dropna(subset=['author'])
        df = df[df['key'].str.contains('journals/')]

        df_authors = df[['author', 'key']]
        df_authors = df_authors.drop_duplicates()

        df_authors['author'] = df_authors['author'].str.split('|')

        df_authors_all = df_authors.set_index(['key']).author.apply(
            pd.Series).stack().reset_index(name='author').drop('level_1', axis=1)
        df_authors_all['author'] = df_authors_all['author'].apply(
            remove_numbers_from_name)

        authors = df_authors_all['author'].tolist()

        df_authors['reviewer'] = df_authors['author'].apply(
            lambda author: self.get_random_reviewers(author, authors))
        df_authors = df_authors.set_index(['key']).reviewer.apply(
            pd.Series).stack().reset_index(name='reviewer').drop('level_1', axis=1)
        df_authors['reviewer'] = df_authors['reviewer'].apply(
            remove_numbers_from_name)

        df_authors['reviewer_uri'] = df_authors['reviewer'].apply(
            get_author_uri)
        df_authors['paper_uri'] = df_authors.apply(get_paper_uri, axis=1)

        df_authors = df_authors.drop(['reviewer', 'key'], axis=1)

        df_authors['textual_description'] = df_authors.apply(
            generate_textual_description, axis=1)
        df_authors['accept'] = True

        df_authors.to_csv('output/journal_paper_reviewers.csv',
                          sep=',', index=False)

        print("Journal's reviewers generated.")

    def generate_random_citations(self):
        print("Generating random citations")
        df_conference_papers = pd.read_csv(
            'output/conference_papers.csv', sep=',')
        df_journal_papers = pd.read_csv(
            'output/journal_papers.csv', sep=',')

        df_conference_papers = df_conference_papers[['uri']]
        df_journal_papers = df_journal_papers[['uri']]

        df = pd.concat([df_conference_papers, df_journal_papers])

        self.papers = df['uri'].tolist()
        df['cited_by'] = df['uri'].apply(
            lambda paper: self.get_random_cited_by(paper))
        df = df.set_index(['uri']).cited_by.apply(
            pd.Series).stack().reset_index(name='cited_by').drop('level_1', axis=1)

        df.to_csv('output/paper_citations.csv',
                  sep=',', index=False)
