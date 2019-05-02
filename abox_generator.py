import pandas as pd
from rdflib import Graph, URIRef, BNode, Literal, XSD, RDFS, Namespace


class ABox_Generator():
    def __init__(self, *args, **kwargs):
        self.graph = Graph()
        return super().__init__(*args, **kwargs)

    def create_schools(self):
        print('Creating schools tuples...')
        df = pd.read_csv('output/schools.csv')
        for index, row in df.iterrows():
            school_uri = URIRef(row['uri'])
            school_name = Literal(row['name'], datatype=XSD.string)
            self.graph.add((school_uri, RDFS.label, school_name))

        print('Schools tuples created.')

    def create_conferences(self):
        print('Creating conferences tuples...')
        df = pd.read_csv('output/conferences.csv')

        dblp_ns = Namespace('https://dblg.org/ontologies/')

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
            self.graph.add((conference_uri, dblp_ns.duration, duration))
            self.graph.add((conference_uri, dblp_ns.venue, venue))
            self.graph.add(
                (conference_uri, dblp_ns.numOfReviewers, num_of_reviewers))

        print('Conferences tuples created.')

    def create_journals(self):
        print('Creating journals tuples...')
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

        print('Journals tuples created.')

    def create_author_names(self):
        print('Creating author names tuples...')
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

        print('Author names tuples created.')

    def save(self):
        self.graph.serialize(destination='output/graph.nt')
        print('Graph saved as graph.nt')
