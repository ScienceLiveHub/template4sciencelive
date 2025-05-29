#!/usr/bin/env python3
"""
Create a nanopublication template for describing scientific papers with comprehensive metadata
using the nanopub-py library and established scholarly ontologies.
"""

import rdflib
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, FOAF
from nanopub import Nanopub, NanopubConf, Profile
from pathlib import Path

# Constructing profile for publishing nanopublications
def create_memory_profile(name: str, orcid_id: str):
    """Create profile entirely in memory without file I/O"""
    profile = Profile(
        name=name,
        orcid_id=orcid_id
    )
    return profile

def create_scientific_paper_template():
    """
    Create a nanopublication template for describing scientific papers
    with comprehensive metadata using established scholarly ontologies.
    """
    
    # Load user profile
    try:
        # Set up Anne Fouilloux's profile
        profile = create_memory_profile(
           name="Anne Fouilloux",
           orcid_id="https://orcid.org/0000-0002-1784-2920"
        )
    except Exception as e:
        print(f"Error loading profile: {e}")
        return None
    
    # Define namespaces
    NP = Namespace("http://www.nanopub.org/nschema#")
    NPX = Namespace("http://purl.org/nanopub/x/")
    NT = Namespace("https://w3id.org/np/o/ntemplate/")
    PROV = Namespace("http://www.w3.org/ns/prov#")
    BIBO = Namespace("http://purl.org/ontology/bibo/")
    DOCO = Namespace("http://purl.org/spar/doco/")
    DEO = Namespace("http://purl.org/spar/deo/")
    CITO = Namespace("http://purl.org/spar/cito/")
    FABIO = Namespace("http://purl.org/spar/fabio/")
    SCHEMA = Namespace("http://schema.org/")
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    
    # Create the assertion graph
    assertion = Graph()
    
    # Bind namespaces
    assertion.bind("np", NP)
    assertion.bind("npx", NPX)
    assertion.bind("nt", NT)
    assertion.bind("prov", PROV)
    assertion.bind("dcterms", DCTERMS)
    assertion.bind("foaf", FOAF)
    assertion.bind("bibo", BIBO)
    assertion.bind("doco", DOCO)
    assertion.bind("deo", DEO)
    assertion.bind("cito", CITO)
    assertion.bind("fabio", FABIO)
    assertion.bind("schema", SCHEMA)
    assertion.bind("skos", SKOS)
    
    # Define template base URI and placeholders
    template_base = "https://w3id.org/np/RAScientificPaperTemplate#"
    
    # Create placeholder URIs
    paper_placeholder = URIRef(template_base + "paper")
    paper_title_placeholder = URIRef(template_base + "paperTitle")
    paper_abstract_placeholder = URIRef(template_base + "paperAbstract")
    publication_date_placeholder = URIRef(template_base + "publicationDate")
    journal_placeholder = URIRef(template_base + "journal")
    author_placeholder = URIRef(template_base + "author")
    author_name_placeholder = URIRef(template_base + "authorName")
    has_introduction_placeholder = URIRef(template_base + "hasIntroduction")
    has_methods_placeholder = URIRef(template_base + "hasMethods")
    has_results_placeholder = URIRef(template_base + "hasResults")
    has_discussion_placeholder = URIRef(template_base + "hasDiscussion")
    research_goal_placeholder = URIRef(template_base + "researchGoal")
    hypothesis_placeholder = URIRef(template_base + "hypothesis")
    cited_paper_placeholder = URIRef(template_base + "citedPaper")
    citation_type_placeholder = URIRef(template_base + "citationType")
    research_field_placeholder = URIRef(template_base + "researchField")
    
    # Statement URIs
    statements = [URIRef(template_base + f"st{i:02d}") for i in range(1, 16)]
    
    # Add property and class labels
    labels = {
        FABIO.ResearchPaper: "research paper - a scholarly paper reporting original research results",
        BIBO.AcademicArticle: "academic article - a scholarly article published in an academic venue",
        DEO.Introduction: "introduction - opening section that establishes context and purpose",
        DEO.Methods: "methods - section describing methodology and procedures",
        DEO.Results: "results - section presenting findings and outcomes", 
        DEO.Discussion: "discussion - section analyzing and interpreting results",
        DCTERMS.title: "has title",
        DCTERMS.abstract: "has abstract",
        DCTERMS.date: "has publication date",
        DCTERMS.creator: "has author/creator",
        DCTERMS.isPartOf: "is part of (journal or venue)",
        DCTERMS.subject: "has subject/research field",
        DOCO.hasSection: "has document section",
        DEO.hasGoal: "has research goal",
        DEO.hasHypothesis: "has hypothesis",
        FOAF.name: "has name",
        RDF.type: "is a - connects a thing to a class it belongs to",
        CITO.cites: "cites",
        CITO.extends: "extends",
        CITO.supports: "supports", 
        CITO.agreesWith: "agrees with",
        CITO.disagreesWith: "disagrees with",
        CITO.citesAsEvidence: "cites as evidence",
        CITO.usesMethodIn: "uses method in",
        CITO.usesDataFrom: "uses data from"
    }
    
    for entity, label in labels.items():
        assertion.add((entity, RDFS.label, Literal(label)))
    
    # Define paper placeholder (main subject)
    assertion.add((paper_placeholder, RDF.type, NT.IntroducedResource))
    assertion.add((paper_placeholder, RDF.type, NT.ExternalUriPlaceholder))
    assertion.add((paper_placeholder, RDFS.label, Literal("DOI or URL of the scientific paper")))
    
    # Define basic metadata placeholders
    assertion.add((paper_title_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((paper_title_placeholder, RDFS.label, Literal("Title of the paper")))
    assertion.add((paper_title_placeholder, NT.hasRegex, Literal(".{5,200}")))
    
    assertion.add((paper_abstract_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((paper_abstract_placeholder, RDFS.label, Literal("Abstract of the paper")))
    assertion.add((paper_abstract_placeholder, NT.hasRegex, Literal(".{50,2000}")))
    
    assertion.add((publication_date_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((publication_date_placeholder, RDFS.label, Literal("Publication date (YYYY-MM-DD format)")))
    assertion.add((publication_date_placeholder, NT.hasRegex, Literal(r"\d{4}-\d{2}-\d{2}")))
    assertion.add((publication_date_placeholder, NT.hasDatatype, XSD.date))
    
    assertion.add((journal_placeholder, RDF.type, NT.ExternalUriPlaceholder))
    assertion.add((journal_placeholder, RDFS.label, Literal("Journal or venue where published")))
    
    # Define author placeholders
    assertion.add((author_placeholder, RDF.type, NT.ExternalUriPlaceholder))
    assertion.add((author_placeholder, RDFS.label, Literal("ORCID ID or URI of an author")))
    
    assertion.add((author_name_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((author_name_placeholder, RDFS.label, Literal("Name of the author")))
    assertion.add((author_name_placeholder, NT.hasRegex, Literal(".{2,50}")))
    
    # Define document structure placeholders
    assertion.add((has_introduction_placeholder, RDF.type, NT.RestrictedChoicePlaceholder))
    assertion.add((has_introduction_placeholder, RDFS.label, Literal("Does the paper have an introduction section?")))
    assertion.add((has_introduction_placeholder, NT.possibleValue, Literal("true")))
    assertion.add((has_introduction_placeholder, NT.possibleValue, Literal("false")))
    
    assertion.add((has_methods_placeholder, RDF.type, NT.RestrictedChoicePlaceholder))
    assertion.add((has_methods_placeholder, RDFS.label, Literal("Does the paper have a methods/methodology section?")))
    assertion.add((has_methods_placeholder, NT.possibleValue, Literal("true")))
    assertion.add((has_methods_placeholder, NT.possibleValue, Literal("false")))
    
    assertion.add((has_results_placeholder, RDF.type, NT.RestrictedChoicePlaceholder))
    assertion.add((has_results_placeholder, RDFS.label, Literal("Does the paper have a results section?")))
    assertion.add((has_results_placeholder, NT.possibleValue, Literal("true")))
    assertion.add((has_results_placeholder, NT.possibleValue, Literal("false")))
    
    assertion.add((has_discussion_placeholder, RDF.type, NT.RestrictedChoicePlaceholder))
    assertion.add((has_discussion_placeholder, RDFS.label, Literal("Does the paper have a discussion/conclusions section?")))
    assertion.add((has_discussion_placeholder, NT.possibleValue, Literal("true")))
    assertion.add((has_discussion_placeholder, NT.possibleValue, Literal("false")))
    
    # Define research content placeholders
    assertion.add((research_goal_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((research_goal_placeholder, RDFS.label, Literal("Main research goal or objective")))
    assertion.add((research_goal_placeholder, NT.hasRegex, Literal(".{10,500}")))
    
    assertion.add((hypothesis_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((hypothesis_placeholder, RDFS.label, Literal("Main hypothesis being tested")))
    assertion.add((hypothesis_placeholder, NT.hasRegex, Literal(".{10,500}")))
    
    # Define citation placeholders
    assertion.add((cited_paper_placeholder, RDF.type, NT.ExternalUriPlaceholder))
    assertion.add((cited_paper_placeholder, RDFS.label, Literal("DOI or URL of a cited paper")))
    
    assertion.add((citation_type_placeholder, RDF.type, NT.RestrictedChoicePlaceholder))
    assertion.add((citation_type_placeholder, RDFS.label, Literal("Type of citation relationship")))
    citation_types = [
        CITO.cites, CITO.extends, CITO.supports, CITO.agreesWith, 
        CITO.disagreesWith, CITO.citesAsEvidence, CITO.usesMethodIn, CITO.usesDataFrom
    ]
    for ct in citation_types:
        assertion.add((citation_type_placeholder, NT.possibleValue, ct))
    
    # Define research field placeholder
    assertion.add((research_field_placeholder, RDF.type, NT.GuidedChoicePlaceholder))
    assertion.add((research_field_placeholder, RDFS.label, Literal("Research field or domain")))
    assertion.add((research_field_placeholder, NT.possibleValuesFromApi, 
                  Literal("https://www.wikidata.org/w/api.php?action=wbsearchentities&language=en&format=json&limit=5&search=")))
    
    # Create the main assertion template
    assertion_uri = URIRef(template_base + "assertion")
    assertion.add((assertion_uri, RDF.type, NT.AssertionTemplate))
    assertion.add((assertion_uri, RDFS.label, Literal("Describing a scientific paper with comprehensive metadata")))
    assertion.add((assertion_uri, NT.hasNanopubLabelPattern, Literal("Scientific Paper: ${paperTitle}")))
    
    # Add description
    description = """<p>This template allows comprehensive semantic annotation of scientific papers using established ontologies for scholarly publishing.</p>
    
    <p>The template incorporates:</p>
    <ul>
    <li><strong>DoCO (Document Components Ontology):</strong> For describing document structure (sections, figures, tables, etc.)</li>
    <li><strong>DEO (Discourse Elements Ontology):</strong> For rhetorical elements (introduction, methods, results, conclusions)</li>
    <li><strong>BIBO (Bibliographic Ontology):</strong> For bibliographic metadata</li>
    <li><strong>CiTO (Citation Typing Ontology):</strong> For characterizing citations</li>
    <li><strong>FOAF:</strong> For author information</li>
    <li><strong>Dublin Core Terms:</strong> For basic metadata</li>
    </ul>
    
    <p>This follows the recommendations from Ruiz-Iniesta & Corcho's ontology review for semantic annotation of scholarly documents.</p>
    
    <p>You can specify:</p>
    <ul>
    <li><strong>Basic Metadata:</strong> Title, abstract, publication date, journal</li>
    <li><strong>Authors:</strong> Multiple authors with ORCID IDs and names</li>
    <li><strong>Document Structure:</strong> Presence of standard sections (introduction, methods, results, discussion)</li>
    <li><strong>Research Content:</strong> Goals, hypotheses, and research questions</li>
    <li><strong>Citations:</strong> Papers cited with specific relationship types</li>
    <li><strong>Research Field:</strong> Domain classification</li>
    </ul>"""
    
    assertion.add((assertion_uri, DCTERMS.description, Literal(description)))
    
    # Add tags
    tags = ["Scientific Publications", "Scholarly Communication", "Research Papers", "Bibliography", "Academic Literature"]
    for tag in tags:
        assertion.add((assertion_uri, NT.hasTag, Literal(tag)))
    
    # Add target nanopub types
    target_types = [FABIO.ResearchPaper, BIBO.AcademicArticle]
    for target_type in target_types:
        assertion.add((assertion_uri, NT.hasTargetNanopubType, target_type))
    
    # Add all statements to the template
    for stmt in statements:
        assertion.add((assertion_uri, NT.hasStatement, stmt))
    
    # Define individual statements
    # st01: Paper is a research paper
    assertion.add((statements[0], RDF.subject, paper_placeholder))
    assertion.add((statements[0], RDF.predicate, RDF.type))
    assertion.add((statements[0], RDF.object, FABIO.ResearchPaper))
    
    # st02: Paper has title
    assertion.add((statements[1], RDF.subject, paper_placeholder))
    assertion.add((statements[1], RDF.predicate, DCTERMS.title))
    assertion.add((statements[1], RDF.object, paper_title_placeholder))
    
    # st03: Paper has abstract (optional)
    assertion.add((statements[2], RDF.subject, paper_placeholder))
    assertion.add((statements[2], RDF.predicate, DCTERMS.abstract))
    assertion.add((statements[2], RDF.object, paper_abstract_placeholder))
    assertion.add((statements[2], RDF.type, NT.OptionalStatement))
    
    # st04: Paper has publication date
    assertion.add((statements[3], RDF.subject, paper_placeholder))
    assertion.add((statements[3], RDF.predicate, DCTERMS.date))
    assertion.add((statements[3], RDF.object, publication_date_placeholder))
    
    # st05: Paper has author (repeatable)
    assertion.add((statements[4], RDF.subject, paper_placeholder))
    assertion.add((statements[4], RDF.predicate, DCTERMS.creator))
    assertion.add((statements[4], RDF.object, author_placeholder))
    assertion.add((statements[4], RDF.type, NT.RepeatableStatement))
    
    # st06: Author has name (repeatable)
    assertion.add((statements[5], RDF.subject, author_placeholder))
    assertion.add((statements[5], RDF.predicate, FOAF.name))
    assertion.add((statements[5], RDF.object, author_name_placeholder))
    assertion.add((statements[5], RDF.type, NT.RepeatableStatement))
    
    # st07: Paper is part of journal (optional)
    assertion.add((statements[6], RDF.subject, paper_placeholder))
    assertion.add((statements[6], RDF.predicate, DCTERMS.isPartOf))
    assertion.add((statements[6], RDF.object, journal_placeholder))
    assertion.add((statements[6], RDF.type, NT.OptionalStatement))
    
    # st08-11: Document structure sections (all optional)
    section_statements = [
        (statements[7], DEO.Introduction, has_introduction_placeholder),
        (statements[8], DEO.Methods, has_methods_placeholder),
        (statements[9], DEO.Results, has_results_placeholder),
        (statements[10], DEO.Discussion, has_discussion_placeholder)
    ]
    
    for stmt, section_type, condition in section_statements:
        assertion.add((stmt, RDF.subject, paper_placeholder))
        assertion.add((stmt, RDF.predicate, DOCO.hasSection))
        assertion.add((stmt, RDF.object, section_type))
        assertion.add((stmt, NT.statementIri, condition))
        assertion.add((stmt, RDF.type, NT.OptionalStatement))
    
    # st12: Paper has research goal (optional)
    assertion.add((statements[11], RDF.subject, paper_placeholder))
    assertion.add((statements[11], RDF.predicate, DEO.hasGoal))
    assertion.add((statements[11], RDF.object, research_goal_placeholder))
    assertion.add((statements[11], RDF.type, NT.OptionalStatement))
    
    # st13: Paper has hypothesis (optional)
    assertion.add((statements[12], RDF.subject, paper_placeholder))
    assertion.add((statements[12], RDF.predicate, DEO.hasHypothesis))
    assertion.add((statements[12], RDF.object, hypothesis_placeholder))
    assertion.add((statements[12], RDF.type, NT.OptionalStatement))
    
    # st14: Paper cites other papers (optional, repeatable)
    assertion.add((statements[13], RDF.subject, paper_placeholder))
    assertion.add((statements[13], RDF.predicate, citation_type_placeholder))
    assertion.add((statements[13], RDF.object, cited_paper_placeholder))
    assertion.add((statements[13], RDF.type, NT.RepeatableStatement))
    assertion.add((statements[13], RDF.type, NT.OptionalStatement))
    
    # st15: Paper has research field/subject (optional, repeatable)
    assertion.add((statements[14], RDF.subject, paper_placeholder))
    assertion.add((statements[14], RDF.predicate, DCTERMS.subject))
    assertion.add((statements[14], RDF.object, research_field_placeholder))
    assertion.add((statements[14], RDF.type, NT.RepeatableStatement))
    assertion.add((statements[14], RDF.type, NT.OptionalStatement))
    
    # Create provenance graph
    provenance = Graph()
    provenance.add((assertion_uri, PROV.wasAttributedTo, URIRef(profile.orcid_id)))
    
    # Create pubinfo graph
    pubinfo = Graph()
    pubinfo.add((URIRef(profile.orcid_id), FOAF.name, Literal(profile.name)))
    
    # Configure nanopub
    np_conf = NanopubConf(
        profile=profile,
        use_test_server=False,  # Set to False for production
        add_prov_generated_time=True,
        add_pubinfo_generated_time=True,
        attribute_publication_to_profile=True,
    )
    
    # Create the nanopublication
    np = Nanopub(
        conf=np_conf,
        assertion=assertion,
        provenance=provenance,
        pubinfo=pubinfo
    )
    
    return np

def main():
    """Main function to create and publish the template."""
    
    print("Creating Scientific Paper Template nanopublication...")
    
    # Create the template
    template_np = create_scientific_paper_template()
    
    if template_np is None:
        print("Failed to create template. Please check your nanopub profile setup.")
        return
    
    try:
        # Sign the nanopub
        print("Signing nanopublication...")
        template_np.sign()
        print(f"✓ Signed nanopub: {template_np.source_uri}")
        
        # Optionally publish (uncomment to publish to nanopub server)
        # print("Publishing nanopublication...")
        # template_np.publish()
        # print(f"✓ Published nanopub: {template_np.source_uri}")
        
        # Save to file
        output_file = Path("scientific_paper_template.trig")
        template_np.store(output_file, format='trig')
        print(f"✓ Saved template to: {output_file}")
        
        # Print the nanopub
        print("\n" + "="*80)
        print("GENERATED NANOPUBLICATION TEMPLATE:")
        print("="*80)
        print(template_np)
        
    except Exception as e:
        print(f"Error processing nanopub: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    main()
