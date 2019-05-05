import os
from SPARQLWrapper import SPARQLWrapper


class Graph_Linker():
    def __init__(self, *args, **kwargs):
        self.sparql = SPARQLWrapper(os.getenv('SPARQL_ENDPOINT'))
        self.sparql.addDefaultGraph(os.getenv('SPARQL_GRAPH'))

        return super().__init__(*args, **kwargs)

    def link_authors(self):
        print('Linking authors...')
        self.sparql.setQuery("""
            PREFIX dblp: <https://dblp.org/ontologies/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            INSERT {
                ?a rdf:type dblp:Author
            }

            WHERE {
                SELECT DISTINCT ?a
                WHERE {
                    ?a dblp:write ?p .
                    FILTER NOT EXISTS {
                        ?a rdf:type dblp:Author
                    }
                }
            }
        """)
        self.sparql.query()
        print('Authors linked to https://dblp.org/ontologies/Author.')

    def link_papers(self):
        print('Linking papers...')
        self.sparql.setQuery("""
            PREFIX dblp: <https://dblp.org/ontologies/>
            PREFIX bibo: <http://purl.org/ontology/bibo/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            INSERT {
                ?p rdf:type bibo:AcademicArticle
            }

            WHERE {
                SELECT DISTINCT ?p
                WHERE {
                    ?a dblp:write ?p .
                    FILTER NOT EXISTS {
                        ?p rdf:type bibo:AcademicArticle
                    }
                }
            }
        """)
        self.sparql.query()
        print('Papers linked to http://purl.org/ontology/bibo/AcademicArticle.')

    def link_reviewers(self):
        print('Linking reviewers...')
        self.sparql.setQuery("""
            PREFIX dblp: <https://dblp.org/ontologies/>
            PREFIX bibo: <http://purl.org/ontology/bibo/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            INSERT {
                ?s rdf:type dblp:Reviewer
            }

            WHERE {
                SELECT DISTINCT ?s
                WHERE {
                    ?s dblp:writeReview ?r .
                    ?r dblp:about ?p .
                    ?p rdf:type bibo:AcademicArticle .
                    FILTER NOT EXISTS {
                        ?s rdf:type dblp:Reviewer
                    }
                }
            }
        """)
        self.sparql.query()
        print('Reviewers linked to https://dblp.org/ontologies/Reviewer.')

    def link_schools(self):
        print('Linking schools...')
        self.sparql.setQuery("""
            PREFIX dblp: <https://dblp.org/ontologies/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            INSERT {
                ?s rdf:type dblp:School
            }

            WHERE {
                SELECT DISTINCT ?s
                WHERE {
                    ?a dblp:affiliatedWith ?s .
                    FILTER ( regex(str(?s), "/schools/" )) .
                    FILTER NOT EXISTS {
                        ?s rdf:type dblp:School
                    }
                }
            }
        """)
        self.sparql.query()
        print('Schools linked to https://dblp.org/ontologies/School.')

    def link_journals(self):
        print('Linking journals...')
        self.sparql.setQuery("""
            PREFIX dblp: <https://dblp.org/ontologies/>
            PREFIX dbo: <https://dbpedia.org/ontology/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            INSERT {
                ?j rdf:type dbo:AcademicJournal
            }

            WHERE {
                SELECT DISTINCT ?j
                WHERE {
                    ?p dblp:publishedIn ?j .
                    FILTER ( regex(str(?s), "/journals/" )) .
                    FILTER NOT EXISTS {
                        ?j rdf:type dbo:AcademicJournal
                    }
                }
            }
        """)
        self.sparql.query()
        print('Journals linked to https://dbpedia.org/ontology/AcademicJournal.')

    def link_conferences(self):
        print('Linking conferences...')
        self.sparql.setQuery("""
            PREFIX dblp: <https://dblp.org/ontologies/>
            PREFIX dbo: <https://dbpedia.org/ontology/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            INSERT {
                ?c rdf:type dbo:AcademicConference
            }

            WHERE {
                SELECT DISTINCT ?c
                WHERE {
                    ?p dblp:publishedIn ?c .
                    FILTER ( regex(str(?c), "/conf/" )) .
                    FILTER NOT EXISTS {
                        ?c rdf:type dbo:AcademicConference
                    }
                }
            }
        """)
        self.sparql.query()
        print('Conferences linked to https://dbpedia.org/ontology/AcademicConference.')

    def link_random_open_access_journals(self):
        print('Generating and linking random open access journals...')
        self.sparql.setQuery("""
            PREFIX dblp: <https://dblp.org/ontologies/>
            PREFIX dbo: <https://dbpedia.org/ontology/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            INSERT {
                ?j rdf:type dblp:OpenAccessJournal
            }

            WHERE {
                SELECT DISTINCT ?j
                WHERE {
                    ?j rdf:type dbo:AcademicJournal .
                    FILTER NOT EXISTS {
                        ?j rdf:type dblp:OpenAccessJournal .
                        ?j rdf:type dblp:CloseAccessJournal
                    }
                }
                ORDER BY RAND()
                LIMIT 200
            }
        """)
        self.sparql.query()
        print('Open access journals generated and linked to https://dblp.org/ontologies/OpenAccessJournal.')

    def link_random_close_access_journals(self):
        print('Generating and linking random close access journals...')
        self.sparql.setQuery("""
            PREFIX dblp: <https://dblp.org/ontologies/>
            PREFIX dbo: <https://dbpedia.org/ontology/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            INSERT {
                ?j rdf:type dblp:CloseAccessJournal
            }

            WHERE {
                SELECT DISTINCT ?j
                WHERE {
                    ?j rdf:type dbo:AcademicJournal .
                    FILTER NOT EXISTS {
                        ?j rdf:type dblp:OpenAccessJournal .
                        ?j rdf:type dblp:CloseAccessJournal
                    }
                }
                ORDER BY RAND()
                LIMIT 200
            }
        """)
        self.sparql.query()
        print('Close access journals generated and linked to https://dblp.org/ontologies/CloseAccessJournal.')

    def link_algorithm_conferences(self):
        print('Linking algorithm conferences...')
        self.sparql.setQuery("""
            PREFIX dblp: <https://dblp.org/ontologies/>
            PREFIX dbo: <https://dbpedia.org/ontology/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            INSERT {
                ?c rdf:type dblp:AlgorithmConference
            }

            WHERE {
                SELECT DISTINCT ?c
                WHERE {
                    ?c rdf:type dbo:AcademicConference .
                    ?p dblp:publishedIn ?c .
                    ?p dblp:keyword ?k .
                    FILTER(str(?k) IN ('algorithm')) .
                    FILTER NOT EXISTS {
                        ?c rdf:type dblp:AlgorithmConference
                    }
                }
            }
        """)
        self.sparql.query()
        print('Algorithm conferences linked to https://dblp.org/ontologies/AlgorithmConference.')

    def link_network_conferences(self):
        print('Linking network conferences...')
        self.sparql.setQuery("""
            PREFIX dblp: <https://dblp.org/ontologies/>
            PREFIX dbo: <https://dbpedia.org/ontology/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            INSERT {
                ?c rdf:type dblp:NetworkConference
            }

            WHERE {
                SELECT DISTINCT ?c
                WHERE {
                    ?c rdf:type dbo:AcademicConference .
                    ?p dblp:publishedIn ?c .
                    ?p dblp:keyword ?k .
                    FILTER(str(?k) IN ('network', 'networks', 'cloud', 'internet', 'wlans')) .
                    FILTER NOT EXISTS {
                        ?c rdf:type dblp:NetworkConference
                    }
                }
            }
        """)
        self.sparql.query()
        print(
            'Network conferences linked to https://dblp.org/ontologies/NetworkConference.')

    def link_database_conferences(self):
        print('Linking database conferences...')
        self.sparql.setQuery("""
            PREFIX dblp: <https://dblp.org/ontologies/>
            PREFIX dbo: <https://dbpedia.org/ontology/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            INSERT {
                ?c rdf:type dblp:DatabaseConference
            }

            WHERE {
                SELECT DISTINCT ?c
                WHERE {
                    ?c rdf:type dbo:AcademicConference .
                    ?p dblp:publishedIn ?c .
                    ?p dblp:keyword ?k .
                    FILTER(str(?k) IN ('data', 'database', 'databases')) .
                    FILTER NOT EXISTS {
                        ?c rdf:type dblp:DatabaseConference
                    }
                }
            }
        """)
        self.sparql.query()
        print(
            'Database conferences linked to https://dblp.org/ontologies/DatabaseConference.')
