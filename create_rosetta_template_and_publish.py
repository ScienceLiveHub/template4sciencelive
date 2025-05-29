#!/usr/bin/env python3
"""
Create a nanopublication template for Rosetta Statements following the metamodel
described in "Rosetta Statements: Simplifying FAIR Knowledge Graph Construction 
with a User-Centered Approach" by Vogt et al.
"""

import rdflib
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, FOAF
from nanopub import Nanopub, NanopubConf, Profile
from pathlib import Path

def create_memory_profile(name: str, orcid_id: str):
    """Create profile entirely in memory without file I/O"""
    profile = Profile(
        name=name,
        orcid_id=orcid_id
    )
    return profile

def create_rosetta_statement_template():
    """
    Create a nanopublication template for Rosetta Statements based on the
    metamodel described in the Vogt et al. paper.
    """
    
    # Load user profile
    try:
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
    # Use a local namespace for Rosetta Statement concepts within this template
    ROSETTA = Namespace("https://w3id.org/rosetta/")
    SCHEMA = Namespace("http://schema.org/")
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    WIKIDATA = Namespace("http://www.wikidata.org/entity/")
    HYCL = Namespace("http://purl.org/petapico/o/hycl#")
    
    # Create the assertion graph
    assertion = Graph()
    
    # Bind namespaces
    assertion.bind("np", NP)
    assertion.bind("npx", NPX)
    assertion.bind("nt", NT)
    assertion.bind("prov", PROV)
    assertion.bind("dcterms", DCTERMS)
    assertion.bind("foaf", FOAF)
    assertion.bind("rosetta", ROSETTA)
    assertion.bind("schema", SCHEMA)
    assertion.bind("skos", SKOS)
    assertion.bind("wd", WIKIDATA)
    assertion.bind("hycl", HYCL)
    
    # Define template base URI and placeholders
    template_base = "https://w3id.org/np/RARosettaStatementTemplate#"
    
    # Core Rosetta Statement placeholders
    statement_instance_placeholder = URIRef(template_base + "statementInstance")
    statement_type_placeholder = URIRef(template_base + "statementType")
    statement_label_placeholder = URIRef(template_base + "statementLabel")
    dynamic_label_template_placeholder = URIRef(template_base + "dynamicLabelTemplate")
    
    # Subject and object placeholders
    subject_resource_placeholder = URIRef(template_base + "subjectResource")
    subject_label_placeholder = URIRef(template_base + "subjectLabel")
    
    # Object position placeholders (supporting n-ary statements)
    object_position_1_placeholder = URIRef(template_base + "objectPosition1")
    object_position_2_placeholder = URIRef(template_base + "objectPosition2")
    object_position_3_placeholder = URIRef(template_base + "objectPosition3")
    object_position_4_placeholder = URIRef(template_base + "objectPosition4")
    
    # Object type and constraint placeholders
    object_1_type_placeholder = URIRef(template_base + "object1Type")
    object_2_type_placeholder = URIRef(template_base + "object2Type")
    object_3_type_placeholder = URIRef(template_base + "object3Type")
    object_4_type_placeholder = URIRef(template_base + "object4Type")
    
    # Metadata placeholders
    confidence_level_placeholder = URIRef(template_base + "confidenceLevel")
    context_placeholder = URIRef(template_base + "context")
    negation_placeholder = URIRef(template_base + "isNegation")
    source_reference_placeholder = URIRef(template_base + "sourceReference")
    
    # Versioning placeholders (for full version)
    version_placeholder = URIRef(template_base + "version")
    anchor_statement_placeholder = URIRef(template_base + "anchorStatement")
    
    # Statement URIs
    statements = [URIRef(template_base + f"st{i:02d}") for i in range(1, 21)]
    
    # Add property and class labels based on Rosetta Statement metamodel
    # Define our own Rosetta Statement vocabulary since the GitHub repo isn't web-resolvable
    labels = {
        ROSETTA.RosettaStatement: "Rosetta Statement - a natural language statement modeled semantically",
        ROSETTA.subject: "has subject - connects statement to its subject resource",
        ROSETTA.requiredObjectPosition1: "required object position 1 - first mandatory object",
        ROSETTA.requiredObjectPosition2: "required object position 2 - second mandatory object", 
        ROSETTA.optionalObjectPosition1: "optional object position 1 - first optional object",
        ROSETTA.optionalObjectPosition2: "optional object position 2 - second optional object",
        ROSETTA.optionalObjectPosition3: "optional object position 3 - third optional object",
        ROSETTA.requiredLiteralObjectPosition1: "required literal object position 1 - first mandatory literal",
        ROSETTA.optionalLiteralObjectPosition1: "optional literal object position 1 - first optional literal",
        ROSETTA.hasStatementType: "has statement type - connects to Rosetta Statement class",
        ROSETTA.hasDynamicLabel: "has dynamic label - template for natural language display",
        ROSETTA.hasConfidenceLevel: "has confidence level - degree of certainty (0-1)",
        ROSETTA.hasContext: "has context - scholarly publication or broader context",
        ROSETTA.isNegation: "is negation - whether this statement is negated",
        ROSETTA.hasSourceReference: "has source reference - supporting evidence",
        ROSETTA.hasVersion: "has version - links to statement version",
        ROSETTA.anchorStatement: "anchor statement - version-independent statement identity",
        HYCL["AIDA-Sentence"]: "AIDA sentence - Atomic, Independent, Declarative, Absolute sentence",
        DCTERMS.created: "created - timestamp of creation",
        DCTERMS.creator: "creator - person who created this statement",
        PROV.wasAttributedTo: "was attributed to - attribution of statement",
        RDF.type: "is a - connects to class/type"
    }
    
    for entity, label in labels.items():
        assertion.add((entity, RDFS.label, Literal(label)))
    
    # Define statement instance placeholder (main subject)
    assertion.add((statement_instance_placeholder, RDF.type, NT.IntroducedResource))
    assertion.add((statement_instance_placeholder, RDFS.label, Literal("The Rosetta Statement instance")))
    
    # Define statement type placeholder
    assertion.add((statement_type_placeholder, RDF.type, NT.GuidedChoicePlaceholder))
    assertion.add((statement_type_placeholder, RDFS.label, Literal("Type of Rosetta Statement (predicate-based classification)")))
    assertion.add((statement_type_placeholder, NT.possibleValuesFromApi, 
                  Literal("https://w3id.org/np/l/nanopub-query-1.1/api/find-things?type=https://w3id.org/rosetta/RosettaStatementClass")))
    
    # Define dynamic label template
    assertion.add((dynamic_label_template_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((dynamic_label_template_placeholder, RDFS.label, 
                  Literal("Dynamic label template (e.g., 'SUBJECT has QUALITY of VALUE UNIT')")))
    assertion.add((dynamic_label_template_placeholder, NT.hasRegex, Literal(".{10,200}")))
    
    # Define subject resource placeholder
    assertion.add((subject_resource_placeholder, RDF.type, NT.ExternalUriPlaceholder))
    assertion.add((subject_resource_placeholder, RDFS.label, Literal("Subject resource (Wikidata URI or ontology term)")))
    
    assertion.add((subject_label_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((subject_label_placeholder, RDFS.label, Literal("Human-readable label for subject")))
    assertion.add((subject_label_placeholder, NT.hasRegex, Literal(".{1,100}")))
    
    # Define object position placeholders (supporting n-ary predicates)
    object_positions = [
        (object_position_1_placeholder, "First object (required or optional)"),
        (object_position_2_placeholder, "Second object (optional)"),  
        (object_position_3_placeholder, "Third object (optional)"),
        (object_position_4_placeholder, "Fourth object (optional)")
    ]
    
    for obj_placeholder, label in object_positions:
        assertion.add((obj_placeholder, RDF.type, NT.ExternalUriPlaceholder))
        assertion.add((obj_placeholder, RDFS.label, Literal(label)))
    
    # Define object type constraints
    object_types = [
        (object_1_type_placeholder, "Constraint for first object position"),
        (object_2_type_placeholder, "Constraint for second object position"),
        (object_3_type_placeholder, "Constraint for third object position"), 
        (object_4_type_placeholder, "Constraint for fourth object position")
    ]
    
    for type_placeholder, label in object_types:
        assertion.add((type_placeholder, RDF.type, NT.RestrictedChoicePlaceholder))
        assertion.add((type_placeholder, RDFS.label, Literal(label)))
        assertion.add((type_placeholder, NT.possibleValue, Literal("resource")))
        assertion.add((type_placeholder, NT.possibleValue, Literal("literal")))
        assertion.add((type_placeholder, NT.possibleValue, Literal("text")))
        assertion.add((type_placeholder, NT.possibleValue, Literal("number")))
        assertion.add((type_placeholder, NT.possibleValue, Literal("date")))
        assertion.add((type_placeholder, NT.possibleValue, Literal("boolean")))
    
    # Define metadata placeholders
    assertion.add((confidence_level_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((confidence_level_placeholder, RDFS.label, Literal("Confidence level (0.0-1.0)")))
    assertion.add((confidence_level_placeholder, NT.hasDatatype, XSD.decimal))
    assertion.add((confidence_level_placeholder, NT.hasRegex, Literal("^(0(\\.\\d+)?|1(\\.0+)?)$")))
    
    assertion.add((context_placeholder, RDF.type, NT.ExternalUriPlaceholder))
    assertion.add((context_placeholder, RDFS.label, Literal("Context (e.g., DOI of scholarly publication)")))
    
    assertion.add((negation_placeholder, RDF.type, NT.RestrictedChoicePlaceholder))
    assertion.add((negation_placeholder, RDFS.label, Literal("Is this statement negated?")))
    assertion.add((negation_placeholder, NT.possibleValue, Literal("true")))
    assertion.add((negation_placeholder, NT.possibleValue, Literal("false")))
    
    assertion.add((source_reference_placeholder, RDF.type, NT.ExternalUriPlaceholder))
    assertion.add((source_reference_placeholder, RDFS.label, Literal("Source reference supporting this statement")))
    
    # Versioning placeholders
    assertion.add((version_placeholder, RDF.type, NT.LiteralPlaceholder))
    assertion.add((version_placeholder, RDFS.label, Literal("Version identifier")))
    assertion.add((version_placeholder, NT.hasRegex, Literal(".{1,50}")))
    
    assertion.add((anchor_statement_placeholder, RDF.type, NT.LocalResource))
    assertion.add((anchor_statement_placeholder, RDFS.label, Literal("Anchor statement for versioning")))
    
    # Create the main assertion template
    assertion_uri = URIRef(template_base + "assertion")
    assertion.add((assertion_uri, RDF.type, NT.AssertionTemplate))
    assertion.add((assertion_uri, RDFS.label, Literal("Creating a Rosetta Statement following the natural language statement metamodel")))
    assertion.add((assertion_uri, NT.hasNanopubLabelPattern, Literal("Rosetta Statement: ${dynamicLabelTemplate}")))
    
    # Add comprehensive description
    description = """<p>This template allows you to create Rosetta Statements following the metamodel described in "Rosetta Statements: Simplifying FAIR Knowledge Graph Construction with a User-Centered Approach".</p>

<p><strong>Rosetta Statements</strong> model the structure of simple English natural language statements rather than attempting to represent a mind-independent reality. They prioritize:</p>
<ul>
<li><strong>Cognitive Interoperability:</strong> Easy to understand for domain experts</li>
<li><strong>Findability:</strong> Supports search without requiring SPARQL knowledge</li>
<li><strong>Semantic Interoperability:</strong> Standardized patterns for each statement type</li>
<li><strong>User-Centered Design:</strong> Reflects natural language structure</li>
</ul>

<p><strong>Key Features:</strong></p>
<ul>
<li><strong>N-ary Support:</strong> Handle statements with multiple objects (not just binary relations)</li>
<li><strong>Dynamic Labels:</strong> Display as natural language sentences in user interfaces</li>
<li><strong>Versioning Support:</strong> Track changes and editing history</li>
<li><strong>Metadata Rich:</strong> Include confidence levels, negation, context, and provenance</li>
<li><strong>Wikidata Integration:</strong> Use Wikidata terms for immediate usability</li>
</ul>

<p><strong>Statement Structure:</strong></p>
<ul>
<li><strong>Subject:</strong> The main entity the statement is about</li>
<li><strong>Predicate:</strong> Captured by the statement type/class</li>
<li><strong>Objects:</strong> Up to 4 object positions (resources or literals)</li>
<li><strong>Constraints:</strong> Type restrictions for each position</li>
</ul>

<p><strong>Example:</strong> "This apple has a weight of 241.68 grams" becomes a 'has-measurement' statement type with subject=apple, object1=weight (quality), object2=241.68 (value), object3=gram (unit).</p>

<p>This approach significantly lowers the barrier for domain experts to create FAIR knowledge graphs without requiring expertise in semantics, RDF, or ontology engineering.</p>"""
    
    assertion.add((assertion_uri, DCTERMS.description, Literal(description)))
    
    # Add tags
    tags = ["Rosetta Statements", "Natural Language", "Knowledge Graphs", "FAIR", "Cognitive Interoperability", "Semantic Modeling"]
    for tag in tags:
        assertion.add((assertion_uri, NT.hasTag, Literal(tag)))
    
    # Add target nanopub types
    target_types = [ROSETTA.RosettaStatement, SCHEMA.Statement]
    for target_type in target_types:
        assertion.add((assertion_uri, NT.hasTargetNanopubType, target_type))
    
    # Add all statements to the template
    for stmt in statements:
        assertion.add((assertion_uri, NT.hasStatement, stmt))
    
    # Define individual statements following Rosetta Statement metamodel
    
    # st01: Statement instance is a Rosetta Statement
    assertion.add((statements[0], RDF.subject, statement_instance_placeholder))
    assertion.add((statements[0], RDF.predicate, RDF.type))
    assertion.add((statements[0], RDF.object, ROSETTA.RosettaStatement))
    
    # st02: Statement has statement type/class
    assertion.add((statements[1], RDF.subject, statement_instance_placeholder))
    assertion.add((statements[1], RDF.predicate, ROSETTA.hasStatementType))
    assertion.add((statements[1], RDF.object, statement_type_placeholder))
    
    # st03: Statement has dynamic label template
    assertion.add((statements[2], RDF.subject, statement_instance_placeholder))
    assertion.add((statements[2], RDF.predicate, ROSETTA.hasDynamicLabel))
    assertion.add((statements[2], RDF.object, dynamic_label_template_placeholder))
    assertion.add((statements[2], RDF.type, NT.OptionalStatement))
    
    # st04: Statement has subject
    assertion.add((statements[3], RDF.subject, statement_instance_placeholder))
    assertion.add((statements[3], RDF.predicate, ROSETTA.subject))
    assertion.add((statements[3], RDF.object, subject_resource_placeholder))
    
    # st05: Subject has label
    assertion.add((statements[4], RDF.subject, subject_resource_placeholder))
    assertion.add((statements[4], RDF.predicate, RDFS.label))
    assertion.add((statements[4], RDF.object, subject_label_placeholder))
    assertion.add((statements[4], RDF.type, NT.OptionalStatement))
    
    # st06-09: Object positions (first is required, others optional)
    assertion.add((statements[5], RDF.subject, statement_instance_placeholder))
    assertion.add((statements[5], RDF.predicate, ROSETTA.requiredObjectPosition1))
    assertion.add((statements[5], RDF.object, object_position_1_placeholder))
    
    assertion.add((statements[6], RDF.subject, statement_instance_placeholder))
    assertion.add((statements[6], RDF.predicate, ROSETTA.optionalObjectPosition1))
    assertion.add((statements[6], RDF.object, object_position_2_placeholder))
    assertion.add((statements[6], RDF.type, NT.OptionalStatement))
    
    assertion.add((statements[7], RDF.subject, statement_instance_placeholder))
    assertion.add((statements[7], RDF.predicate, ROSETTA.optionalObjectPosition2))
    assertion.add((statements[7], RDF.object, object_position_3_placeholder))
    assertion.add((statements[7], RDF.type, NT.OptionalStatement))
    
    assertion.add((statements[8], RDF.subject, statement_instance_placeholder))
    assertion.add((statements[8], RDF.predicate, ROSETTA.optionalObjectPosition3))
    assertion.add((statements[8], RDF.object, object_position_4_placeholder))
    assertion.add((statements[8], RDF.type, NT.OptionalStatement))
    
    # st10: Confidence level (optional)
    assertion.add((statements[9], RDF.subject, statement_instance_placeholder))
    assertion.add((statements[9], RDF.predicate, ROSETTA.hasConfidenceLevel))
    assertion.add((statements[9], RDF.object, confidence_level_placeholder))
    assertion.add((statements[9], RDF.type, NT.OptionalStatement))
    
    # st11: Context (optional)
    assertion.add((statements[10], RDF.subject, statement_instance_placeholder))
    assertion.add((statements[10], RDF.predicate, ROSETTA.hasContext))
    assertion.add((statements[10], RDF.object, context_placeholder))
    assertion.add((statements[10], RDF.type, NT.OptionalStatement))
    
    # st12: Negation flag (optional)
    assertion.add((statements[11], RDF.subject, statement_instance_placeholder))
    assertion.add((statements[11], RDF.predicate, ROSETTA.isNegation))
    assertion.add((statements[11], RDF.object, negation_placeholder))
    assertion.add((statements[11], RDF.type, NT.OptionalStatement))
    
    # st13: Source reference (optional, repeatable)
    assertion.add((statements[12], RDF.subject, statement_instance_placeholder))
    assertion.add((statements[12], RDF.predicate, ROSETTA.hasSourceReference))
    assertion.add((statements[12], RDF.object, source_reference_placeholder))
    assertion.add((statements[12], RDF.type, NT.OptionalStatement))
    assertion.add((statements[12], RDF.type, NT.RepeatableStatement))
    
    # st14: Version (optional - for full version with versioning)
    assertion.add((statements[13], RDF.subject, statement_instance_placeholder))
    assertion.add((statements[13], RDF.predicate, ROSETTA.hasVersion))
    assertion.add((statements[13], RDF.object, version_placeholder))
    assertion.add((statements[13], RDF.type, NT.OptionalStatement))
    
    # st15: Anchor statement (optional - for versioning)
    assertion.add((statements[14], RDF.subject, anchor_statement_placeholder))
    assertion.add((statements[14], RDF.predicate, ROSETTA.hasVersion))
    assertion.add((statements[14], RDF.object, statement_instance_placeholder))
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
    
    print("Creating Rosetta Statement Template nanopublication...")
    
    # Create the template
    template_np = create_rosetta_statement_template()
    
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
        output_file = Path("rosetta_statement_template.trig")
        template_np.store(output_file, format='trig')
        print(f"✓ Saved template to: {output_file}")
        
        # Print the nanopub
        print("\n" + "="*80)
        print("GENERATED ROSETTA STATEMENT TEMPLATE:")
        print("="*80)
        print(template_np)
        
    except Exception as e:
        print(f"Error processing nanopub: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    main()
