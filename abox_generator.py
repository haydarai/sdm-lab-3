import uuid
import pandas as pd
from rdflib import Graph, URIRef, BNode, Literal, XSD, RDFS, Namespace


class ABox_Generator():
    def __init__(self, *args, **kwargs):
        self.graph = Graph()
        return super().__init__(*args, **kwargs)

    def create_schools(self):
        print('Creating schools triples...')
        df = pd.read_csv('output/schools.csv')
        for index, row in df.iterrows():
            school_uri = URIRef(row['uri'])
            school_name = Literal(row['name'], datatype=XSD.string)
            self.graph.add((school_uri, RDFS.label, school_name))

        print('Schools triples created.')

    def create_conferences(self):
        print('Creating conferences triples...')
        df = pd.read_csv('output/conferences.csv')

        dblp_ns = Namespace('https://dblg.org/ontologies/')
        dbpedia_ns = Namespace('https://dbpedia.org/ontology/')

        for index, row in df.iterrows():
            conference_uri = URIRef(row['uri'])
            title = Literal(row['title'], datatype=XSD.string)
            edition = Literal(row['year'], datatype=XSD.string)
            date = Literal(row['date'], datatype=XSD.dateTime)
            duration = Literal(row['duration'], datatype=XSD.string)
            venue = Literal(row['venue'], datatype=XSD.string)
            num_of_reviewers = Literal(
                row['num_of_reviewers'], datatype=XSD.integer)
            self.graph.add((conference_uri, dblp_ns.title, title))
            self.graph.add((conference_uri, dblp_ns.edition, edition))
            self.graph.add((conference_uri, dblp_ns.date, date))
            self.graph.add((conference_uri, dbpedia_ns.duration, duration))
            self.graph.add((conference_uri, dblp_ns.venue, venue))
            self.graph.add(
                (conference_uri, dblp_ns.numOfReviewers, num_of_reviewers))

        print('Conferences triples created.')

    def create_journals(self):
        print('Creating journals triples...')
        df = pd.read_csv('output/journals.csv')

        dblp_ns = Namespace('https://dblg.org/ontologies/')

        for index, row in df.iterrows():
            journal_uri = URIRef(row['uri'])
            title = Literal(row['journal'], datatype=XSD.string)
            edition = Literal(row['year'], datatype=XSD.string)
            volume = Literal(row['volume'], datatype=XSD.string)
            date = Literal(row['date'], datatype=XSD.dateTime)
            num_of_reviewers = Literal(
                row['num_of_reviewers'], datatype=XSD.integer)
            self.graph.add((journal_uri, dblp_ns.title, title))
            self.graph.add((journal_uri, dblp_ns.edition, edition))
            self.graph.add((journal_uri, dblp_ns.volume, volume))
            self.graph.add((journal_uri, dblp_ns.date, date))
            self.graph.add(
                (journal_uri, dblp_ns.numOfReviewers, num_of_reviewers))

        print('Journals triples created.')

    def create_conference_papers(self):
        print('Creating conferences triples...')
        df = pd.read_csv('output/conference_papers.csv')

        dblp_ns = Namespace('https://dblg.org/ontologies/')

        for index, row in df.iterrows():
            paper_uri = URIRef(row['uri'])
            title = Literal(row['title'], datatype=XSD.string)
            abstract = Literal(row['abstract'], datatype=XSD.string)
            conference_uri = URIRef(row['conference_uri'])
            self.graph.add((paper_uri, dblp_ns.title, title))
            self.graph.add((paper_uri, dblp_ns.abstract, abstract))
            self.graph.add((paper_uri, dblp_ns.publishedIn, conference_uri))

        print('Conference papers triples created.')

    def create_journal_papers(self):
        print('Creating journal triples...')
        df = pd.read_csv('output/journal_papers.csv')

        dblp_ns = Namespace('https://dblg.org/ontologies/')

        for index, row in df.iterrows():
            paper_uri = URIRef(row['uri'])
            title = Literal(row['title'], datatype=XSD.string)
            abstract = Literal(row['abstract'], datatype=XSD.string)
            journal_uri = URIRef(row['journal_uri'])
            self.graph.add((paper_uri, dblp_ns.title, title))
            self.graph.add((paper_uri, dblp_ns.abstract, abstract))
            self.graph.add((paper_uri, dblp_ns.publishedIn, journal_uri))

        print('Journal papers triples created.')

    def create_conference_paper_keywords(self):
        print('Creating journal paper keywords triples...')
        df = pd.read_csv('output/conference_paper_keywords.csv')

        dblp_ns = Namespace('https://dblg.org/ontologies/')

        for index, row in df.iterrows():
            paper_uri = URIRef(row['uri'])
            keyword = Literal(row['keyword'], datatype=XSD.string)
            self.graph.add((paper_uri, dblp_ns.keyword, keyword))

        print('Journal paper keywords triples created.')

    def create_journal_paper_keywords(self):
        print('Creating journal paper keywords triples...')
        df = pd.read_csv('output/journal_paper_keywords.csv')

        dblp_ns = Namespace('https://dblg.org/ontologies/')

        for index, row in df.iterrows():
            paper_uri = URIRef(row['uri'])
            keyword = Literal(row['keyword'], datatype=XSD.string)
            self.graph.add((paper_uri, dblp_ns.keyword, keyword))

        print('Journal paper keywords triples created.')

    def create_conference_paper_reviewers(self):
        print('Creating journal paper reviewers triples...')
        df = pd.read_csv('output/conference_paper_reviewers.csv')

        dblp_ns = Namespace('https://dblg.org/ontologies/')

        for index, row in df.iterrows():
            reviewer_uri = URIRef(row['reviewer_uri'])
            paper_uri = URIRef(row['paper_uri'])
            textual_description = Literal(
                row['textual_description'], datatype=XSD.string)
            accept = Literal('true', datatype=XSD.boolean)
            review_uri = URIRef(
                'https://dblg.org/db/reviews/' + uuid.uuid4().hex)
            self.graph.add((reviewer_uri, dblp_ns.writeReview, review_uri))
            self.graph.add((review_uri, dblp_ns.about, paper_uri))
            self.graph.add(
                (review_uri, dblp_ns.textualDescription, textual_description))
            self.graph.add((review_uri, dblp_ns.accept, accept))

        print('Journal paper reviewers triples created.')

    def create_journal_paper_reviewers(self):
        print('Creating journal paper reviewers triples...')
        df = pd.read_csv('output/journal_paper_reviewers.csv')

        dblp_ns = Namespace('https://dblg.org/ontologies/')

        for index, row in df.iterrows():
            reviewer_uri = URIRef(row['reviewer_uri'])
            paper_uri = URIRef(row['paper_uri'])
            textual_description = Literal(
                row['textual_description'], datatype=XSD.string)
            accept = Literal('true', datatype=XSD.boolean)
            review_uri = URIRef(
                'https://dblg.org/db/reviews/' + uuid.uuid4().hex)
            self.graph.add((reviewer_uri, dblp_ns.writeReview, review_uri))
            self.graph.add((review_uri, dblp_ns.about, paper_uri))
            self.graph.add(
                (review_uri, dblp_ns.textualDescription, textual_description))
            self.graph.add((review_uri, dblp_ns.accept, accept))

        print('Journal paper reviewers triples created.')

    def create_conference_paper_corresponding_authors(self):
        print('Creating corresponding authors for conference papers triples...')
        df = pd.read_csv('output/corresponding_conference_authors.csv')

        dblp_ns = Namespace('https://dblg.org/ontologies/')

        for index, row in df.iterrows():
            author_uri = URIRef(row['author_uri'])
            paper_uri = URIRef(row['paper_uri'])
            self.graph.add((author_uri, dblp_ns.write, paper_uri))
            self.graph.add((paper_uri, dblp_ns.correspondingAuthor, author_uri))

        print('Corresponding authors for conference papers triples created.')

    def create_journal_paper_corresponding_authors(self):
        print('Creating corresponding authors for journal papers triples...')
        df = pd.read_csv('output/corresponding_journal_authors.csv')

        dblp_ns = Namespace('https://dblg.org/ontologies/')

        for index, row in df.iterrows():
            author_uri = URIRef(row['author_uri'])
            paper_uri = URIRef(row['paper_uri'])
            self.graph.add((author_uri, dblp_ns.write, paper_uri))
            self.graph.add((paper_uri, dblp_ns.correspondingAuthor, author_uri))

        print('Corresponding authors for journal papers triples created.')

    def create_conference_paper_non_corresponding_authors(self):
        print('Creating non corresponding authors for conference papers triples...')
        df = pd.read_csv('output/non_corresponding_conference_authors.csv')

        dblp_ns = Namespace('https://dblg.org/ontologies/')

        for index, row in df.iterrows():
            author_uri = URIRef(row['author_uri'])
            paper_uri = URIRef(row['paper_uri'])
            self.graph.add((author_uri, dblp_ns.write, paper_uri))

        print('Non corresponding authors for conference papers triples created.')

    def create_journal_paper_non_corresponding_authors(self):
        print('Creating non corresponding authors for journal papers triples...')
        df = pd.read_csv('output/non_corresponding_journal_authors.csv')

        dblp_ns = Namespace('https://dblg.org/ontologies/')

        for index, row in df.iterrows():
            author_uri = URIRef(row['author_uri'])
            paper_uri = URIRef(row['paper_uri'])
            self.graph.add((author_uri, dblp_ns.write, paper_uri))

        print('Non corresponding authors for journal papers triples created.')

    def create_author_names(self):
        print('Creating author names triples...')
        df_corresponding_conference_authors = pd.read_csv(
            'output/corresponding_conference_authors.csv')
        df_corresponding_conference_authors = df_corresponding_conference_authors[[
            'author_uri', 'author']]

        df_corresponding_journal_authors = pd.read_csv(
            'output/corresponding_journal_authors.csv')
        df_corresponding_journal_authors = df_corresponding_journal_authors[[
            'author_uri', 'author']]

        df_non_corresponding_conference_authors = pd.read_csv(
            'output/non_corresponding_conference_authors.csv')
        df_non_corresponding_conference_authors = df_non_corresponding_conference_authors[[
            'author_uri', 'author']]

        df_non_corresponding_journal_authors = pd.read_csv(
            'output/non_corresponding_journal_authors.csv')
        df_non_corresponding_journal_authors = df_non_corresponding_journal_authors[[
            'author_uri', 'author']]

        df = pd.concat([df_corresponding_conference_authors, df_corresponding_journal_authors,
                        df_non_corresponding_conference_authors, df_non_corresponding_journal_authors])
        df = df.drop_duplicates()
        df = pd.DataFrame(df)

        dbpedia_ns = Namespace('https://dbpedia.org/ontology/')

        for index, row in df.iterrows():
            author_uri = URIRef(row['author_uri'])
            author_name = Literal(row['author'], datatype=XSD.string)
            self.graph.add((author_uri, dbpedia_ns.birthName, author_name))

        print('Author names triples created.')

    def save(self):
        self.graph.serialize(destination='output/graph.nt')
        print('Graph saved as graph.nt')
