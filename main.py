from dotenv import load_dotenv
import argparse
from neo4j_loader import Neo4J_Loader
from dblp_loader import DBLP_Loader
from query_runner import Query_Runner

load_dotenv()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--parse', action='store_true')
    parser.add_argument('--load', action='store_true')
    parser.add_argument('--evolve', action='store_true')
    parser.add_argument('--recommend')
    parser.add_argument('--gurus', type=int)
    args = parser.parse_args()

    if args.parse:
        file_loader = DBLP_Loader()
        file_loader.extract_conferences()
        file_loader.extract_journals()
        file_loader.extract_conference_papers()
        file_loader.extract_journal_papers()
        file_loader.extract_conference_authors()
        file_loader.extract_journal_authors()
        file_loader.generate_random_citations()
        file_loader.generate_random_conference_reviewers()
        file_loader.generate_random_journal_reviewers()
        file_loader.extract_schools()
        file_loader.generate_random_author_schools()
        print("Copy files generated in 'output' folder to '/var/lib/neo4j/import'")
    elif args.recommend and args.gurus:
        keywords = """['data', 'database', 'management', 'olap', 'postgres', 'xml', 'relational', 'queries', 'sql']"""
        query_runner = Query_Runner()
        publications = query_runner.get_publication_communities(args.recommend)
        papers = query_runner.get_top_papers(publications)
        gurus = query_runner.get_gurus(papers, args.gurus)
        print('Gurus:')
        print(gurus)
    elif args.recommend:
        query_runner = Query_Runner()
        publications = query_runner.get_publication_communities(args.recommend)
        papers = query_runner.get_top_papers(publications)
        authors = query_runner.get_authors(papers)
        print('Recommended reviewers:')
        print(authors)
