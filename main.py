from dotenv import load_dotenv
import argparse
from dblp_loader import DBLP_Loader
from abox_generator import ABox_Generator
from graph_linker import Graph_Linker

load_dotenv()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--parse', action='store_true')
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--link', action='store_true')
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
        print("Files necessary for creating ABOX are ready.")
    elif args.generate:
        abox_generator = ABox_Generator()
        abox_generator.create_schools()
        abox_generator.create_author_names()
        abox_generator.create_author_schools()
        abox_generator.create_conferences()
        abox_generator.create_journals()
        abox_generator.create_conference_papers()
        abox_generator.create_journal_papers()
        abox_generator.create_conference_paper_keywords()
        abox_generator.create_journal_paper_keywords()
        abox_generator.create_conference_paper_reviewers()
        abox_generator.create_journal_paper_reviewers()
        abox_generator.create_conference_paper_corresponding_authors()
        abox_generator.create_journal_paper_corresponding_authors()
        abox_generator.create_conference_paper_non_corresponding_authors()
        abox_generator.create_journal_paper_non_corresponding_authors()
        abox_generator.create_paper_citations()
        abox_generator.save()
    elif args.link:
        graph_linker = Graph_Linker()
        graph_linker.link_authors()
        graph_linker.link_papers()
        graph_linker.link_reviewers()
        graph_linker.link_schools()
        graph_linker.link_journals()
        graph_linker.link_conferences()
        graph_linker.link_random_open_access_journals()
        graph_linker.link_random_close_access_journals()
        graph_linker.link_algorithm_conferences()
        graph_linker.link_network_conferences()
        graph_linker.link_database_conferences()
