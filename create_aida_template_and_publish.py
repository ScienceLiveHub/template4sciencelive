#!/usr/bin/env python3
"""
Create a nanopublication template for AIDA sentences with spatial-temporal coverage
and scientific paper citations using the nanopub-py library.
"""

import rdflib
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, FOAF
from nanopub import Nanopub, NanopubConf, Profile # load_profile
from pathlib import Path

# Constructing profile for publishing nanopublications
def create_memory_profile(name: str, orcid_id: str):
    """Create profile entirely in memory without file I/O"""
    profile = Profile(
        name=name,
        orcid_id=orcid_id
    )
    return profile

def create_aida_spatiotemporal_template():
    """
    Create a nanopublication template for AIDA sentences with spatial-temporal
    coverage and paper citation capabilities.
    """
    
    # Load user profile (make sure you have set up your profile first)
    try:
        #profile = load_profile()
        # Set up Anne Fouilloux's profile
        profile = create_memory_profile(
           name="Anne Fouilloux",
           orcid_id="https://orcid.org/0000-0002-1784-2920"
        )
    except Exception as e:
        print(f"Error loading profile: {e}")
        print("Please run 'np setup' to configure your nanopub profile first.")
        return None
    
    # Define namespaces
    NP = Namespace("http://www.nanopub.org/nschema#")
    NPX = Namespace("http://purl.org/nanopub/x/")
    NT = Namespace("https://w3id.org/np/o/ntemplate/")
    PROV = Namespace("http://www.w3.org/ns/prov#")
    HYCL = Namespace("http://purl.org/petapico/o/hycl#")
    CITO = Namespace("http://purl.org/spar/cito/")
    FABIO = Namespace("http://purl.org/spar/fabio/")
    DOCO = Namespace("http://purl.org/spar/doco/")
    DCAT = Namespace("http://www.w3.org/ns/dcat#")
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
    assertion.bind("hycl", HYCL)
    assertion.bind("cito", CITO)
    assertion.bind("fabio", FABIO)
    assertion.bind("doco", DOCO)
    assertion.bind("dcat", DCAT)
    assertion.bind("schema", SCHEMA)
    assertion.bind("skos", SKOS)
    assertion.bind("foaf", FOAF)
    
    # Define template base URI and placeholders
    template_base = "https://w3id.org/np/RASpatio-TemporalAIDA-Template123#"
    
    # Create placeholder URIs
    aida_placeholder = URIRef(template_base + "aida")
    topic_placeholder = URIRef(template_base + "topic")
    project_placeholder = URIRef(template_base + "project")
    dataset_placeholder = URIRef(template_base + "dataset")
    scientific_paper_placeholder = URIRef(template_base + "scientificPaper")
    citation_type_placeholder = URIRef(template_base + "citationType")
    extracted_text_placeholder = URIRef(template_base + "extractedText")
    text_chunk_placeholder = URIRef(template_base + "textChunk")
    page_number_placeholder = URIRef(template_base + "pageNumber")
    section_title_placeholder = URIRef(template_base + "sectionTitle")
    paragraph_number_placeholder = URIRef(template_base + "paragraphNumber")
    extraction_type_placeholder = URIRef(template_base + "extractionType")
    spatial_coverage_placeholder = URIRef(template_base + "spatialCoverage")
    spatial_resolution_placeholder = URIRef(template_base + "spatialResolution")
    temporal_start_placeholder = URIRef(template_base + "temporalStart")
    temporal_end_placeholder = URIRef(template_base + "temporalEnd")
    temporal_resolution_placeholder = URIRef(template_base + "temporalResolution")
    temporal_period_placeholder = URIRef(template_base + "temporalPeriod")
    
    # Statement URIs
    statements = [URIRef(template_base + f"st{i}") for i in range(20)]
    
    # Add property labels
    property_labels = {
        HYCL["AIDA-Sentence"]: "AIDA sentence - an English sentence that is Atomic, Independent, Declarative, and Absolute",
        CITO.obtainsSupportFrom: "obtains support from",
        SCHEMA.about: "is about - connects a thing (left) to a subject matter that this thing is about (right)",
        RDF.type: "is an - connects a thing (left) to a class it belongs to (right)",
        SKOS.related: "is related to",
        CITO.cites: "cites",
        CITO.citesAsSourceDocument: "cites as source document",
        FABIO.ScholarlyWork: "scholarly work - any kind of scholarly work, such as an article, book, etc.",
        DOCO.TextChunk: "text chunk - a piece of text from a document",
        CITO.includesQuotationFrom: "includes quotation from",
        FABIO.hasPageNumber: "has page number",
        DOCO.Section: "document section",
        DOCO.Paragraph: "document paragraph",
        DCTERMS.spatial: "has spatial coverage",
        DCTERMS.temporal: "has temporal extent",
        DCAT.spatialResolutionInMeters: "has spatial resolution in meters",
        DCAT.temporalResolution: "has temporal resolution"
    }
    
    for prop, label in property_labels.items():
        assertion.add((prop, RDFS.label, Literal(label)))
    
    # Define AIDA sentence placeholder
    assertion.add((aida_placeholder, RDF.type, NT.AutoEscapeUriPlaceholder))
    assertion.add((aida_placeholder, RDF.type, NT.IntroducedResource))
    assertion.add((aida_placeholder, RDFS.label, Literal("Type your AIDA sentence here (ending with a full stop)")))
    assertion.add((aida_placeholder, NT.hasPrefix, Literal("http://purl.org/aida/")))
    assertion.add((aida_placeholder, NT.hasPrefixLabel, Literal("The sentence")))
    assertion.add((aida_placeholder, NT.hasRegex, Literal(r"[\S ]{5,500}\.")))
    
    # Define spatial coverage placeholders
    assertion.add((spatial_coverage_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((spatial_coverage_placeholder, RDFS.label, Literal("Spatial coverage (e.g., WKT geometry, place name, or bounding box)")))
    assertion.add((spatial_coverage_placeholder, NT.hasRegex, Literal(".{2,200}")))
    
    assertion.add((spatial_resolution_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((spatial_resolution_placeholder, RDFS.label, Literal("Spatial resolution in meters (optional)")))
    assertion.add((spatial_resolution_placeholder, NT.hasDatatype, XSD.decimal))
    
    # Define temporal coverage placeholders
    assertion.add((temporal_start_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((temporal_start_placeholder, RDFS.label, Literal("Temporal coverage start (ISO 8601 format, e.g., 2023-01-01 or 2023-01-01T00:00:00Z)")))
    assertion.add((temporal_start_placeholder, NT.hasDatatype, XSD.dateTime))
    
    assertion.add((temporal_end_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((temporal_end_placeholder, RDFS.label, Literal("Temporal coverage end (ISO 8601 format, e.g., 2023-12-31 or 2023-12-31T23:59:59Z)")))
    assertion.add((temporal_end_placeholder, NT.hasDatatype, XSD.dateTime))
    
    assertion.add((temporal_resolution_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((temporal_resolution_placeholder, RDFS.label, Literal("Temporal resolution (optional, ISO 8601 duration format, e.g., P1D for daily, P1M for monthly)")))
    assertion.add((temporal_resolution_placeholder, NT.hasDatatype, XSD.duration))
    
    # Define topic and project placeholders
    assertion.add((topic_placeholder, RDF.type, NT.GuidedChoicePlaceholder))
    assertion.add((topic_placeholder, RDFS.label, Literal("URI of concept or topic the sentence is about")))
    assertion.add((topic_placeholder, NT.possibleValuesFromApi, Literal("http://purl.org/nanopub/api/find_signed_things?type=http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23Class&searchterm=")))
    assertion.add((topic_placeholder, NT.possibleValuesFromApi, Literal("https://www.wikidata.org/w/api.php?action=wbsearchentities&language=en&format=json&limit=5&search=")))
    
    assertion.add((project_placeholder, RDF.type, NT.GuidedChoicePlaceholder))
    assertion.add((project_placeholder, RDFS.label, Literal("URI of nanopublication for related research project (optional)")))
    assertion.add((project_placeholder, NT.possibleValuesFromApi, Literal("https://w3id.org/np/l/nanopub-query-1.1/api/RAz6f1v82BCG0SjYMfHUe-m927VTVKdwvsuq1X7j1qcA8/find-things?type=https://schema.org/ResearchProject")))
    
    assertion.add((dataset_placeholder, RDF.type, NT.UriPlaceholder))
    assertion.add((dataset_placeholder, RDFS.label, Literal("URI of nanopublication for related dataset (optional)")))
    
    # Define scientific paper placeholders
    assertion.add((scientific_paper_placeholder, RDF.type, NT.ExternalUriPlaceholder))
    assertion.add((scientific_paper_placeholder, RDFS.label, Literal("DOI (https://doi.org/10...) or other URL of the scientific paper (optional)")))
    
    assertion.add((citation_type_placeholder, RDF.type, NT.RestrictedChoicePlaceholder))
    assertion.add((citation_type_placeholder, RDFS.label, Literal("Select the citation relationship type (optional)")))
    # Add possible citation types
    citation_types = [
        CITO.cites, CITO.citesAsSourceDocument, CITO.obtainsSupportFrom,
        CITO.usesDataFrom, CITO.usesMethodIn, CITO.extends,
        CITO.confirms, CITO.supports
    ]
    for ct in citation_types:
        assertion.add((citation_type_placeholder, NT.possibleValue, ct))
    
    # Define text extraction placeholders
    assertion.add((extracted_text_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((extracted_text_placeholder, RDFS.label, Literal("Text extracted from the paper (quote or paraphrase)")))
    
    assertion.add((text_chunk_placeholder, RDF.type, NT.LocalResource))
    assertion.add((text_chunk_placeholder, RDFS.label, Literal("Text chunk from paper")))
    
    assertion.add((page_number_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((page_number_placeholder, RDFS.label, Literal("Page number or section reference (e.g., 'p. 123', 'pp. 45-47', 'Table 2')")))
    assertion.add((page_number_placeholder, NT.hasRegex, Literal(".{1,50}")))
    
    assertion.add((section_title_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((section_title_placeholder, RDFS.label, Literal("Section title or heading (e.g., 'Abstract', 'Results', 'Discussion', 'Figure 3 caption')")))
    assertion.add((section_title_placeholder, NT.hasRegex, Literal(".{1,200}")))
    
    assertion.add((paragraph_number_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((paragraph_number_placeholder, RDFS.label, Literal("Paragraph number or position within section (optional, e.g., 'paragraph 2', 'first sentence')")))
    assertion.add((paragraph_number_placeholder, NT.hasRegex, Literal(".{1,100}")))
    
    assertion.add((extraction_type_placeholder, RDF.type, NT.RestrictedChoicePlaceholder))
    assertion.add((extraction_type_placeholder, RDFS.label, Literal("Type of text extraction")))
    extraction_types = ["direct quote", "paraphrase", "summary", "data point"]
    for et in extraction_types:
        assertion.add((extraction_type_placeholder, NT.possibleValue, Literal(et)))
    
    assertion.add((temporal_period_placeholder, RDF.type, NT.LocalResource))
    assertion.add((temporal_period_placeholder, RDFS.label, Literal("Temporal period")))
    
    # Create the main assertion template
    assertion_uri = URIRef(template_base + "assertion")
    assertion.add((assertion_uri, RDF.type, NT.AssertionTemplate))
    assertion.add((assertion_uri, RDFS.label, Literal("Expressing a research statement as an AIDA sentence with spatial-temporal coverage and paper citations")))
    assertion.add((assertion_uri, NT.hasNanopubLabelPattern, Literal("AIDA sentence with context: ${aida}")))
    
    # Add description
    description = """<p>This template allows you to express a research statement as an AIDA sentence while also capturing its spatial and temporal context, and optionally linking to scientific papers and specific text extracts.</p>

<p>AIDA sentences are:<p>

<ul>
<li><strong>Atomic:</strong> a sentence describing one thought that cannot be further broken down in a practical way</li>
<li><strong>Independent:</strong> a sentence that can stand on its own, without external references like "this effect" or "we"</li>
<li><strong>Declarative:</strong> a complete sentence ending with a full stop that could in theory be either true or false</li>
<li><strong>Absolute:</strong> a sentence describing the core of a claim ignoring the (un)certainty about its truth and ignoring how it was discovered (no "probably" or "evaluation showed that"); typically in present tense</li>
</ul>

<p>Additionally, you can specify:</p>
<ul>
<li><strong>Spatial Coverage:</strong> Where the research applies (geographic location, bounding box, or geometry)</li>
<li><strong>Temporal Coverage:</strong> When the research applies or was conducted</li>
<li><strong>Resolution:</strong> The precision of spatial and temporal measurements</li>
<li><strong>Scientific Paper:</strong> DOI or URL of the source paper</li>
<li><strong>Text Extract:</strong> Multiple specific quotes or paraphrases from the paper, each with precise location details (page, section, paragraph)</li>
</ul>

<p>You can find more information about AIDA sentences <a href="https://github.com/tkuhn/aida" target="_blank">here</a> and about CiTO citation types <a href="http://purl.org/spar/cito" target="_blank">here</a>.</p>"""
    
    assertion.add((assertion_uri, DCTERMS.description, Literal(description)))
    
    # Add tags
    tags = ["Claims", "Spatiotemporal", "Geography", "Time", "Citations", "Papers"]
    for tag in tags:
        assertion.add((assertion_uri, NT.hasTag, Literal(tag)))
    
    # Add target nanopub types
    target_types = [HYCL["AIDA-Sentence"], HYCL[""], CITO.cites, FABIO.ScholarlyWork]
    for target_type in target_types:
        assertion.add((assertion_uri, NT.hasTargetNanopubType, target_type))
    
    # Add all statements to the template
    for i, stmt in enumerate(statements):
        assertion.add((assertion_uri, NT.hasStatement, stmt))
    
    # Define individual statements
    # Core AIDA sentence statements
    assertion.add((statements[0], RDF.object, HYCL["AIDA-Sentence"]))
    assertion.add((statements[0], RDF.predicate, RDF.type))
    assertion.add((statements[0], RDF.subject, aida_placeholder))
    
    assertion.add((statements[1], RDF.object, topic_placeholder))
    assertion.add((statements[1], RDF.predicate, SCHEMA.about))
    assertion.add((statements[1], RDF.subject, aida_placeholder))
    assertion.add((statements[1], RDF.type, NT.OptionalStatement))
    assertion.add((statements[1], RDF.type, NT.RepeatableStatement))
    
    assertion.add((statements[2], RDF.object, project_placeholder))
    assertion.add((statements[2], RDF.predicate, SKOS.related))
    assertion.add((statements[2], RDF.subject, aida_placeholder))
    assertion.add((statements[2], RDF.type, NT.OptionalStatement))
    
    assertion.add((statements[3], RDF.object, dataset_placeholder))
    assertion.add((statements[3], RDF.predicate, CITO.obtainsSupportFrom))
    assertion.add((statements[3], RDF.subject, aida_placeholder))
    assertion.add((statements[3], RDF.type, NT.OptionalStatement))
    
    # Spatial coverage statements
    assertion.add((statements[4], RDF.object, spatial_coverage_placeholder))
    assertion.add((statements[4], RDF.predicate, DCTERMS.spatial))
    assertion.add((statements[4], RDF.subject, aida_placeholder))
    assertion.add((statements[4], RDF.type, NT.OptionalStatement))
    
    assertion.add((statements[5], RDF.object, spatial_resolution_placeholder))
    assertion.add((statements[5], RDF.predicate, DCAT.spatialResolutionInMeters))
    assertion.add((statements[5], RDF.subject, aida_placeholder))
    assertion.add((statements[5], RDF.type, NT.OptionalStatement))
    
    # Temporal coverage statements
    assertion.add((statements[6], RDF.object, temporal_period_placeholder))
    assertion.add((statements[6], RDF.predicate, DCTERMS.temporal))
    assertion.add((statements[6], RDF.subject, aida_placeholder))
    assertion.add((statements[6], RDF.type, NT.OptionalStatement))
    
    assertion.add((statements[7], RDF.object, DCTERMS.PeriodOfTime))
    assertion.add((statements[7], RDF.predicate, RDF.type))
    assertion.add((statements[7], RDF.subject, temporal_period_placeholder))
    assertion.add((statements[7], RDF.type, NT.OptionalStatement))
    
    assertion.add((statements[8], RDF.object, temporal_start_placeholder))
    assertion.add((statements[8], RDF.predicate, DCAT.startDate))
    assertion.add((statements[8], RDF.subject, temporal_period_placeholder))
    assertion.add((statements[8], RDF.type, NT.OptionalStatement))
    
    assertion.add((statements[9], RDF.object, temporal_end_placeholder))
    assertion.add((statements[9], RDF.predicate, DCAT.endDate))
    assertion.add((statements[9], RDF.subject, temporal_period_placeholder))
    assertion.add((statements[9], RDF.type, NT.OptionalStatement))
    
    assertion.add((statements[10], RDF.object, temporal_resolution_placeholder))
    assertion.add((statements[10], RDF.predicate, DCAT.temporalResolution))
    assertion.add((statements[10], RDF.subject, aida_placeholder))
    assertion.add((statements[10], RDF.type, NT.OptionalStatement))
    
    # Scientific paper citation statements
    assertion.add((statements[11], RDF.object, FABIO.ScholarlyWork))
    assertion.add((statements[11], RDF.predicate, RDF.type))
    assertion.add((statements[11], RDF.subject, scientific_paper_placeholder))
    assertion.add((statements[11], RDF.type, NT.OptionalStatement))
    
    assertion.add((statements[12], RDF.object, scientific_paper_placeholder))
    assertion.add((statements[12], RDF.predicate, citation_type_placeholder))
    assertion.add((statements[12], RDF.subject, aida_placeholder))
    assertion.add((statements[12], RDF.type, NT.OptionalStatement))
    
    # Text extraction statements (repeatable for multiple extracts)
    assertion.add((statements[13], RDF.object, text_chunk_placeholder))
    assertion.add((statements[13], RDF.predicate, CITO.includesQuotationFrom))
    assertion.add((statements[13], RDF.subject, aida_placeholder))
    assertion.add((statements[13], RDF.type, NT.OptionalStatement))
    assertion.add((statements[13], RDF.type, NT.RepeatableStatement))
    
    assertion.add((statements[14], RDF.object, DOCO.TextChunk))
    assertion.add((statements[14], RDF.predicate, RDF.type))
    assertion.add((statements[14], RDF.subject, text_chunk_placeholder))
    assertion.add((statements[14], RDF.type, NT.OptionalStatement))
    assertion.add((statements[14], RDF.type, NT.RepeatableStatement))
    
    assertion.add((statements[15], RDF.object, extracted_text_placeholder))
    assertion.add((statements[15], RDF.predicate, RDFS.comment))
    assertion.add((statements[15], RDF.subject, text_chunk_placeholder))
    assertion.add((statements[15], RDF.type, NT.OptionalStatement))
    assertion.add((statements[15], RDF.type, NT.RepeatableStatement))
    
    assertion.add((statements[16], RDF.object, scientific_paper_placeholder))
    assertion.add((statements[16], RDF.predicate, DCTERMS.isPartOf))
    assertion.add((statements[16], RDF.subject, text_chunk_placeholder))
    assertion.add((statements[16], RDF.type, NT.OptionalStatement))
    assertion.add((statements[16], RDF.type, NT.RepeatableStatement))
    
    assertion.add((statements[17], RDF.object, page_number_placeholder))
    assertion.add((statements[17], RDF.predicate, FABIO.hasPageNumber))
    assertion.add((statements[17], RDF.subject, text_chunk_placeholder))
    assertion.add((statements[17], RDF.type, NT.OptionalStatement))
    assertion.add((statements[17], RDF.type, NT.RepeatableStatement))
    
    assertion.add((statements[18], RDF.object, section_title_placeholder))
    assertion.add((statements[18], RDF.predicate, DCTERMS.title))
    assertion.add((statements[18], RDF.subject, text_chunk_placeholder))
    assertion.add((statements[18], RDF.type, NT.OptionalStatement))
    assertion.add((statements[18], RDF.type, NT.RepeatableStatement))
    
    assertion.add((statements[19], RDF.object, paragraph_number_placeholder))
    assertion.add((statements[19], RDF.predicate, DOCO.hasContent))
    assertion.add((statements[19], RDF.subject, text_chunk_placeholder))
    assertion.add((statements[19], RDF.type, NT.OptionalStatement))
    assertion.add((statements[19], RDF.type, NT.RepeatableStatement))
    
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
    np.pubinfo.add((
        np.metadata.sig_uri,
        NPX["signedBy"],
        rdflib.URIRef(profile.orcid_id),
    ))
    
    return np

def main():
    """Main function to create and publish the template."""
    
    print("Creating AIDA Spatiotemporal Template nanopublication...")
    
    # Create the template
    template_np = create_aida_spatiotemporal_template()
    
    if template_np is None:
        print("Failed to create template. Please check your nanopub profile setup.")
        return
    
    try:
        # Sign the nanopub
        print("Signing nanopublication...")
        template_np.sign()
        print(f"✓ Signed nanopub: {template_np.source_uri}")
        
        # Optionally publish (uncomment to publish to nanopub server)
        #AF print("Publishing nanopublication...")
        #AF template_np.publish()
        #AF print(f"✓ Published nanopub: {template_np.source_uri}")
        
        # Save to file
        output_file = Path("aida_spatiotemporal_template.trig")
        template_np.store(output_file, format='trig')
        print(f"✓ Saved template to: {output_file}")
        
        # Print the nanopub
        print("\n" + "="*80)
        print("GENERATED NANOPUBLICATION TEMPLATE:")
        print("="*80)
        print(template_np)
        
    except Exception as e:
        print(f"Error processing nanopub: {e}")
        return

if __name__ == "__main__":
    main()
